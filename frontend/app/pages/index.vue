<script setup lang="ts">
import type { ApiResponse, ProviderItem } from '#shared/types/display';
import { providerAvatar } from '~/utils/providerAvatars';

const config = useRuntimeConfig();

/**
 * 供应商列表数据源。
 *
 * 该接口只返回 data 数组、不返回 total，前端无法实现真正的分页，
 * 因此一次性请求上限条数（size 上限为 100），避免默认 20 条时
 * 供应商数量超出后被静默截断。后端补充 total 后可替换为分页器。
 */
const { data: res, pending, error, refresh } = await useFetch<
  ApiResponse<ProviderItem[]>
>(`${config.public.apiBase}/providers`, {
  query: { page: 1, size: 100 },
});

/** 原始列表。res 与 data 均可能为 null，在此统一兜底，模板中无需重复判空。 */
const providers = computed(() => res.value?.data ?? []);

/** 首屏预览卡用的首字母。取真实数据，数据未到位时给字母占位 */
const previewInitialA = computed(() => {
  const name = (providers.value[0]?.provider_name ?? '').trim();
  return name ? name.charAt(0).toUpperCase() : 'A';
});

const previewInitialB = computed(() => {
  const name = (providers.value[1]?.provider_name ?? '').trim();
  return name ? name.charAt(0).toUpperCase() : 'B';
});

/** 预览卡的品牌头像；加载失败或未登记时回退为字母 */
const avatarABroken = ref(false);
const avatarBBroken = ref(false);

const avatarA = computed(() =>
  avatarABroken.value ? '' : providerAvatar(providers.value[0]?.provider_code),
);

const avatarB = computed(() =>
  avatarBBroken.value ? '' : providerAvatar(providers.value[1]?.provider_code),
);

/**
 * 搜索关键词。
 * 初值取自 URL 的 ?q=，因此搜索结果可以直接分享、刷新后也不会丢。
 */
const route = useRoute();
const keyword = ref(typeof route.query.q === 'string' ? route.query.q : '');

/** 排序方式：默认（接口顺序）/ 名称升序 / 名称降序 */
const sortOrder = ref<'default' | 'asc' | 'desc'>('default');

/**
 * 按关键词过滤 + 排序后的列表。
 *
 * 使用 computed 而非 watch + 手动赋值：computed 具备惰性求值、结果缓存
 * 与依赖追踪，关键词或列表变化时自动重算，无需维护第二份状态。
 *
 * 目前仅匹配 provider_name：列表接口返回 id / provider_code / provider_name / ico，
 * 其中 provider_code 不作为主要可读信息，用户实际可检索的是名称。
 */
const filteredProviders = computed(() => {
  const q = keyword.value.trim().toLowerCase();
  const base = q
    ? providers.value.filter((p) =>
        (p.provider_name ?? '').toLowerCase().includes(q),
      )
    : providers.value;

  if (sortOrder.value === 'default') {
    return base;
  }

  // slice 先复制：直接 sort 会原地修改 providers，影响其它派生数据
  const sorted = base.slice();
  const direction = sortOrder.value === 'asc' ? 1 : -1;
  sorted.sort(
    (a, b) =>
      direction *
      (a.provider_name ?? '').localeCompare(b.provider_name ?? '', 'zh-Hans-CN'),
  );
  return sorted;
});

/** 是否有关键词，用于控制清除按钮显隐。按 trim 后长度判断，纯空格不视为有效输入。 */
const hasKeyword = computed(() => keyword.value.trim().length > 0);

/**
 * 空结果时的建议词：优先取前三个真实供应商名，数据未到位时用占位。
 * 这些词是可点击的，点一下即填入搜索框，避免用户对着空页发呆。
 */
const suggestions = computed(() => {
  const names = providers.value
    .slice(0, 3)
    .map((p) => p.provider_name)
    .filter(Boolean);
  return names.length ? names : ['DeepSeek', 'Kimi', '通义'];
});

/**
 * 关键词同步到 URL（带防抖）。
 * 用 replace 而非 push：输入过程中的每个中间状态不该占用浏览器的回退栈，
 * 否则用户按一次「后退」只会退掉一个字。
 */
let syncTimer: ReturnType<typeof setTimeout> | null = null;
watch(keyword, (value) => {
  if (!import.meta.client) {
    return;
  }
  if (syncTimer) {
    clearTimeout(syncTimer);
  }
  syncTimer = setTimeout(() => {
    const q = value.trim();
    const nextQuery: Record<string, string> = {};
    for (const [k, v] of Object.entries(route.query)) {
      if (k !== 'q' && typeof v === 'string') {
        nextQuery[k] = v;
      }
    }
    if (q) {
      nextQuery.q = q;
    }
    navigateTo({ path: route.path, query: nextQuery }, { replace: true });
  }, 350);
});

