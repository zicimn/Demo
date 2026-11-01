<script setup lang="ts">
import type { ProviderItem } from '#shared/types/display';

// ============================================================
// 为什么把首页卡片单独抽成一个组件？
// 1. 每张卡片需要「自己」记住图标是否加载失败。若写在首页的
//    v-for 里，就得在父组件维护一个 Set<number>，很脏。
//    组件内部一个 ref 就够了，天然隔离。
// 2. 卡片样式可以和首页的网格布局分开，互不干扰。
// ============================================================

const props = defineProps<{
  provider: ProviderItem;
}>();

// 图标请求失败（404 / 不是合法图片地址）时置为 true，退回文字头像
const iconBroken = ref(false);

// ico 判空要考虑到三种「看起来有值、其实没意义」的情况：
//   null / undefined  → 数据库里没填
//   ''                → 空字符串（后端 to_index 直接透传，可能是 ''）
//   '   '             → 只有空格
// 所以统一 trim() 之后再判断长度，而不是简单写 v-if="provider.ico"。
const rawIcon = computed(() => (props.provider.ico ?? '').trim());

const showIcon = computed(() => rawIcon.value.length > 0 && !iconBroken.value);

const iconSrc = computed(() => rawIcon.value);


// 后端 ico 字段是可空的，名字也可能带空格，这里兜一层
const initial = computed(() => {
  const name = (props.provider.provider_name || '').trim();
  return name ? name.charAt(0).toUpperCase() : '?';
});
</script>

<template>
  <NuxtLink :to="`/providers/${provider.provider_code}`" class="provider-tile">
    <img
      v-if="showIcon"
      :src="iconSrc"
      :alt="`${provider.provider_name} 图标`"
      class="tile-icon"
      loading="lazy"
      decoding="async"
      @error="iconBroken = true"
    />
    <div v-else class="tile-avatar">{{ initial }}</div>

    <!-- name 变为 provider_name -->
    <h3 class="tile-name">{{ provider.provider_name }}</h3>
    <p class="tile-action">查看模型 →</p>
  </NuxtLink>
</template>

<style scoped>
.provider-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s;
}

.provider-tile:hover {
  border-color: #3b82f6;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.tile-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  object-fit: contain;
}

.tile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  border-radius: 50%;
  background: #eff6ff;
  color: #3b82f6;
  font-size: 1.5rem;
  font-weight: 700;
}

.tile-name {
  margin: 0;
  font-size: 1.1rem;
  color: #111;
}

.tile-action {
  margin: 12px 0 0;
  color: #3b82f6;
  font-size: 0.9rem;
}
</style>
