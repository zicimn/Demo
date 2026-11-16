<script setup lang="ts">
import type { ApiResponse, ProviderItem } from '#shared/types/display';

/**
 * 命令面板（Ctrl/Cmd + K）。
 *
 * 目的：键盘用户不必回到首页也能直达任一供应商。
 * 数据复用首页同一个接口，Nuxt 会走 payload 缓存，不会重复请求。
 */
const config = useRuntimeConfig();
const route = useRoute();

/**
 * 头部是否显示搜索入口。
 * 首页本身有内联搜索框，同时出现两个搜索入口会让用户犹豫点哪个，
 * 因此首页只保留 Ctrl+K 快捷键（并在 Hero 里提示），按钮仅在其他页显示。
 */
const showTrigger = computed(() => route.path !== '/');

const { data: res } = await useFetch<ApiResponse<ProviderItem[]>>(
  `${config.public.apiBase}/providers`,
  { query: { page: 1, size: 100 } },
);

const providers = computed(() => res.value?.data ?? []);

const open = ref(false);
const query = ref('');
const activeIndex = ref(0);
const inputRef = ref<HTMLInputElement | null>(null);

const results = computed(() => {
  const list = providers.value.map((p) => ({
    label: p.provider_name,
    sub: p.provider_code,
    to: `/providers/${p.provider_code}`,
  }));
  const q = query.value.trim().toLowerCase();
  if (!q) {
    return list;
  }
  return list.filter(
    (i) =>
      i.label.toLowerCase().includes(q) || i.sub.toLowerCase().includes(q),
  );
});

// 结果集变化时把选中项归零，避免高亮停在越界下标上
watch(results, () => {
  activeIndex.value = 0;
});

function show() {
  open.value = true;
  query.value = '';
  activeIndex.value = 0;
  nextTick(() => inputRef.value?.focus());
}

function hide() {
  open.value = false;
}

function go(index: number) {
  const target = results.value[index];
  if (!target) {
    return;
  }
  hide();
  navigateTo(target.to);
}

function onKeydown(event: KeyboardEvent) {
  // Ctrl+K / Cmd+K：打开或关闭面板
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    open.value ? hide() : show();
    return;
  }

  if (!open.value) {
    return;
  }

  if (event.key === 'Escape') {
    event.preventDefault();
    hide();
  } else if (event.key === 'ArrowDown') {
    event.preventDefault();
    activeIndex.value = results.value.length
      ? (activeIndex.value + 1) % results.value.length
      : 0;
  } else if (event.key === 'ArrowUp') {
    event.preventDefault();
    activeIndex.value = results.value.length
      ? (activeIndex.value - 1 + results.value.length) % results.value.length
      : 0;
  } else if (event.key === 'Enter') {
    event.preventDefault();
    go(activeIndex.value);
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown);
});
</script>

<template>
  <!-- 头部留一个可点击入口，不依赖用户知道快捷键；首页由内联搜索框承担 -->
  <button
    v-if="showTrigger"
    type="button"
    class="palette-trigger"
    aria-label="打开快速搜索"
    @click="show"
  >
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-3.6-3.6" />
    </svg>
    <kbd>Ctrl K</kbd>
  </button>

  <!-- Teleport 到 body：避免被布局的层叠上下文裁剪 -->
  <Teleport to="body">
    <Transition name="palette">
      <div v-if="open" class="palette-mask" @click.self="hide">
        <div class="palette" role="dialog" aria-modal="true" aria-label="快速搜索">
          <div class="palette-field">
            <svg class="palette-icon" viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-3.6-3.6" />
            </svg>
            <input
              ref="inputRef"
              v-model="query"
              type="text"
              placeholder="搜索供应商名称或标识…"
              aria-label="搜索供应商"
            />
            <kbd class="palette-esc">Esc</kbd>
          </div>

          <ul v-if="results.length" class="palette-list">
            <li v-for="(item, i) in results" :key="item.to">
              <button
                type="button"
                class="palette-item"
                :class="{ 'is-active': i === activeIndex }"
                @mouseenter="activeIndex = i"
                @click="go(i)"
              >
                <span class="palette-dot" aria-hidden="true"></span>
                <span class="palette-label">{{ item.label }}</span>
                <span class="palette-sub mono">{{ item.sub }}</span>
              </button>
            </li>
          </ul>

          <p v-else class="palette-empty">没有匹配的供应商</p>

          <div class="palette-foot">
            <span><kbd>↑</kbd><kbd>↓</kbd> 选择</span>
            <span><kbd>Enter</kbd> 打开</span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* ---------- 触发按钮（放在导航栏） ---------- */
