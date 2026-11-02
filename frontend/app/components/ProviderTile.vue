<script setup lang="ts">
import type { ProviderItem } from '#shared/types/display';

/**
 * 供应商卡片（首页网格的单元格）。
 *
 * 抽成独立组件的原因：
 * 1. 每张卡片需独立记录图标加载失败状态。若置于父级 v-for 中，需在父组件
 *    额外维护 Set<id>；组件内部一个 ref 即可自然隔离。
 * 2. 卡片样式与首页网格布局解耦，两者互不影响。
 */
const props = defineProps<{
  provider: ProviderItem;
}>();

/** 图标加载失败（404 或非法图片地址）时置为 true，退回文字头像 */
const iconBroken = ref(false);

/**
 * 图标地址归一化。
 * ico 可能为 null / undefined / '' / 纯空格，四种都应视为「无图标」，
 * 因此统一 trim 后按长度判断，而非直接写 v-if="provider.ico"。
 */
const rawIcon = computed(() => (props.provider.ico ?? '').trim());

/** 仅在存在有效地址且未加载失败时展示图片 */
const showIcon = computed(() => rawIcon.value.length > 0 && !iconBroken.value);

/** 模板取值别名 */
const iconSrc = computed(() => rawIcon.value);

/** 文字头像取名称首字母；名称可能为空或含空格，兜底为 '?' */
const initial = computed(() => {
  const name = (props.provider.provider_name || '').trim();
  return name ? name.charAt(0).toUpperCase() : '?';
});
</script>

<template>
  <NuxtLink :to="`/providers/${provider.provider_code}`" class="provider-tile">
    <!-- 有可用图标则展示图片，否则回退为文字头像 -->
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

/* 图标与文字头像统一为 64px，保证切换时布局不跳动 */
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
