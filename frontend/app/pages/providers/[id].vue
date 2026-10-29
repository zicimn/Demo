<script setup lang="ts">
const route = useRoute();
const providerId = route.params.id;

useSeoMeta({
  title: () => `供应商 ${providerId} · AIWiki`,
});
</script>

<template>
  <div class="page-container">
    <h1 class="title">供应商工作台</h1>

    <p class="info-box">
      当前正在查看供应商 ID：<strong>{{ providerId }}</strong>
    </p>

    <div class="placeholder-box">
      <h3>🚧 接口开发中</h3>
      <p>后端目前还没有提供「根据供应商 ID 查询其名下所有模型」的 API 接口。</p>
      <p>接口上线后，这里会列出该厂商的模型清单，并跳转到对应的模型详情页。</p>
    </div>

    <div class="btn-row page-actions">
      <NuxtLink to="/" class="btn">← 返回首页</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.title {
  margin: 0 0 24px;
  font-size: 1.75rem;
  color: #111;
}

.info-box {
  margin: 0 0 32px;
  color: #374151;
  font-size: 1.1rem;
}

.info-box strong {
  color: #2563eb;
  font-size: 1.35rem;
}

.placeholder-box {
  max-width: 520px;
  margin: 0 auto;
  padding: 32px;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
  background: #f9fafb;
  color: #4b5563;
  text-align: left;
}

.placeholder-box h3 {
  margin: 0 0 16px;
  color: #111;
}

.placeholder-box p {
  margin: 8px 0;
  font-size: 0.95rem;
}

.page-actions {
  margin-top: 32px;
}
</style>
