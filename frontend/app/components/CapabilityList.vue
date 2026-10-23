<script setup lang="ts">
import type { AiModelCap } from '#shared/types/display';

// 接收能力数组
defineProps<{
  capabilities: AiModelCap[];
}>();
</script>

<template>
  <section style="margin-top: 24px;">
    <h2>支持能力</h2>
    <ul style="display: flex; flex-wrap: wrap; gap: 12px; list-style: none; padding: 0;">
      <li 
        v-for="cap in capabilities" 
        :key="cap.id"
        style="background: #eef2ff; padding: 8px 12px; border-radius: 6px;"
      >
        <strong>{{ cap.cap_name }}</strong>
        <span v-if="cap.is_beta" style="color: orange; margin-left: 4px; font-size: 12px;">Beta</span>
        <div style="color: #666; font-size: 12px; margin-top: 4px;">
          状态：{{ cap.support_status }}
          <span v-if="cap.note"> | {{ cap.note }}</span>
        </div>
      </li>
    </ul>
  </section>
</template>