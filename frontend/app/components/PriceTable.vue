<script setup lang="ts">
import type { AiModelPrice } from '#shared/types/display';

/** 模型定价表；无数据时展示占位文案，不渲染空表格 */
defineProps<{
  prices: AiModelPrice[];
}>();

/**
 * 价格时段中文化 + 配色。
 * 后端 time_period 实际存在三种取值：peak / off_peak / standard。
 * 不能仅按「是否 peak」二分，否则 standard 会被误标为低谷色，
 * 让用户误判为价格更便宜的时段。
 */
const periodStyle: Record<string, { text: string; color: string }> = {
  peak: { text: '高峰', color: '#dc2626' },
  off_peak: { text: '低谷', color: '#059669' },
  standard: { text: '标准', color: '#6b7280' },
};

/** 取值未收录时按中性色兜底，保证表格可正常渲染 */
function period(timePeriod: string) {
  return periodStyle[timePeriod] ?? { text: timePeriod, color: '#6b7280' };
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
    <h2>定价（元 / 百万 tokens）</h2>

    <p v-if="prices.length === 0" class="muted">该模型暂未录入定价</p>

    <table v-else class="price-table">
      <thead>
        <tr>
          <th>价格类型</th>
          <th>时间周期</th>
          <th class="num">价格</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in prices" :key="p.id">
          <td>{{ priceType(p.price_type) }}</td>
          <td>
            <span :style="{ color: period(p.time_period).color }">
              {{ period(p.time_period).text }}
            </span>
          </td>
          <td class="num price-value">¥ {{ p.price }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style scoped>
.price-section {
  margin-top: 24px;
}

.price-section h2 {
  margin: 0 0 12px;
  font-size: 1.15rem;
}

.price-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.price-table th {
  padding: 10px 8px;
  border-bottom: 2px solid #ddd;
  background: #f5f5f5;
  font-size: 0.9rem;
  white-space: nowrap;
}

.price-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #eee;
  font-size: 0.95rem;
}

/* 数值列右对齐，位数不同时便于纵向比较 */
.price-table .num {
  text-align: right;
}

/* 价格不换行，避免「¥」与数字被拆到两行 */
.price-value {
  font-weight: 600;
  white-space: nowrap;
}
</style>
