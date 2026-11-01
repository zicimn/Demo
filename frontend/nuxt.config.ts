// ============================================================
// nuxt.config.ts —— Nuxt 项目的全局配置文件
// 该文件在项目根目录（和 package.json 同级）
// ============================================================
import process from 'node:process';

export default defineNuxtConfig({
  // ------------------------------------------------------------
  // compatibilityDate
  // Nuxt 用它来判断使用哪些兼容性特性。
  // 一般填项目启动日期即可，不影响功能。
  // ------------------------------------------------------------
  compatibilityDate: '2026-10-10',

  // ------------------------------------------------------------
  // devtools
  // 是否启用 Nuxt DevTools（开发时的可视化调试面板）。
  // 浏览器打开页面时，底部会出现一个浮标，点击可查看组件树、路由、状态等。
  // 开发环境建议开启。
  // ------------------------------------------------------------
  devtools: { enabled: true },

  // ------------------------------------------------------------
  // css
  // 全局样式入口。这里的样式对所有页面生效（不受 scoped 限制），
  // 用来放：CSS 重置、.page-container 这类跨页面复用的容器、
  // 以及页面切换过渡动画的 class。
  // 路径里的 ~ 指向 srcDir，Nuxt 4 的 srcDir 就是 app/，
  // 所以最终解析为 app/assets/css/main.css。
  // ------------------------------------------------------------
  css: ['~/assets/css/main.css'],

  // ------------------------------------------------------------
  // app.head
  // 全站默认的 <head> 内容。单个页面可以用 useSeoMeta() 覆盖。
  // ------------------------------------------------------------
  app: {
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
    // ----------------------------------------------------------
    // pageTransition
    // 页面切换过渡：mode: 'out-in' 表示旧页面先淡出、新页面再淡入，
    // 避免两个页面同时存在于 DOM 导致高度剧烈跳动。
    // name: 'page' 对应 main.css 里的 .page-enter-active 等类名。
    // ----------------------------------------------------------
    pageTransition: { name: 'page', mode: 'out-in' },
  },

  // ------------------------------------------------------------
  // typescript
  // typeCheck: false 表示 dev 和 build 时不做全项目类型检查。
  // 为什么关掉？
  //   Nuxt 有几百个自动生成的文件，全量类型检查非常慢，
  //   会拖慢热更新。
  // 需要检查时手动执行 npm run typecheck。
  // ------------------------------------------------------------
  typescript: {
    typeCheck: false,
  },

  // ------------------------------------------------------------
  // nitro
  // Nitro 是 Nuxt 的服务端引擎（基于 h3）。
  // devProxy 用于开发环境配置代理。
  //
  // ⚠️ 为什么用 nitro.devProxy 而不是 vite.server.proxy？
  //   Nuxt 4 页面默认在服务端渲染（SSR），SSR 阶段发起的请求
  //   由 Nitro 处理，不经过 Vite。
  //   如果只配 vite.server.proxy，SSR 请求会绕过代理，直接
  //   请求 localhost:3000/service/... 然后 404。
  //   所以必须配 nitro.devProxy，才能覆盖 SSR 和浏览器两条路径。
  // ------------------------------------------------------------
  nitro: {
    devProxy: {
      // 匹配所有以 /api 开头的请求
      '/api': {
        // 转发目标：本地后端 FastAPI 服务
        // 后端跑在 8000 端口
        target: 'http://localhost:8000/api',
        // changeOrigin: true 表示把请求头里的 Host 改成目标的 Host。
        // 有些后端会校验 Host，不设置可能被拒绝。
        changeOrigin: true,
      },
    },
  },

  // ------------------------------------------------------------
  // runtimeConfig
  // 运行时配置：在应用运行期间可读取的配置。
  // public 下的字段会同时暴露给服务端和客户端。
  //
  // 为什么用 runtimeConfig 而不是直接硬编码 URL？
  //   1. 环境隔离：开发、测试、生产可以用不同值
  //   2. 可以通过环境变量覆盖：NUXT_PUBLIC_API_BASE=xxx npm run dev
  //   3. 类型安全：useRuntimeConfig() 返回的对象有类型提示
  // ------------------------------------------------------------
  runtimeConfig: {
    public: {
      // API 基础路径。
      // 在组件里用 useRuntimeConfig().public.apiBase 读取。
      //
      // ⚠️ 这里刻意写的是「完整域名」，不是前缀 /api。
      //
      // 原因：SSR 阶段 useFetch 由 Node 直接发起请求，不经过 Vite，
      // 也不经过下面的 nitro.devProxy。Node 环境里没有页面地址可以拼，
      // 相对路径 '/api' 会直接 404 —— 这正是当初那个 404 问题的根因。
      //
      // 写成绝对地址后，服务端和浏览器端走同一条规则：
      //   `${config.public.apiBase}/models/${id}`
      //   = 'http://localhost:8000/api/models/1'
      //
      // 代价：浏览器端变成跨域请求，所以后端必须放行前端源
      // （见 app/main.py 的 CORS_ORIGINS，默认 http://localhost:3000）。
      //
      // 附带说明：因为已经是绝对地址，上面 nitro.devProxy 的 '/api' 规则
      // 实际不会再被命中，属于历史配置。生产环境只需改这一行（比如注入
      // NUXT_PUBLIC_API_BASE=https://api.example.com/api），业务代码不用动。
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api',
    },
  },
});