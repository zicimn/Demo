<script setup lang="ts">
import type { AiProvider } from '#shared/types/display';

/** 模型详情页顶部的供应商概要卡片 */
defineProps<{
  provider: AiProvider;
}>();
</script>

<template>
  <div class="provider-card">
    <h2>供应商信息</h2>
    <p>
      名称：
      <!-- 名称作为入口，可返回该供应商详情页 -->
      <NuxtLink :to="`/providers/${provider.provider_code}`" class="provider-link">
        {{ provider.provider_name }}
      </NuxtLink>
      <span class="provider-code">({{ provider.provider_code }})</span>
    </p>
    <p>
      官网：
      <a
        v-if="provider.website_url"
        :href="provider.website_url"
        target="_blank"
        rel="noopener noreferrer"
        class="site-link"
      >
        {{ provider.website_url }}
      </a>
      <span v-else class="muted">暂无官网</span>
    </p>
  </div>
</template>

<style scoped>
.provider-card {
  padding: 16px;
  border-radius: 8px;
  background: #f9fafb;
}

.provider-card h2 {
  margin: 0 0 12px;
  font-size: 1.15rem;
}

.provider-card p {
  margin: 6px 0;
}

.provider-link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.provider-link:hover {
  text-decoration: underline;
}

.provider-code {
  color: #6b7280;
  font-size: 0.9rem;
}

/* 官网地址长度不可控，允许在任意位置换行，避免撑破容器 */
.site-link {
  color: #2563eb;
  word-break: break-all;
}
</style>
