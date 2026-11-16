<script setup lang="ts">
/**
 * 关键词高亮。
 *
 * 不使用 v-html：把文本切段后在模板里逐段渲染，命中段落用 <mark> 包裹。
 * 这样既避免了 XSS 风险，也不会破坏原有的文本节点结构，
 * 对 SSR 与搜索引擎抓取都更友好。
 */
const props = defineProps<{
  text: string;
  /** 需要高亮的关键词；为空时原样输出 */
  query?: string;
}>();

interface Segment {
  text: string;
  hit: boolean;
}

const segments = computed<Segment[]>(() => {
  const source = props.text ?? '';
  const q = (props.query ?? '').trim();
  if (!q) {
    return [{ text: source, hit: false }];
  }

  const lowerSource = source.toLowerCase();
  const lowerQ = q.toLowerCase();
  const out: Segment[] = [];
  let cursor = 0;

  while (cursor < source.length) {
    const idx = lowerSource.indexOf(lowerQ, cursor);
    if (idx === -1) {
      out.push({ text: source.slice(cursor), hit: false });
      break;
    }
    if (idx > cursor) {
      out.push({ text: source.slice(cursor, idx), hit: false });
    }
    out.push({ text: source.slice(idx, idx + lowerQ.length), hit: true });
    cursor = idx + lowerQ.length;
  }

  return out.length ? out : [{ text: source, hit: false }];
});
</script>

<template>
  <span class="hl"><template v-for="(seg, i) in segments" :key="i"
    ><mark v-if="seg.hit">{{ seg.text }}</mark
    ><template v-else>{{ seg.text }}</template></template
  ></span>
</template>

<style scoped>
.hl {
  /* 不改字重，避免高亮时行宽变化造成卡片抖动 */
  font: inherit;
}

.hl mark {
  padding: 0 1px;
  border-radius: 3px;
  background: rgba(37, 99, 235, 0.18);
  color: inherit;
  font: inherit;
}

/* 深色下的高亮底色见 main.css 第 7 节：
   scoped 内的 :global(html[..]) 后代选择器不可靠，统一走全局覆写。 */
</style>
