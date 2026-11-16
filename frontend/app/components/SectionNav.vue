<script setup lang="ts">
/**
 * 页面内锚点目录（sticky）。
 *
 * 用于模型详情页这种「三块内容纵向堆叠」的长页：
 * 右侧常驻目录，滚动时自动高亮当前区块。
 *
 * 高亮判定用 IntersectionObserver 而非 scroll 事件：
 * 它只在交叉状态变化时回调，不随滚动逐帧触发，开销更低。
 */
const props = defineProps<{
  items: { id: string; label: string }[];
}>();

const active = ref(props.items[0]?.id ?? '');
let observer: IntersectionObserver | null = null;

onMounted(() => {
  if (typeof IntersectionObserver === 'undefined') {
    return;
  }

  const targets = props.items
    .map((i) => document.getElementById(i.id))
    .filter((el): el is HTMLElement => Boolean(el));

  if (!targets.length) {
    return;
  }

  observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) {
        active.value = visible[0].target.id;
      }
    },
    // 上方留出吸顶导航的高度，下方收窄以尽快切换
    { rootMargin: '-88px 0px -55% 0px', threshold: 0 },
  );

  targets.forEach((el) => observer!.observe(el));
});

onBeforeUnmount(() => {
  observer?.disconnect();
});

function jump(id: string) {
  const el = document.getElementById(id);
  if (!el) {
    return;
  }
  active.value = id;
  el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
</script>

<template>
  <nav class="section-nav" aria-label="页内导航">
    <p class="section-nav__title">本页内容</p>
    <ul>
      <li v-for="item in items" :key="item.id">
        <button
          type="button"
          class="section-nav__link"
          :class="{ 'is-active': active === item.id }"
          @click="jump(item.id)"
        >
          <span class="section-nav__bar" aria-hidden="true"></span>
          {{ item.label }}
        </button>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
/* 只在宽屏出现：窄屏没有横向空间，强行保留会挤压正文 */
.section-nav {
  display: none;
}

@media (min-width: 1120px) {
  .section-nav {
    position: sticky;
    top: 96px;
    display: block;
    align-self: start;
    width: 168px;
    padding-left: 4px;
  }
}

.section-nav__title {
  margin: 0 0 10px;
  color: var(--c-text-3);
  font-size: 0.72rem;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.section-nav ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.section-nav__link {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 6px 0;
  border: none;
  background: none;
  color: var(--c-text-3);
  font-family: inherit;
  font-size: 0.84rem;
  text-align: left;
  cursor: pointer;
  transition: color 0.18s ease;
}

.section-nav__link:hover {
  color: var(--c-text-1);
}

/* 左侧竖线：激活时变长变亮，作为位置指示 */
.section-nav__bar {
  width: 2px;
  height: 14px;
  border-radius: var(--r-full);
  background: var(--c-border-strong);
  transition: background-color 0.18s ease, height 0.18s ease;
}

.section-nav__link.is-active {
  color: var(--c-primary);
  font-weight: 600;
}

.section-nav__link.is-active .section-nav__bar {
  height: 20px;
  background: var(--c-primary);
}
</style>
