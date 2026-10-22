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
  <div style="background: #f9f9f9; padding: 16px; border-radius: 8px;">
    <h2>供应商信息</h2>
    <p>
      名称：{{ provider.provider_name }} ({{ provider.provider_code }})
    </p>
    <p>
      官网：
      <a
        v-if="provider.website_url"
        :href="provider.website_url"
        target="_blank"
        style="color: blue;"
      >
        {{ provider.website_url }}
      </a>
      <span v-else style="color: #999;">暂无官网</span>
    </p>
  </div>
</template>