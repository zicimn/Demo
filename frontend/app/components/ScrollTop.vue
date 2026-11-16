<script setup lang="ts">
/**
 * 返回顶部悬浮按钮。
 *
 * 只在滚动超过阈值后出现，避免首屏就出现无效按钮；
 * 监听挂在 window 上，组件卸载时移除，防止重复挂载导致内存泄漏。
 */
const visible = ref(false);
const THRESHOLD = 320;

function onScroll() {
  visible.value = window.scrollY > THRESHOLD;
}

function toTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

onMounted(() => {
  // passive 让滚动监听不阻塞主线程
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll);
});
</script>

<template>
  <Transition name="fade">
    <button
      v-if="visible"
      type="button"
      class="to-top"
      aria-label="返回顶部"
      title="返回顶部"
      @click="toTop"
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="m6 14 6-6 6 6" />
      </svg>
    </button>
  </Transition>
</template>

<style scoped>
.to-top {
  position: fixed;
  right: 24px;
  bottom: 28px;
  z-index: 30;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  border: 1px solid var(--c-border);
  border-radius: var(--r-full);
  background: var(--c-surface);
  color: var(--c-text-2);
  cursor: pointer;
  box-shadow: var(--sh-md);
  transition: color 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
}

.to-top:hover {
  border-color: var(--c-primary);
  color: var(--c-primary);
  transform: translateY(-3px);
}

.to-top svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* 出入场：轻微上移淡入 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (max-width: 640px) {
  .to-top {
    right: 16px;
    bottom: 18px;
    width: 38px;
    height: 38px;
  }
}
</style>
