<!--
  全局布局：吸顶导航栏 + 内容区 + 页脚。

  由根组件 app/app.vue 的 <NuxtLayout> 触发渲染，缺少该组件则本布局不生效。
  主题初始化放在 onMounted：首屏的实际主题由 nuxt.config.ts 的
  head.script 在样式加载前写入，这里只负责后续同步与交互。
-->
<template>
  <div class="app-wrapper">
    <!-- 键盘用户可直接跳过导航，属于基础可达性要求 -->
    <a class="skip-link" href="#main">跳到主内容</a>

    <!-- 顶部阅读进度条：固定在视口顶端，不占布局 -->
    <ScrollProgress />

    <header class="global-header">
      <div class="header-content">
        <NuxtLink to="/" class="logo">
          <!-- 品牌图可选：把 logo.png 放到 public/brand/ 下即自动生效，
               缺失时静默回退为首字母方块（alt 为空，不会出现破图图标） -->
          <span class="logo-mark">
            <img
              v-if="!logoBroken"
              :src="logoSrc"
              alt=""
              aria-hidden="true"
              @error="logoBroken = true"
            />
            <span v-if="logoBroken" class="logo-initial">A</span>
          </span>
          <span class="logo-text">AIWiki</span>
        </NuxtLink>

        <div class="header-right">
          <nav class="nav-links">
            <NuxtLink to="/">首页</NuxtLink>
          </nav>
          <CommandPalette />
          <ThemeToggle />
        </div>
      </div>
    </header>

    <!-- 内容出口：渲染当前路由匹配到的页面组件 -->
    <main id="main" class="main-content">
      <slot />
    </main>

    <footer class="global-footer">
      <div class="footer-inner">
        <p class="footer-brand">
          <span class="footer-dot-mark" aria-hidden="true"></span>
          AIWiki · AI 模型能力与定价速查
        </p>
        <p class="footer-meta">
          数据来自 FastAPI 接口 · 按供应商浏览 · 支持明暗主题
        </p>
      </div>
    </footer>

    <ScrollTop />
  </div>
</template>

<script setup lang="ts">
const { init } = useTheme();

/**
 * 品牌图路径用变量而非模板字面量。
 * 原因：静态写在 src 里会被 Vite 当作资源去解析导入，
 * 文件不存在时直接构建失败；运行时字符串不做静态解析。
 * 已附一个内置 SVG，替换为自有 logo 时改这里即可。
 */
const logoSrc = '/brand/logo.svg';

/** 品牌图加载失败后置为 true，回退为文字标记 */
const logoBroken = ref(false);

onMounted(() => {
  init();
});
</script>

<style scoped>
/* 纵向弹性布局：配合 .main-content 的 flex: 1，使页脚始终贴底 */
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.global-header {
  position: sticky;
  top: 0;
  z-index: 20;
  padding: 14px 32px;
  background: linear-gradient(120deg, #0d1524 0%, #1a2333 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  transition: background 0.28s ease;
}

/* 与 .page-container 的最大宽度保持一致，避免内容左右错位 */
.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  max-width: 1320px;
  margin: 0 auto;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  font-size: 1.22rem;
  font-weight: 700;
  letter-spacing: 0.3px;
  text-decoration: none;
}

/* 品牌标记：有图显示图，无图显示首字母 */
.logo-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  color: #fff;
  font-size: 1.05rem;
  font-weight: 800;
  line-height: 1;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.45);
}

.logo-mark img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-text {
  line-height: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-links {
  display: flex;
  gap: 6px;
}

.nav-links a {
  padding: 7px 16px;
  border-radius: var(--r-full);
  color: #cbd5e1;
  font-size: 0.98rem;
  text-decoration: none;
  transition: color 0.18s ease, background-color 0.18s ease;
}

.nav-links a:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

.nav-links a.router-link-active {
  color: #fff;
  background: rgba(59, 130, 246, 0.28);
  box-shadow: inset 0 0 0 1px rgba(147, 197, 253, 0.35);
}

.main-content {
  flex: 1;
  /* 左右留白走全局变量：首页 Hero 用它的负值实现全宽出血 */
  padding: 32px var(--page-gutter) 56px;
}

.global-footer {
  border-top: 1px solid var(--c-border);
  background: var(--c-surface);
  padding: 24px var(--sp-4);
  transition: background-color 0.28s ease, border-color 0.28s ease;
}

.footer-inner {
  max-width: 1320px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  color: var(--c-text-2);
  font-size: 0.9rem;
}

/* 页脚小圆点：与顶部 logo 呼应，弱化装饰 */
.footer-dot-mark {
  width: 6px;
  height: 6px;
  border-radius: var(--r-full);
  background: linear-gradient(135deg, #3b82f6, #6366f1);
}

.footer-meta {
  margin: 0;
  color: var(--c-text-3);
  font-size: 0.82rem;
}

@media (max-width: 640px) {
  .global-header {
    padding: 10px 16px;
  }

  .main-content {
    padding: var(--sp-4) var(--page-gutter) var(--sp-5);
  }

  .logo-text {
    font-size: 0.95rem;
  }

  .nav-links {
    display: none;
  }
}
</style>
