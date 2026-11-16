<script setup lang="ts">
import type { AiModelPrice } from '#shared/types/display';

/** 模型定价表；无数据时展示占位文案，不渲染空表格 */
const props = defineProps<{
  prices: AiModelPrice[];
}>();

/**
 * 价格条归一化基准：取本表最大价格。
 * 用相对长度而非绝对刻度，避免不同模型的量级差异导致所有条都贴边。
 */
const maxPrice = computed(() => {
  const values = props.prices.map((p) => Number(p.price) || 0);
  return values.length ? Math.max(...values) : 0;
});

/** 价格条宽度百分比；基准为 0 时返回 0，避免除零 */
function barWidth(price: number | string) {
  const v = Number(price) || 0;
  if (!maxPrice.value) {
    return '0%';
  }
  // 下限 4%，保证极低价格仍有一条可见的短条
  return `${Math.max((v / maxPrice.value) * 100, 4)}%`;
}

/** 价格条配色跟随时段：高峰红、低谷绿、其余为主题色 */
function barClass(period: string) {
  if (period === 'peak') {
    return 'is-peak';
  }
  if (period === 'off_peak') {
    return 'is-offpeak';
  }
  return '';
}

/**
 * 价格时段中文化。
 * 后端 time_period 实际存在三种取值：peak / off_peak / standard。
 * 不能仅按「是否 peak」二分，否则 standard 会被误标为低谷色，
 * 让用户误判为价格更便宜的时段。
 */
const periodText: Record<string, string> = {
  peak: '高峰',
  off_peak: '低谷',
  standard: '标准',
};

/** 取值未收录时原样返回，配色回退为中性 */
function periodLabel(period: string) {
  return periodText[period] ?? period;
}

function periodClass(period: string) {
  return periodText[period] ? `period--${period}` : 'period--default';
}

/** 价格类型中文化：input_cache_hit / input_cache_miss / output 等 */
const priceTypeText: Record<string, string> = {
  input_cache_hit: '输入（缓存命中）',
  input_cache_miss: '输入（缓存未命中）',
  output: '输出',
};

function priceType(type: string) {
  return priceTypeText[type] ?? type;
}
</script>

<template>
  <section class="price-section">
    <h2 class="block-title">
      定价
      <span class="unit">元 / 百万 tokens</span>
    </h2>

    <p v-if="prices.length === 0" class="muted">该模型暂未录入定价</p>

    <div v-else class="table-wrap">
      <table class="price-table">
        <thead>
          <tr>
            <th>价格类型</th>
            <th>时间周期</th>
            <th class="num">价格</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in prices" :key="p.id">
            <td class="type-cell">{{ priceType(p.price_type) }}</td>
            <td>
              <span class="period" :class="periodClass(p.time_period)">
                {{ periodLabel(p.time_period) }}
              </span>
            </td>
            <td class="num price-value">
              <span class="currency">¥</span>{{ p.price }}
              <!-- 价格条：用相对长度直观呈现同表内的价格高低 -->
              <span class="mini-bar" aria-hidden="true">
                <i
                  :class="barClass(p.time_period)"
                  :style="{ width: barWidth(p.price) }"
                ></i>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.price-section {
  margin-top: var(--sp-6);
}

.block-title {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin: 0 0 var(--sp-4);
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-1);
}

.unit {
  color: var(--c-text-3);
  font-size: 0.74rem;
  font-weight: 400;
}

/* 圆角需要 overflow 裁剪，故表格外包一层容器 */
.table-wrap {
  overflow: hidden;
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
}

.price-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.price-table th {
  padding: 10px 14px;
  border-bottom: 1px solid var(--c-border);
  background: var(--c-surface-2);
  color: var(--c-text-2);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.price-table td {
  padding: 11px 14px;
  border-bottom: 1px solid var(--c-border);
  font-size: 0.88rem;
  color: var(--c-text-1);
}

.price-table tbody tr:last-child td {
  border-bottom: none;
}

/* 斑马纹：隔行浅底，长表格更易横向对齐视线 */
.price-table tbody tr:nth-child(even) {
  background: #fbfcfe;
}

.price-table tbody tr:hover {
  background: var(--c-primary-weak);
}

.type-cell {
  color: var(--c-text-2);
}

/* 时段胶囊：用底色而非纯文字色区分，弱化后更耐看 */
.period {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--r-full);
  font-size: 0.76rem;
  font-weight: 500;
  line-height: 1.7;
}

.period--peak {
  background: var(--c-danger-weak);
  color: var(--c-danger);
}

.period--off_peak {
  background: var(--c-success-weak);
  color: var(--c-success);
}

.period--standard,
.period--default {
  background: var(--c-surface-2);
  color: var(--c-text-2);
}

/* 数值列右对齐并使用等宽数字，位数不同时也能对齐 */
.price-table .num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.price-value {
  font-weight: 600;
  white-space: nowrap;
}

.currency {
  margin-right: 2px;
  color: var(--c-text-3);
  font-size: 0.8rem;
  font-weight: 400;
}
</style>