.palette-trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 10px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: var(--r-full);
  background: rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
  cursor: pointer;
  transition: background-color 0.18s ease, border-color 0.18s ease,
    color 0.18s ease;
}

.palette-trigger:hover {
  background: rgba(255, 255, 255, 0.16);
  color: #fff;
}

.palette-trigger svg {
  width: 14px;
  height: 14px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
}

kbd {
  padding: 1px 5px;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 4px;
  font-family: inherit;
  font-size: 0.66rem;
  line-height: 1.5;
}

/* ---------- 遮罩与面板 ---------- */
.palette-mask {
  position: fixed;
  inset: 0;
  z-index: 60;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 14vh 16px 16px;
  background: rgba(8, 12, 20, 0.45);
  backdrop-filter: blur(3px);
}

.palette {
  width: 100%;
  max-width: 560px;
  overflow: hidden;
  border: 1px solid var(--c-border);
  border-radius: var(--r-lg);
  background: var(--c-surface);
  box-shadow: 0 24px 64px rgba(8, 12, 20, 0.35);
}

.palette-field {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--c-border);
}

.palette-icon {
  width: 16px;
  height: 16px;
  flex: 0 0 16px;
  color: var(--c-text-3);
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
}

.palette-field input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  color: var(--c-text-1);
  font-family: inherit;
  font-size: 0.95rem;
}

.palette-field input:focus {
  outline: none;
}

.palette-esc {
  border-color: var(--c-border);
  color: var(--c-text-3);
}

.palette-list {
  max-height: 320px;
  margin: 0;
  padding: 6px;
  overflow-y: auto;
  list-style: none;
}

.palette-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: none;
  border-radius: var(--r-sm);
  background: transparent;
  color: inherit;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
}

/* 选中态：键盘与鼠标共用同一套高亮，行为一致 */
.palette-item.is-active {
  background: var(--c-primary-weak);
}

.palette-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: var(--r-full);
  background: var(--c-primary);
  opacity: 0.7;
}

.palette-label {
  color: var(--c-text-1);
  font-size: 0.9rem;
}

.palette-sub {
  margin-left: auto;
  color: var(--c-text-3);
  font-size: 0.72rem;
}

.palette-empty {
  margin: 0;
  padding: 28px 16px;
  color: var(--c-text-3);
  font-size: 0.86rem;
  text-align: center;
}

.palette-foot {
  display: flex;
  gap: 16px;
  padding: 10px 16px;
  border-top: 1px solid var(--c-border);
  background: var(--c-surface-2);
  color: var(--c-text-3);
  font-size: 0.72rem;
}

.palette-foot kbd {
  margin-right: 3px;
  border-color: var(--c-border-strong);
  color: var(--c-text-2);
}

/* 出场动画：轻微上浮 + 淡入 */
.palette-enter-active,
.palette-leave-active {
  transition: opacity 0.18s ease;
}

.palette-enter-active .palette,
.palette-leave-active .palette {
  transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1);
}

.palette-enter-from,
.palette-leave-to {
  opacity: 0;
}

.palette-enter-from .palette,
.palette-leave-to .palette {
  transform: translateY(-10px) scale(0.98);
}

@media (max-width: 640px) {
  .palette-trigger kbd {
    display: none;
  }
}
</style>
