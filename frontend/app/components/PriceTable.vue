<script setup lang="ts">
import type { AiModelPrice } from '#shared/types/display';

// 接收价格数组
defineProps<{
  prices: AiModelPrice[];
}>();

// 后端 time_period 实际出现三种值：peak / off_peak / standard，
// 原来只判断「是不是 peak」，导致 standard 一律被染成绿色，
// 看起来像「便宜时段」，语义是错的。这里按三种值分别处理。
const periodStyle: Record<string, { text: string; color: string }> = {
  peak: { text: '高峰', color: '#dc2626' },
  off_peak: { text: '低谷', color: '#059669' },
  standard: { text: '标准', color: '#6b7280' },
};

function period(timePeriod: string) {
  return periodStyle[timePeriod] ?? { text: timePeriod, color: '#6b7280' };
}

// price_type 同理：input_cache_hit / input_cache_miss / output 直接显示太生硬
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

.price-table .num {
  text-align: right;
}

.price-value {
  font-weight: 600;
  white-space: nowrap;
}
</style>
