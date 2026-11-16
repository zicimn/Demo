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

/** 已收录的状态才有独立配色，其余回退为中性灰 */
const KNOWN = ['supported', 'partial', 'non_thinking_only', 'beta', 'unsupported'];

function toneClass(status: string) {
  return KNOWN.includes(status) ? `cap--${status}` : 'cap--default';
}
</script>

<template>
  <section class="cap-section">
    <h2 class="block-title">支持能力</h2>

    <p v-if="capabilities.length === 0" class="muted">暂无已记录的能力信息</p>

    <ul v-else class="cap-list">
      <li
        v-for="cap in capabilities"
        :key="cap.id"
        class="cap-item"
        :class="toneClass(cap.support_status)"
      >
        <div class="cap-head">
          <span class="cap-dot" aria-hidden="true"></span>
          <strong class="cap-name">{{ cap.cap_name }}</strong>
          <!-- is_beta 独立标记，避免与 support_status 的语义混淆 -->
          <span v-if="cap.is_beta" class="cap-beta">Beta</span>
        </div>
        <div class="cap-meta">
          状态：{{ label(cap.support_status) }}
          <span v-if="cap.note" class="cap-note">· {{ cap.note }}</span>
        </div>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.cap-section {
  margin-top: var(--sp-6);
}

.block-title {
  margin: 0 0 var(--sp-4);
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-1);
}

/* 标签流式排布，数量较多时自动换行 */
.cap-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

/* 每个能力一张小卡：左侧圆点用当前状态色，整体保持低饱和 */
.cap-item {
  min-width: 150px;
  padding: 10px 14px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
  background: var(--c-surface);
  transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

.cap-item:hover {
  border-color: var(--c-border-strong);
  box-shadow: var(--sh-sm);
}

.cap-head {
  display: flex;
  align-items: center;
  gap: 6px;
}

.cap-dot {
  width: 7px;
  height: 7px;
  flex: 0 0 7px;
  border-radius: var(--r-full);
  background: var(--c-text-3);
}

.cap-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--c-text-1);
  line-height: 1.4;
}

.cap-beta {
  padding: 1px 6px;
  border-radius: var(--r-full);
  background: var(--c-warning-weak);
  color: var(--c-warning);
  font-size: 0.68rem;
  font-weight: 600;
  line-height: 1.5;
}

.cap-meta {
  margin-top: 4px;
  padding-left: 13px;
  color: var(--c-text-2);
  font-size: 0.78rem;
}

.cap-note {
  color: var(--c-text-3);
}

/* ---------- 状态配色 ---------- */
.cap--supported {
  border-color: #cdeadd;
  background: var(--c-success-weak);
}

.cap--supported .cap-dot {
  background: var(--c-success);
}

.cap--supported .cap-meta {
  color: var(--c-success);
}

.cap--partial .cap-dot {
  background: var(--c-primary);
}

.cap--partial .cap-meta {
  color: var(--c-primary);
}

.cap--non_thinking_only .cap-dot {
  background: #7c3aed;
}

.cap--non_thinking_only .cap-meta {
  color: #7c3aed;
}

.cap--beta {
  border-color: #f5e3c3;
  background: var(--c-warning-weak);
}

.cap--beta .cap-dot {
  background: var(--c-warning);
}

.cap--beta .cap-meta {
  color: var(--c-warning);
}

.cap--unsupported {
  background: var(--c-surface-2);
}

.cap--unsupported .cap-name,
.cap--unsupported .cap-meta {
  color: var(--c-text-3);
}

.cap--unsupported .cap-dot {
  background: #cbd5e1;
}
</style>
