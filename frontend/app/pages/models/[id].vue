<script setup lang="ts">
import type { ApiResponse, Detail } from '#shared/types/display';

const route = useRoute();
/** 路由参数为模型主键 id，与后端 /api/models/{id} 对应 */
const modelId = route.params.id;
const config = useRuntimeConfig();

/**
 * 模型详情数据源。
 * 后端在「模型不存在」或「所属供应商已停用」时返回 404，
 * 因此 404 需单独映射为「不存在」文案，不能笼统归为加载失败。
 */
const { data: res, pending, error, refresh } = await useFetch<
  ApiResponse<Detail>
>(`${config.public.apiBase}/models/${modelId}`);

/** 详情数据；请求失败或响应为空时为 null */
const detail = computed(() => res.value?.data ?? null);

/**
 * 顶部指标条用的思考模式简写。
 * 与 ModelInfo 中的完整文案（「两种模式都支持」）刻意区分：
 * 指标条追求一行内可读，明细区才展开完整表述。
 */
const thinkingLabel: Record<string, string> = {
  none: '不支持',
  non_thinking_only: '仅非思考',
  thinking_only: '仅思考',
  both: '都支持',
  unknown: '未知',
};

/** 与首页共用同一套错误归一化逻辑（见 composables/useApiError） */
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

/** 页内目录：与下方各区块的 id 一一对应 */
const toc = [
  { id: 'sec-provider', label: '供应商信息' },
  { id: 'sec-info', label: '模型信息' },
  { id: 'sec-cap', label: '支持能力' },
  { id: 'sec-price', label: '定价' },
];

/** 记入「最近查看」；push 内部已处理 SSR 与存储异常 */
const { push } = useRecent();
watch(
  detail,
  (d) => {
    if (!d) {
      return;
    }
    push({
      type: 'model',
      label: d.model.display_name,
      sub: d.model.model_slug,
      to: `/models/${d.model.id}`,
    });
  },
  { immediate: true },
);

/**
 * SEO 元信息使用 getter 而非固定值：
 * 数据在 SSR 阶段异步获取，固定值会在数据到达前就写入默认标题。
 */
useSeoMeta({
  title: () =>
    detail.value
      ? `${detail.value.model.display_name} · AIWiki`
      : '模型详情 · AIWiki',
  description: () =>
    detail.value?.model.description ?? '查看模型的能力、上下文长度与定价。',
});
</script>

<template>
  <div class="page-container">
    <div v-if="pending" class="status-box">
      <span class="spinner" aria-hidden="true"></span>
      正在加载模型信息…
    </div>

    <!-- 404 单独文案，其余错误使用统一归一化后的提示 -->
    <div v-else-if="error" class="status-box">
      <svg class="status-svg" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 8v5" />
        <circle cx="12" cy="16" r="0.6" fill="currentColor" stroke="none" />
        <path d="M10.3 3.9 2.6 17a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" />
      </svg>
      <p class="error-text">
        {{ statusCode === 404 ? '模型不存在，或所属供应商已停用' : errorMessage }}
      </p>
      <p v-if="isNetworkError" class="hint">
        启动后端：
        <code>uvicorn main:app --app-dir app --reload --port 8000</code>
      </p>
      <div class="btn-row">
        <button class="btn" @click="refresh()">重试</button>
        <NuxtLink to="/" class="btn btn--ghost">← 返回首页</NuxtLink>
      </div>
    </div>

    <!-- 请求成功但响应体无 data -->
    <div v-else-if="!detail" class="status-box">没有找到该模型的数据</div>

    <template v-else>
      <!-- 页首：面包屑给出层级路径，模型名作为整页视觉起点 -->
      <div class="model-header">
        <nav class="breadcrumb" aria-label="面包屑">
          <NuxtLink to="/">首页</NuxtLink>
          <span class="sep">/</span>
          <NuxtLink :to="`/providers/${detail.provider.provider_code}`">
            {{ detail.provider.provider_name }}
          </NuxtLink>
          <span class="sep">/</span>
          <span class="current">{{ detail.model.display_name }}</span>
        </nav>
        <h1 class="model-title">{{ detail.model.display_name }}</h1>
      </div>

      <!-- 关键指标前置：这三个参数是用户最先比较的，先给结论再给明细 -->
      <div v-reveal class="metric-strip">
        <div class="metric">
          <p class="metric-label">上下文长度</p>
          <p class="metric-value">{{ detail.model.context_length_raw || '—' }}</p>
        </div>
        <div class="metric">
          <p class="metric-label">最大输出</p>
          <p class="metric-value">{{ detail.model.max_output_raw || '—' }}</p>
        </div>
        <div class="metric">
          <p class="metric-label">并发限制</p>
          <p class="metric-value">{{ detail.model.concurrency_limit ?? '—' }}</p>
        </div>
        <div class="metric">
          <p class="metric-label">思考模式</p>
          <p class="metric-value">
            {{ thinkingLabel[detail.model.thinking_support] ?? detail.model.thinking_support }}
          </p>
        </div>
      </div>

      <div class="model-body">
        <div class="model-main">
          <div id="sec-provider" class="anchor-block">
            <ProviderCard :provider="detail.provider" />
          </div>
          <div id="sec-info" class="anchor-block">
            <ModelInfo :model="detail.model" />
          </div>
          <div id="sec-cap" class="anchor-block">
            <CapabilityList :capabilities="detail.capabilities" />
          </div>
          <div id="sec-price" class="anchor-block">
            <PriceTable :prices="detail.prices" />
          </div>
        </div>

        <!-- 宽屏常驻目录；窄屏由组件 CSS 自行隐藏 -->
        <SectionNav :items="toc" />
      </div>

      <div class="btn-row page-actions">
        <NuxtLink to="/" class="btn btn--ghost">← 返回首页</NuxtLink>
      </div>
    </template>
  </div>
</template>

<style scoped>
.model-header {
  margin-bottom: var(--sp-5);
}

/* 宽屏两栏：正文 1fr + 右侧目录 168px；窄屏退回单列 */
.model-body {
  display: block;
}

@media (min-width: 1120px) {
  .model-body {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 168px;
    gap: 32px;
    align-items: start;
  }

  .model-main {
    min-width: 0;
  }
}

/* 锚点定位时为吸顶导航留出安全距离，避免标题被遮住 */
.anchor-block {
  scroll-margin-top: 96px;
}

.model-title {
  margin: 0;
  font-size: 1.6rem;
  line-height: 1.35;
  color: var(--c-text-1);
}

/* 操作区左对齐，与上方内容块保持同一左边距 */
.page-actions {
  margin-top: var(--sp-6);
  justify-content: flex-start;
}

/* ---------- 状态元素 ---------- */
.spinner {
  display: block;
  width: 22px;
  height: 22px;
  margin: 0 auto var(--sp-3);
  border: 2px solid var(--c-border-strong);
  border-top-color: var(--c-primary);
  border-radius: var(--r-full);
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.status-svg {
  display: block;
  width: 32px;
  height: 32px;
  margin: 0 auto var(--sp-3);
  color: var(--c-text-3);
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

@media (max-width: 640px) {
  .model-title {
    font-size: 1.35rem;
  }
}
</style>
