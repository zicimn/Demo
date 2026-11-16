<script setup lang="ts">
/**
 * 明暗主题切换按钮。
 *
 * 状态来源统一走 useTheme()，与 head.script 的首屏设置共用同一份 useState，
 * 因此不会出现按钮显示「暗」而页面实际是「亮」的错位。
 */
const { mode, toggle } = useTheme();

/** 供 aria-label 与 title 使用；中文描述比图标本身更可读 */
const nextLabel = computed(() =>
  mode.value === 'dark' ? '切换到浅色模式' : '切换到深色模式',
);
</script>

<template>
  <button
    type="button"
    class="theme-toggle"
    :aria-label="nextLabel"
    :title="nextLabel"
    :aria-pressed="mode === 'dark'"
    @click="toggle"
  >
    <!-- 两个图标叠放，靠 .is-dark 控制显隐，避免图标切换时按钮宽度跳动 -->
    <svg class="icon icon-sun" viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="4.2" />
      <path
        d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.2 5.2l1.4 1.4M17.4 17.4l1.4 1.4M18.8 5.2l-1.4 1.4M6.6 17.4l-1.4 1.4"
      />
    </svg>
    <svg class="icon icon-moon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M20 14.2A8.2 8.2 0 0 1 9.8 4a8.2 8.2 0 1 0 10.2 10.2Z" />
    </svg>
  </button>
</template>

<style scoped>
/* 与导航胶囊同尺寸的圆形按钮 */
.theme-toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: var(--r-full);
  background: rgba(255, 255, 255, 0.08);
  color: #e2e8f0;
  cursor: pointer;
  transition: background-color 0.18s ease, border-color 0.18s ease,
    color 0.18s ease, transform 0.18s ease;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.16);
  border-color: rgba(255, 255, 255, 0.28);
  color: #fff;
  transform: rotate(-12deg);
}

.icon {
  position: absolute;
  width: 17px;
  height: 17px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.7;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: opacity 0.22s ease, transform 0.32s cubic-bezier(0.22, 1, 0.36, 1);
}

/* 浅色模式下显示太阳：表示「当前是亮色」 */
.icon-sun {
  opacity: 1;
  transform: rotate(0) scale(1);
}

.icon-moon {
  opacity: 0;
  transform: rotate(-35deg) scale(0.7);
}

/* 深色下的图标互换见 main.css 第 7 节：
   scoped 样式里写 :global(html[..]) .icon-x 会被编译器丢掉后代选择器，
   因此跨主题覆写统一放到全局样式表中处理。 */
</style>
