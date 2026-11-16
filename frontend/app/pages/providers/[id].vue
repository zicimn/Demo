<script setup lang="ts">
import type { ApiResponse, ProviderOverviewData } from '#shared/types/display';

const route = useRoute();
/**
 * 路由文件名虽为 [id]，但承载的是供应商编码（provider_code），
 * 与后端 /api/providers/{provider_code}/... 保持一致。
 */
const providerCode = route.params.id as string;
const config = useRuntimeConfig();

/**
 * 供应商概览数据源。
 * 该接口一次返回「供应商详情 + 最近 5 条模型」，避免详情页发起两次请求。
 * 供应商不存在或已停用时后端返回 404。
 */
const { data: res, pending, error, refresh } = await useFetch<
  ApiResponse<ProviderOverviewData>
>(`${config.public.apiBase}/providers/${providerCode}/overview`);

/** 概览数据；请求失败或响应为空时为 null */
const detail = computed(() => res.value?.data ?? null);

/** 头部文字头像取名称首字母；名称缺失时兜底为 '?' */
const providerInitial = computed(() => {
  const name = (detail.value?.provider.provider_name || '').trim();
  return name ? name.charAt(0).toUpperCase() : '?';
});

/** 与首页、模型详情页共用同一套错误归一化逻辑 */
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

/** 记入「最近查看」；push 内部已处理 SSR 与存储异常 */
const { push } = useRecent();
watch(
  detail,
  (d) => {
    if (!d) {
      return;
    }
    push({
      type: 'provider',
      label: d.provider.provider_name,
      sub: d.provider.provider_code,
      to: `/providers/${d.provider.provider_code}`,
    });
  },
  { immediate: true },
);

/** 标题使用 getter，保证异步数据到达后能正确更新 */
useSeoMeta({
  title: () =>
    detail.value
      ? `${detail.value.provider.provider_name} · AIWiki`
      : '供应商详情 · AIWiki',
});
</script>

<template>
  <div class="page-container">
    <div v-if="pending" class="status-box">
      <span class="spinner" aria-hidden="true"></span>
      正在加载供应商信息…
    </div>

    <!-- 404 单独文案，其余错误使用统一归一化后的提示 -->
    <div v-else-if="error" class="status-box">
      <svg class="status-svg" viewBox="0 0 24 24" aria-hidden="true">
        <path d="M12 8v5" />
        <circle cx="12" cy="16" r="0.6" fill="currentColor" stroke="none" />
        <path d="M10.3 3.9 2.6 17a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" />
      </svg>
      <p class="error-text">
        {{ statusCode === 404 ? '供应商不存在或已停用' : errorMessage }}
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
    <div v-else-if="!detail" class="status-box">没有找到该供应商的数据</div>

    <template v-else>
      <!-- 面包屑：给出当前位置与返回路径 -->
      <nav class="breadcrumb" aria-label="面包屑">
        <NuxtLink to="/">首页</NuxtLink>
        <span class="sep">/</span>
        <span class="current">{{ detail.provider.provider_name }}</span>
      </nav>

      <!-- 头部：整块渐变 banner + 大字水印首字母，视觉上比纯白卡片更醒目 -->
      <div class="provider-header">
        <span class="provider-watermark" aria-hidden="true">{{ providerInitial }}</span>
        <div class="provider-avatar" aria-hidden="true">{{ providerInitial }}</div>

        <div class="provider-main">
          <h1 class="provider-title">{{ detail.provider.provider_name }}</h1>

          <div class="provider-meta">
            <span class="chip mono">{{ detail.provider.provider_code }}</span>

            <!-- 官网与描述均可为空，为空时整块不渲染，避免出现空标签 -->
            <a
              v-if="detail.provider.website_url"
              :href="detail.provider.website_url"
              target="_blank"
              rel="noopener noreferrer"
              class="provider-site"
            >
              访问官网 ↗
            </a>
          </div>

          <p v-if="detail.provider.description" class="provider-desc">
            {{ detail.provider.description }}
          </p>
        </div>
      </div>

      <div class="models-section">
        <h2 class="section-title">模型列表 (最近 5 条)</h2>

        <div v-if="detail.models_data.length === 0" class="status-box">
          <svg class="status-svg" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 7h16v12H4z" />
            <path d="M4 11h16" />
            <path d="M9 15h6" />
          </svg>
          该供应商暂无已上架的模型。
        </div>

        <div v-else class="model-list">
          <NuxtLink
            v-for="model in detail.models_data"
            :key="model.id"
            :to="`/models/${model.id}`"
            class="model-card"
          >
            <div class="model-info">
              <h3 class="model-name">{{ model.display_name }}</h3>
              <p class="model-slug mono">{{ model.model_slug }}</p>
              <!-- 关键规格前置：让用户不必点进去就能横向比较 -->
              <p
                v-if="model.context_length_raw || model.max_output_raw"
                class="model-meta"
              >
                <span v-if="model.context_length_raw">
                  上下文 {{ model.context_length_raw }}
                </span>
                <span v-if="model.max_output_raw" class="meta-sep">·</span>
                <span v-if="model.max_output_raw">
                  {{ model.max_output_raw }}
                </span>
              </p>
            </div>
            <span class="view-link">查看详情 →</span>
          </NuxtLink>
        </div>
      </div>

      <div class="btn-row page-actions">
        <NuxtLink to="/" class="btn btn--ghost">← 返回首页</NuxtLink>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* ---------- 头部 ---------- */
