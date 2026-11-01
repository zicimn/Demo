<script setup lang="ts">
import type { ApiResponse, ProviderItem } from '#shared/types/display';

const config = useRuntimeConfig();

// 后端 /api/home/ 支持 page / size，但上限是 le=100，且响应里没有 total，
// 前端无法做真正的分页。这里直接要 100 条，避免默认 size=20 时
// 供应商超过 20 个被静默截断（等后端补 total 后再换成分页器）。
const { data: res, pending, error, refresh } = await useFetch<
  ApiResponse<ProviderItem[]>
>(`${config.public.apiBase}/providers`, {
  query: { page: 1, size: 100 },
});

// 统一从这里取列表：res / data 都可能是 null，集中兜一次，模板里就不用到处写 ?
const providers = computed(() => res.value?.data ?? []);

// 搜索关键词。空串表示不筛选。ref 是 Vue 的“响应式盒子”，
// 值一变，所有读它的 computed / 模板都会自动更新。
const keyword = ref('');

// 过滤后的列表。
// 为什么用 computed 而不是 watch + 手动赋值？
//   computed 是惰性 + 缓存 + 依赖追踪：keyword 或 providers 一变自动重算，
//   不需要额外维护一份状态，也不会出现“refresh 后忘了重算”的 bug。
// 为什么只按 name 匹配？
//   首页 DTO 只有 {id, name, ico}：ico 全为 null，id 对用户不可见，
//   provider_code 列表接口没返回。name 是唯一有意义的搜索字段。
const filteredProviders = computed(() => {
  const q = keyword.value.trim().toLowerCase();
  if (!q) {
    return providers.value;
  }
  return providers.value.filter((p) =>
    (p.provider_name ?? '').toLowerCase().includes(q),
  );
});

// 是否有关键词（用于控制“清除”按钮显隐）。
// 用 trim 后的长度判断，避免用户只输入空格时按钮也冒出来。
const hasKeyword = computed(() => keyword.value.trim().length > 0);

// 把 error 拆成 statusCode / isNetworkError / 人话文案
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
      列表接口在「查不到任何启用中的供应商」时会返回 404（后端 raise NotFound）。
      对前端来说这等价于「没有数据」，不该显示成加载失败，所以单独拦一层。
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
      空数组也走这里。
      注意：这里必须用 providers（原始数据）判断，不能用 filteredProviders。
      否则后端真没数据时，会被误报成「搜索无结果」。
    -->
    <div v-else-if="providers.length === 0" class="status-box">
      暂无供应商数据
    </div>

    <!--
      走到这里说明「后端确实有数据」。
      工具栏只在有数据时显示；搜索无结果的分支也必须放在这里，
      因为用户需要能改关键词、清空关键词。
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
/* 工具栏：输入框 + 清除按钮 */
.toolbar {
  position: relative;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 12px; /* 右侧留 40px 给清除按钮 */
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

/* 清除按钮：绝对定位到输入框右侧内部 */
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

/* 网格布局；单张卡片的样式在 ProviderTile.vue 里 */
.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
</style>