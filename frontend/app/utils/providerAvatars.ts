/**
 * 供应商头像清单。
 *
 * 为什么不直接拼接 `/brand/providers/${code}.webp`：
 * 1. 文件缺失时会产生一次 404 请求，dev 环境下还会触发路由未匹配警告；
 * 2. 拼接出的路径无法在代码里被审计「到底有哪些头像在用」。
 *
 * 用显式清单可以规避这两点：新增头像时在下面加一行，命名与 provider_code 对齐。
 * 未登记的供应商会走文字头像（首字母）回退，不影响页面。
 */
export const PROVIDER_AVATARS: Record<string, string> = {
  deepseek: '/brand/providers/deepseek.webp',
  qwen: '/brand/providers/qwen.webp',
};

/**
 * 取供应商头像路径。
 * @param code provider_code，例如 deepseek
 * @returns 头像 URL；未登记时返回空串，由调用方回退为文字头像
 */
export function providerAvatar(code: string | null | undefined): string {
  if (!code) {
    return '';
  }
  return PROVIDER_AVATARS[code] ?? '';
}
