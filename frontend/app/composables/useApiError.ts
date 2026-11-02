/**
 * useApiError —— 将 useFetch 的 error 归一化为可直接用于渲染的状态。
 *
 * 背景：
 * 请求未到达服务器（TCP 连接失败）时，useFetch 同样会抛出 FetchError，
 * 且 status 被包装为 500，与后端真实返回 500 的情况无法通过状态码区分。
 * 若直接按状态码渲染，用户会看到「服务端错误（500）」，而后端可能从未启动。
 *
 * 解决方案：
 * 状态码为 500 时，进一步遍历 error 的 cause 链，匹配网络层特有的错误特征：
 *   Node（SSR） ：FetchError.cause → AggregateError { code: 'ECONNREFUSED' }
 *   浏览器      ：TypeError: Failed to fetch / Load failed（Safari）
 * 只有命中这些特征才判定为「网络不可达」。
 *
 * 返回值：
 *   statusCode     HTTP 状态码，无状态码时为 null
 *   isNetworkError 是否为网络层失败
 *   message        面向用户的错误提示文案
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

/** 出现这些字样时，可判定为网络层失败而非服务端业务错误 */
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
 * 深度遍历 cause 与 AggregateError.errors，收集其中的 message 与 code。
 * depth 上限用于防止异常对象存在循环引用时无限递归。
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

/** 判断 cause 链中是否出现网络层错误特征（不区分大小写） */
function looksLikeNetworkFailure(err: unknown): boolean {
  return collectSignals(err).some((signal) => {
    const text = signal.toLowerCase();
    return NETWORK_SIGNS.some((sign) => text.includes(sign));
  });
}

export function useApiError(error: Ref<unknown>) {
  const config = useRuntimeConfig();

  const raw = computed(() => error.value as ApiErrorLike | null | undefined);

  /** 兼容不同 Nuxt 版本：新版本为 status，旧版本为 statusCode */
  const statusCode = computed(
    () => raw.value?.status ?? raw.value?.statusCode ?? null,
  );

  /**
   * 网络失败判定分两步：
   *   1. 无状态码 → 直接判定为网络层失败（部分版本的表现）
   *   2. 状态码为 500 → 再检查 cause 链，才能区分「未连上」与「后端确实报错」
   */
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