onBeforeUnmount(() => {
  if (syncTimer) {
    clearTimeout(syncTimer);
  }
});

/* ---------------- Hero 预览卡视差 ---------------- */

/*
  鼠标在 Hero 内移动时，把指针相对中心的偏移（-0.5 ~ 0.5）写进
  CSS 变量，由样式表换算成位移。两张卡位移幅度不同，形成前后景层次。
  用 requestAnimationFrame 合并高频 mousemove，避免每像素都触发样式计算。
*/
const parallax = reactive({ x: 0, y: 0 });
let pendingX = 0;
let pendingY = 0;
let rafId = 0;

/** 尊重系统的「减少动效」偏好，直接不启用 */
function motionAllowed() {
  return (
    import.meta.client &&
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );
}

function onHeroMove(event: MouseEvent) {
  if (!motionAllowed()) {
    return;
  }
  const el = event.currentTarget as HTMLElement;
  const rect = el.getBoundingClientRect();
  pendingX = (event.clientX - rect.left) / rect.width - 0.5;
  pendingY = (event.clientY - rect.top) / rect.height - 0.5;

  if (rafId) {
    return;
  }
  rafId = requestAnimationFrame(() => {
    parallax.x = pendingX;
    parallax.y = pendingY;
    rafId = 0;
  });
}

function resetParallax() {
  if (rafId) {
    cancelAnimationFrame(rafId);
    rafId = 0;
  }
  parallax.x = 0;
  parallax.y = 0;
}

const parallaxStyle = computed(() => ({
  '--px': parallax.x.toFixed(3),
  '--py': parallax.y.toFixed(3),
}));

/* ---------------- 卡片排序 FLIP 动画 ---------------- */

/*
  FLIP：First（记录旧位置）→ Last（读新位置）→ Invert（反向位移）
  → Play（动画回零）。
  排序时 DOM 节点是被复用的，直接改顺序会「瞬移」；先反向位移再动画
  归零，视觉上就是卡片平滑滑到新位置。
*/
const gridRef = ref<HTMLElement | null>(null);

function captureRects() {
  const map = new Map<string, DOMRect>();
  const root = gridRef.value;
  if (!root) {
    return map;
  }
  root.querySelectorAll<HTMLElement>('[data-flip-key]').forEach((node) => {
    const key = node.dataset.flipKey;
    if (key) {
      map.set(key, node.getBoundingClientRect());
    }
  });
  return map;
}

function playFlip(previous: Map<string, DOMRect>) {
  const root = gridRef.value;
  if (!root) {
    return;
  }
  root.querySelectorAll<HTMLElement>('[data-flip-key]').forEach((node) => {
    const key = node.dataset.flipKey;
    const before = key ? previous.get(key) : undefined;
    if (!before) {
      return;
    }
    const after = node.getBoundingClientRect();
    const dx = before.left - after.left;
    const dy = before.top - after.top;
    if (!dx && !dy) {
      return;
    }
    // Web Animations API：不写内联样式，动画结束自动清理
    node.animate(
      [
        { transform: `translate(${dx}px, ${dy}px)` },
        { transform: 'translate(0, 0)' },
      ],
      { duration: 340, easing: 'cubic-bezier(0.22, 1, 0.36, 1)' },
    );
  });
}

// flush: 'pre' 保证在 DOM 更新前记录旧位置
watch(
  [sortOrder, keyword],
  async () => {
    if (!motionAllowed()) {
      return;
    }
    const previous = captureRects();
    await nextTick();
    playFlip(previous);
  },
  { flush: 'pre' },
);

onBeforeUnmount(() => {
  if (rafId) {
    cancelAnimationFrame(rafId);
  }
});

/** 统一解构错误：statusCode 用于分支判断，isNetworkError 与 message 用于提示文案。 */
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

useSeoMeta({
  title: 'AIWiki - 选择供应商',
  description: '按供应商浏览 AI 模型的能力、上下文长度与定价。',
});
</script>

