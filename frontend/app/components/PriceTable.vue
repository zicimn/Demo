<script setup lang="ts">
import type { AiModelPrice } from '#shared/types/display';

// 接收价格数组
defineProps<{
  prices: AiModelPrice[];
}>();
</script>

<template>
  <section style="margin-top: 24px;">
    <h2>定价（元 / 百万 tokens）</h2>
    <table style="border-collapse: collapse; width: 100%; text-align: left;">
      <thead>
        <tr style="background: #f5f5f5;">
          <th style="border-bottom: 2px solid #ddd; padding: 12px 8px;">价格类型</th>
          <th style="border-bottom: 2px solid #ddd; padding: 12px 8px;">时间周期</th>
          <th style="border-bottom: 2px solid #ddd; padding: 12px 8px;">价格</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in prices" :key="p.id">
          <td style="border-bottom: 1px solid #eee; padding: 12px 8px;">{{ p.price_type }}</td>
          <td style="border-bottom: 1px solid #eee; padding: 12px 8px;">
            <span :style="{ color: p.time_period === 'peak' ? 'red' : 'green' }">
              {{ p.time_period }}
            </span>
          </td>
          <td style="border-bottom: 1px solid #eee; padding: 12px 8px; font-weight: bold;">
            ¥ {{ p.price }}
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>