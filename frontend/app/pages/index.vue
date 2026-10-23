<script setup lang="ts">
import type { ApiResponse, ProviderItem } from '#shared/types/display';

const config = useRuntimeConfig();
const { data: res, pending, error } = await useFetch<ApiResponse<ProviderItem[]>>(
  `${config.public.apiBase}/home/`
);
</script>

<template>
  <!-- 这里的 class 会被 layout 里的 :deep(.page-container) 接管样式 -->
  <div class="page-container">
    <div v-if="pending" class="status-box">正在加载供应商列表...</div>
    
    <div v-else-if="error" class="status-box error-text">
      加载失败：{{ error.message }}
    </div>

    <div v-else-if="res && res.code === 200">
      <h2 class="section-title">选择供应商</h2>

      <div class="provider-grid">
        <NuxtLink 
          v-for="provider in res.data" 
          :key="provider.id"
          :to="`/providers/${provider.id}`"
          class="provider-card"
        >
          <div class="provider-avatar">
            {{ provider.name.charAt(0) }}
          </div>
          <h3 class="provider-name">{{ provider.name }}</h3>
          <p class="provider-action">查看模型 →</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 作用域样式：只影响当前组件，不会污染全局 */
.status-box {
  text-align: center;
  padding: 50px;
  color: #666;
}

.error-text {
  color: #ef4444;
}

.section-title {
  border-bottom: 2px solid #eee;
  padding-bottom: 12px;
  margin-bottom: 24px;
  color: #111;
}

.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.provider-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
  background: white;
}

.provider-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  transform: translateY(-2px); /* 鼠标悬浮时卡片微微上浮 */
  border-color: #3b82f6;
}

.provider-avatar {
  width: 64px;
  height: 64px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 50%;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.provider-name {
  margin: 0;
  font-size: 1.2rem;
  color: #111;
}

.provider-action {
  color: #3b82f6;
  font-size: 0.9rem;
  margin-top: 12px;
}
</style>