<template>
  <div class="home">
    <!--
      首屏 Hero：通过负外边距铺满视口宽度（见 ui.css），
      内部再对齐 1320px 栅格，形成「整条渐变带」而非圆角卡片。
    -->
    <section
      v-reveal
      class="page-hero"
      @mousemove="onHeroMove"
      @mouseleave="resetParallax"
    >
      <span class="hero-orb hero-orb--1" aria-hidden="true"></span>
      <span class="hero-orb hero-orb--2" aria-hidden="true"></span>

      <div class="page-hero__inner">
        <div class="hero-content">
          <p class="eyebrow">AI Model Directory</p>
          <h1 class="page-title">按供应商<br /><em>找到合适的模型</em></h1>
          <p class="page-subtitle">
            一览各家 AI 模型的能力、上下文长度与峰谷定价。先选供应商，再挑模型，几十秒得出结论。
          </p>

          <div class="hero-actions">
            <a class="btn btn--lg" href="#provider-list">开始浏览</a>
            <span class="hero-count">
              当前收录 <strong>{{ providers.length }}</strong> 家供应商
            </span>
          </div>

          <!-- 数据条：只放能确证的信息（供应商数为真实值，定价档位为接口枚举） -->
          <div class="hero-stats">
            <div class="hero-stat">
              <strong>{{ providers.length }}</strong>
              <span>家供应商</span>
            </div>
            <div class="hero-stat">
              <strong>3</strong>
              <span>档定价时段</span>
            </div>
            <div class="hero-stat">
              <strong>Ctrl K</strong>
              <span>快速搜索</span>
            </div>
          </div>
        </div>

        <!-- 右侧预览卡：纯展示，用真实数据填充，不承担交互；随鼠标轻移 -->
        <div
          v-if="providers.length"
          class="hero-preview"
          :style="parallaxStyle"
          aria-hidden="true"
        >
          <div class="preview-card">
            <span class="preview-avatar">
              <img
                v-if="avatarA"
                :src="avatarA"
                alt=""
                aria-hidden="true"
                @error="avatarABroken = true"
              />
              <template v-else>{{ previewInitialA }}</template>
            </span>
            <div>
              <p class="preview-name">{{ providers[0].provider_name }}</p>
              <p class="preview-code">{{ providers[0].provider_code }}</p>
            </div>
            <span class="preview-badge">供应商</span>
          </div>

          <div class="preview-card preview-card--offset">
            <span class="preview-avatar preview-avatar--b">
              <img
                v-if="avatarB"
                :src="avatarB"
                alt=""
                aria-hidden="true"
                @error="avatarBBroken = true"
              />
              <template v-else>{{ previewInitialB }}</template>
            </span>
            <div>
              <p class="preview-name">
                {{ providers[1]?.provider_name ?? '更多供应商' }}
              </p>
              <p class="preview-code">{{ providers[1]?.provider_code ?? '…' }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="page-container">
      <!-- 最近查看：来自 localStorage，首屏为空时不渲染 -->
      <RecentStrip />

      <h2 id="provider-list" class="section-title">全部供应商</h2>

      <!-- 加载中：骨架屏直接预示最终卡片结构 -->
      <div v-if="pending">
        <div class="skeleton-grid">
          <div v-for="n in 6" :key="n" class="skeleton-card">
            <span class="skeleton-avatar"></span>
            <span class="skeleton-line skeleton-line--title"></span>
            <span class="skeleton-line skeleton-line--sub"></span>
          </div>
        </div>
        <p class="loading-note">正在加载供应商列表…</p>
      </div>

      <!--
        列表接口在「查无启用中的供应商」时返回 404（后端主动 raise NotFound）。
        该状态对前端而言等价于「无数据」，单独拦截，避免被误报为加载失败。
      -->
      <div v-else-if="error && statusCode === 404" class="status-box">
        <svg class="status-svg" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M3 7h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z" />
          <path d="M3 10h18" />
          <path d="M9 15h6" />
        </svg>
        暂无供应商数据
      </div>

      <div v-else-if="error" class="status-box">
        <svg class="status-svg status-svg--danger" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M12 8v5" />
          <circle cx="12" cy="16" r="0.6" fill="currentColor" stroke="none" />
          <path d="M10.3 3.9 2.6 17a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" />
        </svg>
        <p class="error-text">{{ errorMessage }}</p>
        <p v-if="isNetworkError" class="hint">
          启动后端：
          <code>uvicorn main:app --app-dir app --reload --port 8000</code>
        </p>
        <div class="btn-row">
          <button class="btn" @click="refresh()">重试</button>
        </div>
      </div>

      <!--
        接口成功但返回空数组时进入此分支。
        注意必须基于 providers（原始数据）判断，不能使用 filteredProviders，
        否则后端确实没有数据时会被误判为「搜索无结果」。
      -->
      <div v-else-if="providers.length === 0" class="status-box">
        <svg class="status-svg" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M3 7h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z" />
          <path d="M3 10h18" />
          <path d="M9 15h6" />
        </svg>
        暂无供应商数据
      </div>

      <!--
        进入此分支表示后端确认存在数据。
        工具栏仅在有数据时渲染；搜索无结果的状态同样放在分支内部，
        以保证用户仍可修改或清空关键词。
      -->
      <template v-else>
        <div class="toolbar">
          <span class="search-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-3.6-3.6" />
            </svg>
          </span>
          <input
            v-model="keyword"
            type="text"
            class="search-input"
            placeholder="搜索供应商名称，如 DeepSeek、Kimi…"
            aria-label="搜索供应商"
          />
          <button
            v-if="hasKeyword"
            type="button"
            class="clear-btn"
            aria-label="清除搜索"
            @click="keyword = ''"
          >
            ×
          </button>
        </div>

        <div class="list-tools">
          <!-- aria-live：筛选结果数量变化时，读屏用户也能听到反馈 -->
          <p class="result-line" role="status" aria-live="polite">
            <template v-if="hasKeyword">
              匹配到 <strong>{{ filteredProviders.length }}</strong> 个，共
              <strong>{{ providers.length }}</strong> 个供应商
            </template>
            <template v-else>
              共 <strong>{{ providers.length }}</strong> 个供应商
            </template>
          </p>

          <!-- 排序：纯前端派生，不产生额外请求 -->
          <div class="sort-group" role="group" aria-label="排序方式">
            <button
              type="button"
              class="sort-btn"
              :class="{ 'is-active': sortOrder === 'default' }"
              @click="sortOrder = 'default'"
            >
              默认
            </button>
            <button
              type="button"
              class="sort-btn"
              :class="{ 'is-active': sortOrder === 'asc' }"
              @click="sortOrder = 'asc'"
            >
              名称 A→Z
            </button>
            <button
              type="button"
              class="sort-btn"
              :class="{ 'is-active': sortOrder === 'desc' }"
              @click="sortOrder = 'desc'"
            >
              名称 Z→A
            </button>
          </div>
        </div>

        <div v-if="filteredProviders.length === 0" class="status-box">
          <svg class="status-svg" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.6-3.6" />
            <path d="M8.5 11h5" />
          </svg>
          没有匹配「{{ keyword.trim() }}」的供应商

          <div class="suggest-row">
            <span class="suggest-label">试试</span>
            <button
              v-for="s in suggestions"
              :key="s"
              type="button"
              class="suggest-chip"
              @click="keyword = s"
            >
              {{ s }}
            </button>
          </div>
        </div>

        <!-- 卡片错峰入场：--i 由序号注入，见 ui.css 的 fade-in -->
        <div v-else ref="gridRef" class="provider-grid">
          <ProviderTile
            v-for="(provider, i) in filteredProviders"
            :key="provider.id"
            :provider="provider"
            :query="keyword"
            :data-flip-key="String(provider.id)"
            :style="{ '--i': i }"
          />
        </div>

        <!--
          图片来源声明。
          头像为 AI 生成的装饰性示意图，并非各供应商的官方形象；
          明确写出来既避免用户误认，也降低与品牌方产生关联混淆的风险。
        -->
        <p class="avatar-note">
          供应商头像为 AI 生成的装饰示意图，不代表各供应商官方形象。
        </p>
      </template>
    </div>

    <!-- 特性区：说明这个站能回答哪三个问题 -->
    <section class="feature-grid">
      <article class="feature-card">
        <span class="feature-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 7h16M4 12h10M4 17h13" />
          </svg>
        </span>
        <h3 class="feature-title">能力逐项标注</h3>
        <p class="feature-desc">
          JSON 输出、工具调用、图像理解等能力逐条列出支持状态，含 Beta 标记，不用翻官方文档。
        </p>
      </article>

      <article class="feature-card">
        <span class="feature-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 18V6M4 18h16" />
            <path d="M8 18v-6M12 18v-9M16 18v-3" />
          </svg>
        </span>
        <h3 class="feature-title">上下文与输出直读</h3>
        <p class="feature-desc">
          上下文长度、最大输出、并发限制集中呈现，规格差异一眼可比，不必来回切标签页。
        </p>
      </article>

      <article class="feature-card">
        <span class="feature-icon">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="8" />
            <path d="M12 8v4l3 2" />
          </svg>
        </span>
        <h3 class="feature-title">峰谷定价分时对照</h3>
        <p class="feature-desc">
          按高峰 / 低谷 / 标准三档展示单价，并配相对长度条，什么时候更划算一目了然。
        </p>
      </article>
    </section>
  </div>
</template>

<style scoped>
/* 搜索栏：图标、输入框与清除按钮共用一个相对定位容器 */
.toolbar {
  position: relative;
  margin-bottom: var(--sp-3);
}

.search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  width: 18px;
  height: 18px;
  transform: translateY(-50%);
  color: var(--c-text-3);
  pointer-events: none;
  transition: color 0.18s ease;
}

