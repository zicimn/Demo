<template>
  <div class="app-wrapper">
    <!-- 全局顶部导航栏 -->
    <header class="global-header">
      <div class="header-content">
        <NuxtLink to="/" class="logo">AIWiki</NuxtLink>
        <nav class="nav-links">
          <NuxtLink to="/">首页</NuxtLink>
          <!-- 以后可以在这里加更多导航 -->
        </nav>
      </div>
    </header>

    <!-- 页面主体内容出口：<slot /> 会被替换成 index.vue / [id].vue 的内容 -->
    <main class="main-content">
      <slot />
    </main>

    <!-- 全局底部 -->
    <footer class="global-footer">
      © 2026 AIWiki - 前端学习实战项目
    </footer>
  </div>
</template>

<style scoped>
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif;
}

.global-header {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 14px 24px;
  background-color: #1f2937;
  color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  max-width: 960px;
  margin: 0 auto;
}

.logo {
  color: #fff;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 16px;
}

.nav-links a {
  padding-bottom: 2px;
  border-bottom: 2px solid transparent;
  color: #d1d5db;
  font-size: 0.95rem;
  text-decoration: none;
  transition: color 0.2s, border-color 0.2s;
}

.nav-links a:hover {
  color: #fff;
}

/* Nuxt 会为「当前路由」对应的 NuxtLink 自动加上 router-link-active 类，
   用它做高亮，比在 JS 里比对 pathname 简单得多。
   注意：首页的 "/" 默认是所有路由的前缀，所以还需要 exact-active 才算精确命中。
   单层路由场景下 active 就够了。 */
.nav-links a.router-link-active {
  border-bottom-color: #3b82f6;
  color: #fff;
}

.main-content {
  flex: 1; /* 撑满剩余高度，把页脚顶到最底部 */
  padding: 24px;
}

.global-footer {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
  background-color: #fff;
  color: #6b7280;
  font-size: 0.875rem;
  text-align: center;
}
</style>
