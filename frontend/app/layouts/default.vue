<!--
  全局布局：吸顶导航栏 + 内容区 + 页脚。

  说明：该文件由根组件 app/app.vue 中的 <NuxtLayout> 触发渲染，
  若根组件缺少 <NuxtLayout>，本布局不会生效。
-->
<template>
  <div class="app-wrapper">
    <header class="global-header">
      <div class="header-content">
        <NuxtLink to="/" class="logo">AIWiki</NuxtLink>
        <nav class="nav-links">
          <NuxtLink to="/">首页</NuxtLink>
          <!-- 后续导航项在此扩展 -->
        </nav>
      </div>
    </header>

    <!-- 内容出口：渲染当前路由匹配到的页面组件 -->
    <main class="main-content">
      <slot />
    </main>

    <footer class="global-footer">
      © 2026 AIWiki - 前端学习实战项目
    </footer>
  </div>
</template>

<style scoped>
/* 纵向弹性布局：配合 .main-content 的 flex: 1，使页脚始终贴底 */
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif;
}

/* sticky 定位实现滚动时吸顶；z-index 保证盖住页面内容 */
.global-header {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 14px 24px;
  background-color: #1f2937;
  color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 内容宽度与 .page-container 对齐，保证导航与页面主体左右边界一致 */
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

/* 当前路由高亮：NuxtLink 会自动附加 router-link-active 类，
   无需在脚本中比对 pathname。默认保留 2px 透明下边框，防止
   高亮时因边框出现导致高度跳动。 */
.nav-links a.router-link-active {
  border-bottom-color: #3b82f6;
  color: #fff;
}

/* 撑满剩余高度，将页脚推至视口底部（内容不足一屏时同样贴底） */
.main-content {
  flex: 1;
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