.search-icon svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
}

/* 聚焦时图标同步变为主题色，强化「已进入输入状态」的反馈 */
.toolbar:focus-within .search-icon {
  color: var(--c-primary);
}

.search-input {
  width: 100%;
  /* 左右各留出图标与清除按钮的空间，避免文字被遮挡 */
  padding: 15px 50px;
  border: 1px solid var(--c-border-strong);
  border-radius: var(--r-full);
  background: var(--c-surface);
  color: var(--c-text-1);
  font-size: 1.05rem;
  font-family: inherit;
  transition: border-color 0.18s ease, box-shadow 0.18s ease,
    background-color 0.18s ease;
}

.search-input::placeholder {
  color: var(--c-text-3);
}

.search-input:focus {
  outline: none;
  border-color: var(--c-primary);
  box-shadow: 0 0 0 4px var(--c-primary-ring);
}

/* 清除按钮：绝对定位到输入框右侧内部，垂直居中 */
.clear-btn {
  position: absolute;
  top: 50%;
  right: 12px;
  width: 26px;
  height: 26px;
  padding: 0;
  transform: translateY(-50%);
  border: none;
  border-radius: var(--r-full);
  background: #eef1f5;
  color: var(--c-text-2);
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  transition: background-color 0.18s ease, color 0.18s ease;
}

