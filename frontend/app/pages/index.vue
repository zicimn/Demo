<script setup lang="ts">
import type { ApiResponse, ProviderItem } from '#shared/types/display';

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

/** 搜索关键词，空串表示不筛选。 */
const keyword = ref('');

/**
 * 按关键词过滤后的列表。
 *
 * 使用 computed 而非 watch + 手动赋值：computed 具备惰性求值、结果缓存
 * 与依赖追踪，keyword 或 providers 变化时自动重算，无需维护第二份状态，
 * 也不会出现「refresh 后忘记重算」的问题。
 *
 * 目前仅匹配 provider_name：列表接口返回 id / provider_code / provider_name / ico，
 * 其中 provider_code 不在界面展示，用户实际可见且可检索的只有名称。
 */
const filteredProviders = computed(() => {
  const q = keyword.value.trim().toLowerCase();
  if (!q) {
    return providers.value;
  }
  return providers.value.filter((p) =>
    (p.provider_name ?? '').toLowerCase().includes(q),
  );
});

/** 是否有关键词，用于控制清除按钮显隐。按 trim 后长度判断，纯空格不视为有效输入。 */
const hasKeyword = computed(() => keyword.value.trim().length > 0);

/** 统一解构错误：statusCode 用于分支判断，isNetworkError 与 message 用于提示文案。 */
const { statusCode, isNetworkError, message: errorMessage } = useApiError(error);

useSeoMeta({
  title: 'AIWiki - 选择供应商',
  description: '按供应商浏览 AI 模型的能力、上下文长度与定价。',
});
</script>

<template>
  <div class="page-container">
    <h2 class="section-title">选择供应商</h2>

    <div v-if="pending" class="status-box">正在加载供应商列表…</div>

    <!--
      列表接口在「查无启用中的供应商」时返回 404（后端主动 raise NotFound）。
      该状态对前端而言等价于「无数据」，单独拦截，避免被误报为加载失败。
    -->
    <div v-else-if="error && statusCode === 404" class="status-box">
      暂无供应商数据
    </div>

    <div v-else-if="error" class="status-box">
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
      暂无供应商数据
    </div>

    <!--
      进入此分支表示后端确认存在数据。
      工具栏仅在有数据时渲染；搜索无结果的状态同样放在分支内部，
      以保证用户仍可修改或清空关键词。
    -->
    <template v-else>
      <div class="toolbar">
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

      <div v-if="filteredProviders.length === 0" class="status-box">
        没有匹配「{{ keyword.trim() }}」的供应商
      </div>

      <div v-else class="provider-grid">
        <ProviderTile
          v-for="provider in filteredProviders"
          :key="provider.id"
          :provider="provider"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
/* 搜索栏：输入框与清除按钮共用同一相对定位容器 */
.toolbar {
  position: relative;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  /* 右侧预留 40px，为清除按钮留出位置，避免文字被按钮遮挡 */
  padding: 10px 40px 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  font-size: 0.95rem;
  font-family: inherit;
  color: #111;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* 清除按钮：绝对定位到输入框右侧内部，垂直居中 */
.clear-btn {
  position: absolute;
  top: 50%;
  right: 8px;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: #e5e7eb;
  color: #4b5563;
  font-size: 1rem;
  line-height: 1;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.clear-btn:hover {
  background: #d1d5db;
  color: #111;
}

/* 自适应网格：按容器宽度自动决定列数；单张卡片的样式见 ProviderTile.vue */
.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
</style>
