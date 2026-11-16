<script setup lang="ts">
/**
 * 顶部阅读进度条。
 *
 * 用 transform: scaleX 而不是改 width：只触发合成层，不引起重排，
 * 滚动时不会额外掉帧。滚动监听设 passive，避免阻塞主线程。
 */
const progress = ref(0);

function update() {
  const doc = document.documentElement;
  const scrollable = doc.scrollHeight - doc.clientHeight;
  progress.value = scrollable > 0 ? doc.scrollTop / scrollable : 0;
}

onMounted(() => {
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  update();
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', update);
  window.removeEventListener('resize', update);
});
</script>

<template>
  <div class="scroll-progress" aria-hidden="true">
    <span class="scroll-progress__bar" :style="{ transform: `scaleX(${progress})` }"></span>
  </div>
</template>

<style scoped>
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
  height: 2px;
  background: transparent;
  pointer-events: none;
}

.scroll-progress__bar {
  display: block;
  height: 100%;
  transform-origin: 0 50%;
  background: linear-gradient(90deg, #2563eb, #7c3aed, #06b6d4);
  box-shadow: 0 0 8px rgba(37, 99, 235, 0.6);
  will-change: transform;
}
</style>
