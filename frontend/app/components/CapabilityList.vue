<script setup lang="ts">
import type { AiModelCap } from '#shared/types/display';

// 接收能力数组
defineProps<{
  capabilities: AiModelCap[];
}>();

// 后端 support_status 的取值不止 supported/unsupported，
// 还有 non_thinking_only / partial / beta，直接当文案显示会很难懂。
const statusText: Record<string, string> = {
  supported: '支持',
  unsupported: '不支持',
  beta: 'Beta',
  partial: '部分支持',
  non_thinking_only: '仅非思考模式',
};

function label(status: string) {
  return statusText[status] ?? status;
}
</script>

<template>
  <section class="cap-section">
    <h2>支持能力</h2>

    <p v-if="capabilities.length === 0" class="muted">暂无已记录的能力信息</p>

    <ul v-else class="cap-list">
      <li v-for="cap in capabilities" :key="cap.id" class="cap-item">
        <div class="cap-head">
          <strong>{{ cap.cap_name }}</strong>
          <span v-if="cap.is_beta" class="cap-beta">Beta</span>
        </div>
        <div class="cap-meta">
          状态：{{ label(cap.support_status) }}
          <span v-if="cap.note"> | {{ cap.note }}</span>
        </div>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.cap-section {
  margin-top: 24px;
}

.cap-section h2 {
  margin: 0 0 12px;
  font-size: 1.15rem;
}

.cap-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.cap-item {
  padding: 8px 12px;
  border-radius: 6px;
  background: #eef2ff;
}

.cap-head {
  display: flex;
  align-items: center;
  gap: 4px;
}

.cap-beta {
  color: #d97706;
  font-size: 12px;
}

.cap-meta {
  margin-top: 4px;
  color: #6b7280;
  font-size: 12px;
}
</style>
