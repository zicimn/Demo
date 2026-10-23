<template>
  <div class="app-wrapper">
    <!-- 全局顶部导航栏 -->
    <header class="global-header">
      <div class="header-content">
        <NuxtLink to="/" class="logo">
          AIWiki
        </NuxtLink>
        <nav class="nav-links">
          <NuxtLink to="/">首页</NuxtLink>
          <!-- 以后可以在这里加更多导航 -->
        </nav>
      </div>
    </header>

    <!-- 页面主体内容出口 -->
    <main class="main-content">
      <!-- 这里的 <slot /> 会被自动替换为 index.vue 或 [id].vue 的内容 -->
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
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.global-header {
  background-color: #1f2937;
  color: white;
  padding: 16px 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links a {
  color: #d1d5db;
  text-decoration: none;
  margin-left: 16px;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: white;
}

.main-content {
  flex: 1; /* 让主体内容撑满剩余空间 */
  padding: 24px;
  background-color: #f9fafb;
}

.global-footer {
  text-align: center;
  padding: 24px;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;
  background-color: white;
}

/* 这里教给你一个 Vue 特有的 CSS 技巧：深度选择器 */
:deep(.page-container) {
  max-width: 960px;
  margin: 0 auto;
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>