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

/** 与首页、模型详情页共用同一套错误归一化逻辑 */
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

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
    <div v-if="pending" class="status-box">正在加载供应商信息…</div>

    <!-- 404 单独文案，其余错误使用统一归一化后的提示 -->
    <div v-else-if="error" class="status-box">
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
      <div class="provider-header">
        <h1 class="provider-title">{{ detail.provider.provider_name }}</h1>
        <p class="provider-code">标识：{{ detail.provider.provider_code }}</p>

        <!-- 官网与描述均可为空，为空时整行不渲染，避免出现空标签 -->
        <p v-if="detail.provider.website_url" class="provider-site">
          官网：
          <a
            :href="detail.provider.website_url"
            target="_blank"
            rel="noopener noreferrer"
          >
            {{ detail.provider.website_url }}
          </a>
        </p>
        <p v-if="detail.provider.description" class="provider-desc">
          {{ detail.provider.description }}
        </p>
      </div>

      <div class="models-section">
        <h2 class="section-title">模型列表 (最近 5 条)</h2>

        <p v-if="detail.models_data.length === 0" class="status-box">
          该供应商暂无已上架的模型。
        </p>

        <div v-else class="model-list">
          <NuxtLink
            v-for="model in detail.models_data"
            :key="model.id"
            :to="`/models/${model.id}`"
            class="model-card"
          >
            <div class="model-info">
              <h3 class="model-name">{{ model.display_name }}</h3>
              <p class="model-slug">{{ model.model_slug }}</p>
            </div>
            <div class="model-actions">
              <span class="view-link">查看详情 →</span>
            </div>
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
/* 头部与模型列表之间用分隔线区分信息层级 */
.provider-header {
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.provider-title {
  margin: 0 0 8px;
  font-size: 1.75rem;
  color: #111;
}

.provider-code {
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 0.9rem;
}

.provider-site {
  margin: 0 0 12px;
  font-size: 0.95rem;
}

/* 官网地址长度不可控，允许任意位置换行 */
.provider-site a {
  color: #2563eb;
  word-break: break-all;
}

.provider-desc {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
}

.models-section {
  margin-top: 32px;
}

/* 复用全局 .section-title 时去掉其默认上外边距，避免与上块叠加 */
.models-section .section-title {
  margin-top: 0;
}

.model-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 模型卡片：整行可点击，hover 时描边高亮提示可交互 */
.model-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.model-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.model-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.model-name {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #111;
}

/* 模型标识用等宽字体，便于与接口/文档中的 slug 逐字比对 */
.model-slug {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

.view-link {
  color: #3b82f6;
  font-size: 0.9rem;
  white-space: nowrap;
}

.page-actions {
  margin-top: 32px;
  justify-content: flex-start;
}
</style>
