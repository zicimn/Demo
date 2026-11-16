<script setup lang="ts">
/**
 * 「最近查看」横条。
 *
 * 数据来自 localStorage（见 composables/useRecent），仅在客户端读取，
 * 因此首屏 SSR 输出为空，挂载后才出现——不会造成水合不一致。
 */
const { items, load, clear } = useRecent();

onMounted(load);
</script>

<template>
  <section v-if="items.length" class="recent">
    <div class="recent-head">
      <h2 class="section-title">最近查看</h2>
      <button type="button" class="recent-clear" @click="clear">清空</button>
    </div>

    <ul class="recent-list">
      <li v-for="item in items" :key="item.to">
        <NuxtLink :to="item.to" class="recent-item">
          <span class="recent-dot" :class="`recent-dot--${item.type}`" aria-hidden="true"></span>
          <span class="recent-text">
            <span class="recent-label">{{ item.label }}</span>
            <span class="recent-sub mono">{{ item.sub }}</span>
          </span>
        </NuxtLink>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.recent {
  margin-bottom: var(--sp-6);
}

.recent-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

/* section-title 自带底部外边距，这里收掉以便与清空按钮对齐 */
.recent-head :deep(.section-title) {
  margin-bottom: var(--sp-3);
  flex: 1;
}

.recent-clear {
  margin-bottom: var(--sp-3);
  padding: 4px 10px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-full);
  background: var(--c-surface);
  color: var(--c-text-3);
  font-size: 0.75rem;
  font-family: inherit;
  cursor: pointer;
  transition: color 0.18s ease, border-color 0.18s ease;
}

.recent-clear:hover {
  border-color: var(--c-primary);
  color: var(--c-primary);
}

/* 横向滚动而不是换行：条目数固定不超过 6，横向更省纵向空间 */
.recent-list {
  display: flex;
  gap: 10px;
  margin: 0;
  padding: 2px 0 6px;
  list-style: none;
  overflow-x: auto;
  scrollbar-width: thin;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 9px 14px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-full);
  background: var(--c-surface);
  color: inherit;
  text-decoration: none;
  white-space: nowrap;
  transition: border-color 0.18s ease, transform 0.18s ease,
    box-shadow 0.18s ease;
}

.recent-item:hover {
  border-color: var(--c-primary);
  box-shadow: var(--sh-sm);
  transform: translateY(-1px);
}

/* 类型色点：供应商蓝、模型紫，一眼区分 */
.recent-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: var(--r-full);
}

.recent-dot--provider {
  background: var(--c-primary);
}

.recent-dot--model {
  background: #7c3aed;
}

.recent-text {
  display: flex;
  flex-direction: column;
  gap: 0;
  line-height: 1.3;
}

.recent-label {
  color: var(--c-text-1);
  font-size: 0.84rem;
  font-weight: 500;
}

.recent-sub {
  color: var(--c-text-3);
  font-size: 0.68rem;
}
</style>
