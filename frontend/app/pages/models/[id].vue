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

/** 与首页共用同一套错误归一化逻辑（见 composables/useApiError） */
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

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
    <div v-if="pending" class="status-box">正在加载模型信息…</div>

    <!-- 404 单独文案，其余错误使用统一归一化后的提示 -->
    <div v-else-if="error" class="status-box">
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
      <h1 class="model-title">{{ detail.model.display_name }}</h1>

      <ProviderCard :provider="detail.provider" />
      <ModelInfo :model="detail.model" />
      <CapabilityList :capabilities="detail.capabilities" />
      <PriceTable :prices="detail.prices" />

      <div class="btn-row page-actions">
        <NuxtLink to="/" class="btn btn--ghost">← 返回首页</NuxtLink>
      </div>
    </template>
  </div>
</template>

<style scoped>
.model-title {
  margin: 0 0 24px;
  font-size: 1.75rem;
  color: #111;
}

/* 操作区左对齐，与上方内容块保持同一左边距 */
.page-actions {
  margin-top: 32px;
  justify-content: flex-start;
}
</style>
