<script setup lang="ts">
import type { AiModelBase } from '#shared/types/display';

/** 模型基础信息列表；空值统一以「—」占位，保持结构完整 */
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

/** 空值占位：null / undefined / 空串统一显示为「—」，避免出现空白项 */
function orDash(value: string | number | null | undefined) {
  return value === null || value === undefined || value === '' ? '—' : value;
}
</script>

<template>
  <section class="model-section">
    <h2 class="block-title">模型信息</h2>

    <dl class="info-grid">
      <div class="info-item">
        <dt>模型标识</dt>
        <dd class="mono">{{ model.model_slug }}</dd>
      </div>
      <div class="info-item">
        <dt>模型版本</dt>
        <dd>{{ orDash(model.model_version) }}</dd>
      </div>
      <div class="info-item">
        <dt>模型系列</dt>
        <dd>{{ orDash(model.model_family) }}</dd>
      </div>
      <div class="info-item">
        <dt>上下文长度</dt>
        <dd>{{ orDash(model.context_length_raw) }}</dd>
      </div>
      <div class="info-item">
        <dt>最大输出</dt>
        <dd>{{ orDash(model.max_output_raw) }}</dd>
      </div>
      <div class="info-item">
        <dt>思考模式</dt>
        <!-- 枚举值兜底：出现未收录的取值时原样展示，避免信息丢失 -->
        <dd>{{ thinkingText[model.thinking_support] ?? model.thinking_support }}</dd>
      </div>
      <div class="info-item">
        <dt>默认模式</dt>
        <dd>
          {{
            model.default_thinking_mode
              ? (modeText[model.default_thinking_mode] ?? model.default_thinking_mode)
              : '—'
          }}
        </dd>
      </div>
      <div class="info-item">
        <dt>并发限制</dt>
        <dd>{{ orDash(model.concurrency_limit) }}</dd>
      </div>
      <div class="info-item">
        <dt>模式说明</dt>
        <dd>{{ orDash(model.thinking_note) }}</dd>
      </div>
      <!-- 描述可能较长，独占一行 -->
      <div class="info-item info-item--wide">
        <dt>描述</dt>
        <dd>{{ orDash(model.description) }}</dd>
      </div>
    </dl>
  </section>
</template>

<style scoped>
.model-section {
  margin-top: var(--sp-6);
}

/* 子区块标题：比页面主标题弱一级，仅用字重与间距区分 */
.block-title {
  margin: 0 0 var(--sp-4);
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-1);
}

/* 字段网格：窄屏单列、宽屏双列，标签在值上方 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--sp-3);
  margin: 0;
}

.info-item {
  padding: 12px 14px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
  background: var(--c-surface-2);
  transition: border-color 0.18s ease, background-color 0.18s ease;
}

.info-item:hover {
  border-color: var(--c-border-strong);
  background: var(--c-surface);
}

.info-item--wide {
  grid-column: 1 / -1;
}

.info-item dt {
  margin-bottom: 4px;
  color: var(--c-text-3);
  font-size: 0.76rem;
  letter-spacing: 0.2px;
}

.info-item dd {
  margin: 0;
  color: var(--c-text-1);
  font-size: 0.92rem;
  line-height: 1.55;
  /* 长标识串允许在任意位置换行，避免撑破卡片 */
  word-break: break-word;
}
</style>
