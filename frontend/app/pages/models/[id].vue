<script setup lang="ts">
import type { ApiResponse, Detail } from '#shared/types/display';

const route = useRoute();
const modelId = route.params.id;
const config = useRuntimeConfig();

const { data: res, pending, error, refresh } = await useFetch<
  ApiResponse<Detail>
>(`${config.public.apiBase}/models/${modelId}`);

const detail = computed(() => res.value?.data ?? null);

// statusCode / isNetworkError / 人话文案，与首页共用同一套判断逻辑
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

// 标题用函数（getter）而不是写死的值：数据是异步来的，
// 直接传字符串会在数据到达前就把标题定成默认值。
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

.page-actions {
  margin-top: 32px;
  justify-content: flex-start;
}
</style>
