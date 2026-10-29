<script setup lang="ts">
import type { ApiResponse, ProviderItem } from '#shared/types/display';

const config = useRuntimeConfig();

// 后端 /api/home/ 支持 page / size，但上限是 le=100，且响应里没有 total，
// 前端无法做真正的分页。这里直接要 100 条，避免默认 size=20 时
// 供应商超过 20 个被静默截断（等后端补 total 后再换成分页器）。
const { data: res, pending, error, refresh } = await useFetch<
  ApiResponse<ProviderItem[]>
>(`${config.public.apiBase}/home/`, {
  query: { page: 1, size: 100 },
});

// 统一从这里取列表：res / data 都可能是 null，集中兜一次，模板里就不用到处写 ?
const providers = computed(() => res.value?.data ?? []);

// 把 error 拆成 statusCode / isNetworkError / 人话文案
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

useSeoMeta({
  title: 'AIWiki - 选择供应商',
  description: '按供应商浏览 AI 模型的能力、上下文长度与定价。',
});
</script>

<template>
  <div class="page-container">
    <h2 class="section-title">选择供应商</h2>

    <div v-if="pending" class="status-box">正在加载供应商列表…</div>

    <!--
      列表接口在「查不到任何启用中的供应商」时会返回 404（后端 raise NotFound）。
      对前端来说这等价于「没有数据」，不该显示成加载失败，所以单独拦一层。
    -->
    <div v-else-if="error && statusCode === 404" class="status-box">
      暂无供应商数据
    </div>

    <div v-else-if="error" class="status-box">
      <p class="error-text">{{ errorMessage }}</p>
      <p v-if="isNetworkError" class="hint">
        启动后端：
        <code>uvicorn main:app --app-dir app --reload --port 8000</code>
      </p>
      <div class="btn-row">
        <button class="btn" @click="refresh()">重试</button>
      </div>
    </div>

    <!--
      空数组也走这里。
      之前的写法是 v-else-if="res && res.code === 200"，一旦返回空数组，
      页面什么都不渲染，看起来就是白屏。
    -->
    <div v-else-if="providers.length === 0" class="status-box">
      暂无供应商数据
    </div>

    <div v-else class="provider-grid">
      <ProviderTile
        v-for="provider in providers"
        :key="provider.id"
        :provider="provider"
      />
    </div>
  </div>
</template>

<style scoped>
/* 只留网格布局；单张卡片的样式在 ProviderTile.vue 里 */
.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
</style>
