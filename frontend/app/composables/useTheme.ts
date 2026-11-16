/**
 * 主题（明暗模式）管理。
 *
 * 设计要点：
 * 1. 主题写在 <html data-theme="..."> 上，样式侧只靠 CSS 变量切换，
 *    组件无需感知主题，避免每个组件都维护一份条件判断。
 * 2. 用 useState 托管，保证 SSR/水合前后状态一致，不会出现「服务端亮色、
 *    客户端暗色」的错位。
 * 3. 首屏防闪烁不在这里做——由 nuxt.config.ts 的 head.script 在样式加载前
 *    直接写入 data-theme，本模块只负责后续切换与持久化。
 */
export type ThemeMode = 'light' | 'dark';

const STORAGE_KEY = 'aiwiki-theme';

export function useTheme() {
  const mode = useState<ThemeMode>('theme-mode', () => 'light');

  /** 写入 DOM + 持久化。localStorage 可能被隐私模式禁用，故用 try 兜底 */
  function apply(next: ThemeMode) {
    mode.value = next;
    if (import.meta.client) {
      document.documentElement.dataset.theme = next;
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch {
        /* 忽略：不影响本次会话内的切换 */
      }
    }
  }

  /**
   * 首次挂载时同步一次真实主题。
   * 取值优先级：用户上次选择 > 系统偏好 > 亮色。
   */
  function init() {
    if (!import.meta.client) {
      return;
    }
    let saved: string | null = null;
    try {
      saved = localStorage.getItem(STORAGE_KEY);
    } catch {
      saved = null;
    }
    if (saved === 'light' || saved === 'dark') {
      apply(saved);
      return;
    }
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    apply(prefersDark ? 'dark' : 'light');
  }

  function toggle() {
    apply(mode.value === 'dark' ? 'light' : 'dark');
  }

  return { mode, init, toggle };
}
