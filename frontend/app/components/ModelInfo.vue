<script setup lang="ts">
import type { AiModelBase } from '#shared/types/display';

// 接收父组件传过来的 model 数据
defineProps<{
  model: AiModelBase;
}>();
</script>

<template>
  <section style="margin-top: 24px;">
    <h2>模型信息</h2>
    <ul style="list-style: none; padding: 0; line-height: 1.8;">
      <li><strong>模型标识：</strong>{{ model.model_slug }}</li>
      <li><strong>模型系列：</strong>{{ model.model_family || '—' }}</li>
      <li><strong>上下文长度：</strong>{{ model.context_length_raw || '—' }}</li>
      <li><strong>最大输出：</strong>{{ model.max_output_raw || '—' }}</li>
      <li><strong>思考模式：</strong>{{ model.thinking_support }}</li>
      <li><strong>默认思考模式：</strong>{{ model.default_thinking_mode || '—' }}</li>
      <li><strong>思考模式说明：</strong>{{ model.thinking_note || '—' }}</li>
      <li><strong>并发限制：</strong>{{ model.concurrency_limit ?? '—' }}</li>
      <li><strong>描述：</strong>{{ model.description || '—' }}</li>
    </ul>
  </section>
</template>
