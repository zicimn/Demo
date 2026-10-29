/**
 * useApiError —— 把 useFetch 的 error 拆成「能给用户看的文案」。
 *
 * ⚠️ 这里踩过一个真坑，记录一下：
 *
 * 直觉上「请求没到达服务器」应该表现为「没有 HTTP 状态码」。
 * 但 Nuxt 的 useFetch 会把「fetch failed」（TCP 连不上）统一包装成
 * status = 500 的 FetchError，于是状态码看起来和「后端真的返回了 500」
 * 一模一样 —— 用户会看到「服务端错误（500）」，明明后端根本没启动过。
 *
 * 所以真正的判据不是状态码，而是 error 的 cause 链路：
 *   Node(SSR)  : FetchError -> cause: AggregateError(code: ECONNREFUSED)
 *   浏览器      : TypeError: Failed to fetch / Load failed(Safari)
 * 把这些特征串起来匹配，才能区分「没连上」和「连上了但报错」。
 */

/** error 及其 cause 链上可能出现的关键字段 */
interface ApiErrorLike {
  status?: number;
  statusCode?: number;
  statusMessage?: string;
  message?: string;
  code?: string;
  cause?: unknown;
  errors?: unknown[];
}

/** 出现这些字样，基本可以断定是网络层失败，而不是服务端业务错误 */
const NETWORK_SIGNS = [
  'fetch failed',
  'failed to fetch',
  'load failed',
  'networkerror',
  'network request failed',
  'econnrefused',
  'econnreset',
  'etimedout',
  'enotfound',
  'eai_again',
  'err_connection',
  'err_internet',
];

/**
 * 深度遍历 cause / AggregateError.errors，把 message 和 code 收集成字符串数组。
 * 限制 depth 是为了防止异常对象里出现循环引用。
 */
function collectSignals(err: unknown, depth = 0): string[] {
  if (!err || depth > 4) {
    return [];
  }
  const node = err as ApiErrorLike;
  const signals: string[] = [];

  if (typeof node.message === 'string') {
    signals.push(node.message);
  }
  if (typeof node.code === 'string') {
    signals.push(node.code);
  }
  if (Array.isArray(node.errors)) {
    for (const sub of node.errors) {
      signals.push(...collectSignals(sub, depth + 1));
    }
  }
  if (node.cause) {
    signals.push(...collectSignals(node.cause, depth + 1));
  }
  return signals;
}

function looksLikeNetworkFailure(err: unknown): boolean {
  return collectSignals(err).some((signal) => {
    const text = signal.toLowerCase();
    return NETWORK_SIGNS.some((sign) => text.includes(sign));
  });
}

export function useApiError(error: Ref<unknown>) {
  const config = useRuntimeConfig();

  const raw = computed(() => error.value as ApiErrorLike | null | undefined);

  // 新版本 Nuxt 用 status，老版本用 statusCode，两个都兜一下
  const statusCode = computed(
    () => raw.value?.status ?? raw.value?.statusCode ?? null,
  );

  // 有 error 且没状态码 → 网络层失败（部分版本会这样表现）
  // 有 error 且是 500 → 还要再看 cause，才能区分「没连上」和「后端真报错」
  const isNetworkError = computed(() => {
    if (!raw.value) {
      return false;
    }
    if (statusCode.value === null) {
      return true;
    }
    if (statusCode.value !== 500) {
      return false;
    }
    return looksLikeNetworkFailure(error.value);
  });

  const message = computed(() => {
    if (!raw.value) {
      return '';
    }
    if (isNetworkError.value) {
      return `连不上后端服务 ${config.public.apiBase}，请确认 FastAPI 已在 8000 端口启动。`;
    }
    if (statusCode.value === 404) {
      return raw.value.statusMessage || raw.value.message || '请求的资源不存在';
    }
    if (statusCode.value && statusCode.value >= 500) {
      return `服务端错误（${statusCode.value}），请查看后端控制台日志。`;
    }
    return raw.value.statusMessage || raw.value.message || '未知错误';
  });

  return { statusCode, isNetworkError, message };
}
