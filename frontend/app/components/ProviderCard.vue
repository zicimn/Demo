<script setup lang="ts">
import type { AiProvider } from '#shared/types/display';

/** 模型详情页顶部的供应商概要卡片 */
const props = defineProps<{
  provider: AiProvider;
}>();

/** 头像首字母；名称缺失时兜底为 '?' */
const initial = computed(() => {
  const name = (props.provider.provider_name || '').trim();
  return name ? name.charAt(0).toUpperCase() : '?';
});
</script>

<template>
  <div class="provider-card">
    <div class="provider-avatar" aria-hidden="true">{{ initial }}</div>

    <div class="provider-body">
      <p class="provider-label">供应商</p>

      <p class="provider-name">
        <!-- 名称作为入口，可返回该供应商详情页 -->
        <NuxtLink
          :to="`/providers/${provider.provider_code}`"
          class="provider-link"
        >
          {{ provider.provider_name }}
        </NuxtLink>
        <span class="provider-code mono">{{ provider.provider_code }}</span>
      </p>

      <p class="provider-site">
        <span class="site-label">官网</span>
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
  </div>
</template>

<style scoped>
/* 横向信息卡：头像 + 两行信息，比纯文字段更有层次 */
.provider-card {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-5);
  border: 1px solid var(--c-border);
  border-radius: var(--r-lg);
  background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
}

.provider-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 44px;
  width: 44px;
  height: 44px;
  border-radius: var(--r-full);
  background: var(--c-surface);
  color: var(--c-primary);
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1;
  box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.14);
}

.provider-body {
  min-width: 0;
  flex: 1;
}

.provider-label {
  margin: 0 0 2px;
  color: var(--c-text-3);
  font-size: 0.74rem;
  letter-spacing: 0.4px;
}

.provider-name {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 6px;
  line-height: 1.5;
}

.provider-link {
  color: var(--c-text-1);
  font-size: 1.05rem;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.18s ease;
}

.provider-link:hover {
  color: var(--c-primary);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.provider-code {
  padding: 1px 8px;
  border-radius: var(--r-full);
  background: rgba(37, 99, 235, 0.1);
  color: var(--c-primary);
  font-size: 0.72rem;
  letter-spacing: 0.3px;
}

.provider-site {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin: 0;
  font-size: 0.84rem;
}

.site-label {
  flex: 0 0 auto;
  color: var(--c-text-3);
  font-size: 0.74rem;
}

/* 官网地址长度不可控，允许在任意位置换行，避免撑破容器 */
.site-link {
  color: var(--c-primary);
  word-break: break-all;
}

.site-link:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .provider-card {
    padding: var(--sp-4);
  }
}
</style>
