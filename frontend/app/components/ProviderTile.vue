<script setup lang="ts">
import type { ProviderItem } from '#shared/types/display';
import { providerAvatar } from '~/utils/providerAvatars';

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
  /** 可选：当前搜索关键词，用于在供应商名称中高亮命中片段 */
  query?: string;
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

/**
 * 本地品牌头像优先。
 * 分支优先级：本地头像 → 接口 ico → 首字母文字头像。
 * 本地头像走 WebP，若浏览器不支持解码会触发 error，自动落到下一级。
 */
const localAvatar = computed(() => providerAvatar(props.provider.provider_code));
const avatarBroken = ref(false);
const showAvatar = computed(
  () => localAvatar.value.length > 0 && !avatarBroken.value,
);

/** 文字头像取名称首字母；名称可能为空或含空格，兜底为 '?' */
const initial = computed(() => {
  const name = (props.provider.provider_name || '').trim();
  return name ? name.charAt(0).toUpperCase() : '?';
});

/**
 * 官网域名。
 * 直接展示完整 URL 会很长且挤，去掉协议、www 与路径后只保留主机名，
 * 例如 platform.deepseek.com —— 既能判断是不是官方站，也不占空间。
 * URL 非法时返回空串，模板用 v-if 跳过该行。
 */
const domain = computed(() => {
  const raw = (props.provider.website_url ?? '').trim();
  if (!raw) {
    return '';
  }
  try {
    return new URL(raw).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
});
</script>

<template>
  <NuxtLink :to="`/providers/${provider.provider_code}`" class="provider-tile">
    <!-- 头像三级回退：本地品牌图 → 接口 ico → 首字母 -->
    <img
      v-if="showAvatar"
      :src="localAvatar"
      :alt="`${provider.provider_name} 头像`"
      class="tile-photo"
      loading="lazy"
      decoding="async"
      @error="avatarBroken = true"
    />
    <img
      v-else-if="showIcon"
      :src="rawIcon"
      :alt="`${provider.provider_name} 图标`"
      class="tile-icon"
      loading="lazy"
      decoding="async"
      @error="iconBroken = true"
    />
    <div v-else class="tile-avatar">{{ initial }}</div>

    <h3 class="tile-name">
      <HighlightText :text="provider.provider_name" :query="query" />
    </h3>
    <!-- 展示 provider_code：让用户与实际接口标识建立对应关系 -->
    <p class="tile-code mono">{{ provider.provider_code }}</p>
    <!-- 官网域名：真实数据，帮助判断是否为官方渠道 -->
    <p v-if="domain" class="tile-domain">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18" />
        <path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18Z" />
      </svg>
      {{ domain }}
    </p>

    <span class="tile-arrow" aria-hidden="true">查看模型 →</span>
  </NuxtLink>
</template>

<style scoped>
.provider-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 24px 28px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-lg);
  background: var(--c-surface);
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.provider-tile:hover {
  border-color: #bfdbfe;
  box-shadow: var(--sh-md);
  transform: translateY(-3px);
}

/* 图标与文字头像统一为 72px，保证三级回退之间切换时布局不跳动 */
.tile-photo {
  width: 72px;
  height: 72px;
  margin-bottom: 18px;
  /* 图片本身已带圆形透明通道，这里再加圆角与描边作为双保险与外轮廓 */
  border-radius: var(--r-full);
  object-fit: cover;
  background: var(--c-surface-2);
  /* 用一圈与卡片同色的描边把头像从背景中"托"起来 */
  box-shadow: 0 0 0 3px var(--c-surface), 0 6px 18px rgba(37, 99, 235, 0.18);
}

.tile-icon {
  width: 72px;
  height: 72px;
  margin-bottom: 18px;
  border-radius: var(--r-md);
  object-fit: contain;
}

.tile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  margin-bottom: 18px;
  border-radius: var(--r-full);
  background: linear-gradient(135deg, #eff6ff, #e0eaff);
  color: var(--c-primary);
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1;
  /* 用内描边代替边框，避免改变尺寸 */
  box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.12);
}

.tile-name {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
  line-height: 1.45;
  color: var(--c-text-1);
}

.tile-code {
  margin: 3px 0 0;
  color: var(--c-text-3);
  font-size: 0.8rem;
  letter-spacing: 0.4px;
}

/* 官网域名：比 code 更弱一级，带一个小地球图标 */
.tile-domain {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  max-width: 100%;
  margin: 7px 0 0;
  padding: 2px 9px;
  border-radius: var(--r-full);
  background: var(--c-surface-2);
  color: var(--c-text-2);
  font-size: 0.74rem;
  line-height: 1.6;
}

.tile-domain svg {
  width: 11px;
  height: 11px;
  flex: 0 0 11px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.75;
}

/* 箭头文字：hover 时右移，给出可点击的方向暗示 */
.tile-arrow {
  margin-top: 16px;
  color: var(--c-primary);
  font-size: 0.92rem;
  transition: transform 0.2s ease;
}

.provider-tile:hover .tile-arrow {
  transform: translateX(4px);
}
</style>
