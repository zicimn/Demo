<script setup lang="ts">
import type { AiModelCap } from '#shared/types/display';

/** 模型能力标签列表；无数据时展示占位文案，不渲染空列表 */
defineProps<{
  capabilities: AiModelCap[];
}>();

/**
 * 能力状态中文化。
 * 后端 support_status 除 supported / unsupported 外，还可能出现
 * non_thinking_only、partial、beta，直接展示英文会难以理解。
 */
const statusText: Record<string, string> = {
  supported: '支持',
  unsupported: '不支持',
  beta: 'Beta',
  partial: '部分支持',
  non_thinking_only: '仅非思考模式',
};

/** 取值未收录时原样返回，保证后端新增枚举时不丢信息 */
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
          <!-- is_beta 独立标记，避免与 support_status 的语义混淆 -->
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

/* 标签流式排布，数量较多时自动换行 */
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
