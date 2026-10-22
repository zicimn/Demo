<script setup lang="ts">
const route = useRoute();
const providerId = route.params.id;
</script>

<template>
  <div class="page-container" style="text-align: center; padding: 60px 20px;">
    <h1 class="title">供应商工作台</h1>
    
    <div class="info-box">
      当前正在查看供应商 ID：<strong>{{ providerId }}</strong>
    </div>
    
    <div class="placeholder-box">
      <h3>🚧 接口开发中</h3>
      <p>后端目前还没有提供“根据供应商 ID 查询其名下所有模型”的 API 接口。</p>
      <p>一旦接口上线，这里将为你呈现属于该厂商的各类模型。</p>
    </div>

    <div style="margin-top: 32px;">
      <NuxtLink to="/" class="back-btn">← 返回首页</NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.title {
  font-size: 2rem;
  color: #111;
  margin-bottom: 24px;
}

.info-box {
  font-size: 1.2rem;
  color: #374151;
  margin-bottom: 32px;
}

.info-box strong {
  color: #3b82f6;
  font-size: 1.5rem;
}

.placeholder-box {
  background: #f3f4f6;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
  padding: 32px;
  max-width: 500px;
  margin: 0 auto;
  color: #4b5563;
}

.placeholder-box h3 {
  color: #111;
  margin-bottom: 16px;
}

.placeholder-box p {
  margin: 8px 0;
  font-size: 0.95rem;
}

.back-btn {
  display: inline-block;
  background: #3b82f6;
  color: white;
  padding: 10px 24px;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #2563eb;
}
</style>