/* banner 式头部：整块渐变 + 超大首字母水印 */
.provider-header {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  display: flex;
  align-items: flex-start;
  gap: var(--sp-4);
  margin-bottom: var(--sp-6);
  padding: 40px 40px 36px;
  border: 1px solid var(--c-border);
  border-radius: 20px;
  background: radial-gradient(
      110% 130% at 8% 0%,
      rgba(37, 99, 235, 0.14) 0%,
      transparent 58%
    ),
    radial-gradient(
      100% 120% at 96% 10%,
      rgba(124, 58, 237, 0.14) 0%,
      transparent 55%
    ),
    linear-gradient(150deg, #f6faff 0%, #edf3ff 100%);
}

/* 大字水印：把首字母放大成装饰，弱到不干扰阅读 */
.provider-watermark {
  position: absolute;
  top: 50%;
  right: 10px;
  z-index: -1;
  transform: translateY(-50%);
  color: var(--c-primary);
  font-size: 10rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -6px;
  opacity: 0.07;
  pointer-events: none;
  user-select: none;
}

/* 首字母头像：与首页卡片同款视觉语言 */
.provider-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 64px;
  width: 64px;
  height: 64px;
  border-radius: var(--r-full);
  background: linear-gradient(135deg, #dbeafe, #e0eaff);
  color: var(--c-primary);
  font-size: 1.65rem;
  font-weight: 700;
  line-height: 1;
  box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.14);
}

.provider-main {
  min-width: 0;
  flex: 1;
}

.provider-title {
  margin: 0 0 10px;
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 800;
  line-height: 1.25;
  letter-spacing: -0.6px;
  color: var(--c-text-1);
}

.provider-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.provider-site {
  color: var(--c-primary);
  font-size: 0.86rem;
  text-decoration: none;
  transition: opacity 0.18s ease;
}

.provider-site:hover {
  opacity: 0.75;
  text-decoration: underline;
}

.provider-desc {
  margin: 0;
  color: var(--c-text-2);
  font-size: 0.9rem;
  line-height: 1.7;
}

/* ---------- 模型列表 ---------- */
.models-section {
  margin-top: var(--sp-6);
}

.model-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 整行可点击；hover 时左侧出现蓝色竖条，给出方向感 */
.model-card {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: 14px 18px 14px 20px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
  background: var(--c-surface);
  text-decoration: none;
  color: inherit;
  transition: border-color 0.18s ease, box-shadow 0.18s ease,
    transform 0.18s ease;
}

.model-card::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 3px;
  height: 0;
  border-radius: 0 var(--r-full) var(--r-full) 0;
  background: var(--c-primary);
  transform: translateY(-50%);
  transition: height 0.2s ease;
}

.model-card:hover {
  border-color: #bfdbfe;
  box-shadow: var(--sh-sm);
  transform: translateX(2px);
}

.model-card:hover::before {
  height: 60%;
}

.model-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.model-name {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-1);
  line-height: 1.45;
}

/* 模型标识用等宽字体，便于与接口/文档中的 slug 逐字比对 */
.model-slug {
  margin: 0;
  color: var(--c-text-3);
  font-size: 0.76rem;
  word-break: break-all;
}

/* 规格行：比 slug 更淡，只作为辅助信息 */
.model-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin: 2px 0 0;
  color: var(--c-text-2);
  font-size: 0.75rem;
}

.meta-sep {
  color: var(--c-border-strong);
}

.view-link {
  flex: 0 0 auto;
  color: var(--c-primary);
  font-size: 0.84rem;
  white-space: nowrap;
}

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
  .provider-header {
    flex-direction: column;
    padding: var(--sp-4);
  }

  .provider-title {
    font-size: 1.3rem;
  }

  .model-card {
    padding: 12px 14px 12px 16px;
  }
}
</style>
