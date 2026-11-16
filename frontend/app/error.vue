<script setup lang="ts">
/**
 * 全局错误页。
 *
 * Nuxt 在路由未匹配、服务端异常、或页面内抛出错误时渲染此组件，
 * 且它不套用 layouts/default.vue，因此需要自带最小外壳。
 * 主题与全局 CSS 仍然生效（nuxt.config 的 css 是全站注入的）。
 */
import type { NuxtError } from '#app';

const props = defineProps<{ error: NuxtError }>();

const statusCode = computed(() => Number(props.error?.statusCode) || 500);

const isNotFound = computed(() => statusCode.value === 404);

const title = computed(() => (isNotFound.value ? '这个页面不存在' : '出了点问题'));

const description = computed(() => {
  if (isNotFound.value) {
    return '链接可能已失效，或者地址输错了。可以回到首页重新选择供应商。';
  }
  return (
    props.error?.message ||
    '服务暂时不可用。如果后端未启动，请先启动后重试。'
  );
});

/** clearError 传 redirect 会清空错误状态并跳转，避免刷新后仍停留在错误页 */
function goHome() {
  clearError({ redirect: '/' });
}

/** 重新加载当前地址，用于「后端刚启动好」的场景 */
function retry() {
  if (import.meta.client) {
    window.location.reload();
  }
}
</script>

<template>
  <div class="error-shell">
    <div class="error-card">
      <!-- 状态码做成大字水印，视觉焦点立刻落在错误类型上 -->
      <p class="error-code" aria-hidden="true">{{ statusCode }}</p>

      <svg class="error-art" viewBox="0 0 120 84" aria-hidden="true">
        <rect x="8" y="12" width="104" height="62" rx="10" />
        <path d="M8 30h104" />
        <circle cx="20" cy="21" r="2.6" />
        <circle cx="30" cy="21" r="2.6" />
        <circle cx="40" cy="21" r="2.6" />
        <path d="M42 46h36" />
        <path d="M42 56h22" />
      </svg>

      <h1 class="error-title">{{ title }}</h1>
      <p class="error-desc">{{ description }}</p>

      <div class="btn-row">
        <button class="btn" type="button" @click="goHome">返回首页</button>
        <button class="btn btn--ghost" type="button" @click="retry">
          重新加载
        </button>
      </div>

      <p class="error-hint">
        状态码 {{ statusCode }} · 若持续出现，请确认后端已启动：
        <code>uvicorn main:app --app-dir app --reload --port 8000</code>
      </p>
    </div>
  </div>
</template>

<style scoped>
.error-shell {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 24px;
  background: var(--c-bg);
}

/* 白色卡片 + 轻阴影，与站内其它页面保持同一语言 */
.error-card {
  position: relative;
  width: 100%;
  max-width: 520px;
  padding: 44px 36px 32px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-lg);
  background: var(--c-surface);
  box-shadow: var(--sh-md);
  text-align: center;
  overflow: hidden;
}

/* 大字状态码作为背景水印，避免与正文抢读 */
.error-code {
  position: absolute;
  top: -26px;
  right: -6px;
  margin: 0;
  color: var(--c-text-1);
  font-size: 7.5rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -4px;
  opacity: 0.05;
  pointer-events: none;
  user-select: none;
}

.error-art {
  display: block;
  width: 120px;
  height: 84px;
  margin: 0 auto 18px;
  fill: none;
  stroke: var(--c-primary);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.85;
}

.error-title {
  margin: 0 0 10px;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--c-text-1);
}

.error-desc {
  max-width: 34em;
  margin: 0 auto 24px;
  color: var(--c-text-2);
  font-size: 0.92rem;
  line-height: 1.75;
}

.error-hint {
  margin: 26px 0 0;
  color: var(--c-text-3);
  font-size: 0.76rem;
  line-height: 1.9;
}

.error-hint code {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 8px;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: var(--c-surface-2);
  color: var(--c-text-2);
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.72rem;
  word-break: break-all;
}

@media (max-width: 480px) {
  .error-card {
    padding: 36px 20px 26px;
  }

  .error-code {
    font-size: 6rem;
  }
}
</style>
