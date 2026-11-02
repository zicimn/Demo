<script setup lang="ts">
import type { AiModelBase } from '#shared/types/display';

/** 模型基础信息列表；空值统一以「—」占位，保持行结构完整 */
defineProps<{
  model: AiModelBase;
}>();

/** 思考模式中文化：数据库存储英文枚举，直接展示对用户不可读 */
const thinkingText: Record<string, string> = {
  none: '不支持',
  non_thinking_only: '仅非思考模式',
  thinking_only: '仅思考模式',
  both: '两种模式都支持',
  unknown: '未知',
};

/** 默认思考模式中文化 */
const modeText: Record<string, string> = {
  thinking: '思考模式',
  non_thinking: '非思考模式',
  unknown: '未知',
};

/** 空值占位：null / undefined / 空串统一显示为「—」，避免出现空白行 */
function orDash(value: string | number | null | undefined) {
  return value === null || value === undefined || value === '' ? '—' : value;
}
</script>

<template>
  <section class="model-section">
    <h2>模型信息</h2>
    <ul class="model-list">
      <li><span class="label">模型标识</span>{{ model.model_slug }}</li>
      <li><span class="label">模型版本</span>{{ orDash(model.model_version) }}</li>
      <li><span class="label">模型系列</span>{{ orDash(model.model_family) }}</li>
      <li><span class="label">上下文长度</span>{{ orDash(model.context_length_raw) }}</li>
      <li><span class="label">最大输出</span>{{ orDash(model.max_output_raw) }}</li>
      <li>
        <span class="label">思考模式</span>
        <!-- 枚举值兜底：出现未收录的取值时原样展示，避免信息丢失 -->
        {{ thinkingText[model.thinking_support] ?? model.thinking_support }}
      </li>
      <li>
        <span class="label">默认模式</span>
        {{
          model.default_thinking_mode
            ? (modeText[model.default_thinking_mode] ?? model.default_thinking_mode)
            : '—'
        }}
      </li>
      <li><span class="label">模式说明</span>{{ orDash(model.thinking_note) }}</li>
      <li><span class="label">并发限制</span>{{ orDash(model.concurrency_limit) }}</li>
      <li><span class="label">描述</span>{{ orDash(model.description) }}</li>
    </ul>
  </section>
</template>

<style scoped>
.model-section {
  margin-top: 24px;
}

.model-section h2 {
  margin: 0 0 12px;
  font-size: 1.15rem;
}

.model-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

/* 每项一行，末项去掉分隔线避免与下方区块叠线 */
.model-list li {
  display: flex;
  gap: 12px;
  padding: 6px 0;
  border-bottom: 1px dashed #f0f0f0;
  font-size: 0.95rem;
}

.model-list li:last-child {
  border-bottom: none;
}

/* 固定宽度的标签列，使右侧各行的值起始位置对齐 */
.label {
  flex: 0 0 90px;
  color: #6b7280;
}
</style>
