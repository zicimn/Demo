<!--
  应用根组件。

  结构说明：
  - <NuxtLayout> 是自定义布局（app/layouts/default.vue）的渲染入口。
    若根组件中缺少该标签，布局文件不会被执行，页面将直接渲染在根节点下，
    布局内定义的导航栏、页脚与 :deep() 样式均不会生效。
  - <NuxtLoadingIndicator> 置于根节点，使路由切换与页面级数据请求共用同一条
    顶部进度条，各页面无需重复实现加载指示。
-->
<template>
  <div>
    <NuxtLoadingIndicator color="#3b82f6" :height="3" :duration="1800" />

    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
