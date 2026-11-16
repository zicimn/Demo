/**
 * 最近查看记录（供应商 + 模型）。
 *
 * 纯前端能力，不依赖任何接口改动：用 localStorage 存最近访问的条目，
 * 首页据此渲染「最近查看」横条，减少重复寻找成本。
 *
 * 状态用 useState 托管：SSR 阶段为空数组，客户端挂载后由 load() 填充，
 * 因此不会出现服务端与客户端首屏不一致的警告。
 */
export interface RecentItem {
  /** 类型，用于区分图标与跳转目标 */
  type: 'provider' | 'model';
  /** 主标题，如 DeepSeek */
  label: string;
  /** 副标题，如 provider_code 或 model_slug */
  sub: string;
  /** 目标路径 */
  to: string;
}

const STORAGE_KEY = 'aiwiki-recent';
const MAX_ITEMS = 6;

export function useRecent() {
  const items = useState<RecentItem[]>('recent-items', () => []);

  /** 从 localStorage 读取；隐私模式下 getItem 可能抛错，统一吞掉 */
  function load() {
    if (!import.meta.client) {
      return;
    }
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return;
      }
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        items.value = parsed.slice(0, MAX_ITEMS);
      }
    } catch {
      items.value = [];
    }
  }

  /** 记录一次访问：同路径去重后置顶，超出上限截断 */
  function push(item: RecentItem) {
    if (!import.meta.client) {
      return;
    }
    const next = [item, ...items.value.filter((i) => i.to !== item.to)].slice(
      0,
      MAX_ITEMS,
    );
    items.value = next;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      /* 存不进去不影响本次会话 */
    }
  }

  function clear() {
    items.value = [];
    if (import.meta.client) {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch {
        /* 忽略 */
      }
    }
  }

  return { items, load, push, clear };
}
