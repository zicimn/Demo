<script setup lang="ts">
import type { ApiResponse, Detail } from '#shared/types/display';

const route = useRoute();
const modelId = route.params.id;

const config = useRuntimeConfig();

const { data: res, pending, error } = await useFetch<ApiResponse<Detail>>(
  `${config.public.apiBase}/models/${modelId}`
);
</script>

<template>
  <div style="max-width: 800px; margin: 0 auto;">
    <div v-if="pending" style="text-align: center; padding: 50px;">
      正在加载模型信息...
    </div>

    <div v-else-if="error">
      <p v-if="error.statusCode === 404">模型不存在</p>
      <p v-else>加载失败：{{ error.message }}</p>
      <NuxtLink to="/" style="color: #3b82f6;">← 返回首页</NuxtLink>
    </div>

    <div v-else-if="res && res.code === 200">
      <h1 style="font-size: 2rem; margin-bottom: 24px;">{{ res.data.model.display_name }}</h1>
      
      <ProviderCard :provider="res.data.provider" />
      
      <ModelInfo :model="res.data.model" />
      
      <CapabilityList :capabilities="res.data.capabilities" />
      
      <PriceTable :prices="res.data.prices" />

      <div style="margin-top: 32px;">
        <NuxtLink to="/" style="color: #3b82f6;">← 返回首页</NuxtLink>
      </div>
    </div>
  </div>
</template>