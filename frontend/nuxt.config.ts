/**
 * Nuxt 应用全局配置。
 *
 * 集中管理：全局样式、路由过渡、SEO 默认值、接口地址。
 * 修改本文件需重启 dev server 才会生效。
 */
import process from 'node:process';

export default defineNuxtConfig({
  /** 用于判定采用哪些 Nuxt 兼容性特性，填项目初始化日期即可 */
  compatibilityDate: '2026-10-10',

  /** Nuxt DevTools 调试面板，仅开发环境使用 */
  devtools: { enabled: true },

  /**
   * 全局样式入口。
   * 此处引入的样式对所有页面生效（不受 scoped 限制），用于承载
   * CSS 重置、跨页面复用的容器类与路由过渡动画的类名。
   * 路径中的 `~` 指向 srcDir，Nuxt 4 默认为 app/，
   * 因此实际解析到 app/assets/css/main.css。
   */
  css: ['~/assets/css/main.css'],

  app: {
    /**
     * 全站默认 head 内容。
     * 单页可通过 useSeoMeta() 覆盖 title 与 description。
     */
    head: {
      htmlAttrs: { lang: 'zh-CN' },
      title: 'AIWiki - AI 模型能力与定价速查',
      meta: [
        {
          name: 'description',
          content: 'AIWiki：按供应商浏览 AI 模型的能力、上下文长度与定价。',
        },
      ],
    },
    /**
     * 路由切换过渡。
     * mode: 'out-in' 使旧页面先淡出、新页面再淡入，避免两者同时存在于 DOM
     * 导致页面高度剧烈跳动；name: 'page' 对应 main.css 中的 .page-* 类名。
     */
    pageTransition: { name: 'page', mode: 'out-in' },
  },

  /**
   * 关闭构建期全量类型检查。
   * 原因：Nuxt 会生成大量类型文件，全量检查显著拖慢热更新。
   * 需要检查时单独执行 npm run typecheck。
   */
  typescript: {
    typeCheck: false,
  },

  /**
   * 开发环境反向代理。
   *
   * 说明：当前 runtimeConfig.public.apiBase 使用绝对地址，请求不会经过此处，
   * 因此以下规则实际不会被命中。保留该配置是为了将来若改回相对路径
   * 仍能覆盖 SSR 与服务端两条链路——SSR 阶段请求由 Node 发起、不经过 Vite，
   * 仅在 vite.server.proxy 中配置会漏掉 SSR 链路。
   */
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8000/api',
        /** 将请求头 Host 改写为目标地址，部分后端会校验 Host */
        changeOrigin: true,
      },
    },
  },

  runtimeConfig: {
    public: {
      /**
       * 接口基础地址。组件中通过 useRuntimeConfig().public.apiBase 读取。
       *
       * 此处刻意使用「绝对地址」而非 `/api` 前缀：
       * SSR 阶段 useFetch 由 Node 直接发起请求，环境中不存在页面 URL 可供拼接，
       * 相对路径会直接 404。使用绝对地址后，服务端与浏览器端遵循同一规则：
       *   `${apiBase}/models/1` → `http://localhost:8000/api/models/1`
       *
       * 代价：浏览器端变为跨域请求，需后端放行前端源
       * （见 app/main.py 的 CORS_ORIGINS，默认 http://localhost:3000）。
       *
       * 部署到其他环境时，通过环境变量覆盖即可，无需改动业务代码：
       *   NUXT_PUBLIC_API_BASE=https://api.example.com/api
       */
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api',
    },
  },
});