.clear-btn:hover {
  background: #dfe3ea;
  color: var(--c-text-1);
}

/* 结果计数与排序共用一行：左对齐信息、右侧操作 */
.list-tools {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: var(--sp-5);
}

/* 结果计数：做成小胶囊，弱于卡片但比纯文字更有边界 */
.result-line {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 6px 15px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-full);
  background: var(--c-surface-2);
  color: var(--c-text-3);
  font-size: 0.9rem;
}

/* 前置小圆点：与 hero 的 eyebrow 同一视觉语言 */
.result-line::before {
  content: "";
  width: 5px;
  height: 5px;
  border-radius: var(--r-full);
  background: var(--c-primary);
  opacity: 0.7;
}

.result-line strong {
  color: var(--c-text-2);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

/* 排序控件：分段按钮，激活项用主题色底 */
.sort-group {
  display: inline-flex;
  padding: 3px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-full);
  background: var(--c-surface-2);
}

.sort-btn {
  padding: 6px 16px;
  border: none;
  border-radius: var(--r-full);
  background: transparent;
  color: var(--c-text-3);
  font-family: inherit;
  font-size: 0.88rem;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.18s ease, color 0.18s ease;
}

.sort-btn:hover {
  color: var(--c-text-1);
}

.sort-btn.is-active {
  background: var(--c-surface);
  color: var(--c-primary);
  font-weight: 600;
  box-shadow: var(--sh-sm);
}

/*
  自适应网格。
  用 auto-fit 而不是 auto-fill：auto-fill 会保留空轨道，3 张卡在宽屏下会
  空出一列、看起来像没加载完；auto-fit 会折叠空轨道，让现有卡片撑满整行。
*/
.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}

/* 图片来源声明：弱化到几乎只剩提示作用，不影响主视觉 */
.avatar-note {
  margin: var(--sp-5) 0 0;
  color: var(--c-text-3);
  font-size: 0.78rem;
  text-align: center;
}

/* 空结果时的建议词：可点击直接填入搜索框 */
.suggest-row {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: var(--sp-4);
}

.suggest-label {
  color: var(--c-text-3);
  font-size: 0.84rem;
}

.suggest-chip {
  padding: 5px 14px;
  border: 1px solid var(--c-border);
  border-radius: var(--r-full);
  background: var(--c-surface);
  color: var(--c-text-2);
  font-family: inherit;
  font-size: 0.84rem;
  cursor: pointer;
  transition: border-color 0.18s ease, color 0.18s ease,
    background-color 0.18s ease;
}

.suggest-chip:hover {
  border-color: var(--c-primary);
  background: var(--c-primary-weak);
  color: var(--c-primary);
}

/* 状态图标：统一 32px 描边风格 */
.status-svg {
  display: block;
  width: 32px;
  height: 32px;
  margin: 0 auto var(--sp-3);
  color: var(--c-text-3);
  fill: none;
  stroke: currentColor;
  stroke-width: 1.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.status-svg--danger {
  color: var(--c-danger);
}
</style>
