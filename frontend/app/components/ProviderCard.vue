<script setup lang="ts">
// 引入我们写好的 AiProvider 类型
import type { AiProvider } from '#shared/types/display';

// ============================================================
// defineProps 是 Vue 3 的语法，用于定义「父组件传给子组件」的数据。
// 语法：defineProps<{ 属性名: 类型 }>()
// 这样写之后，父组件必须传一个 provider 对象给这个组件。
// ============================================================
defineProps<{
  provider: AiProvider;
}>();
</script>

<template>
  <div class="provider-card">
    <h2>供应商信息</h2>
    <p>
      名称：
      <!-- 供应商名做成链接，可以回跳到该供应商的页面 -->
      <NuxtLink :to="`/providers/${provider.id}`" class="provider-link">
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

.site-link {
  color: #2563eb;
  word-break: break-all;
}
</style>
