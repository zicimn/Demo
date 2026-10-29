<template>
  <!--
    ⚠️ 这里是整个应用最容易踩的一个坑，务必理解：

    1. <NuxtLayout> 才是「layout 的渲染开关」。
       只有被 <NuxtLayout> 包裹的内容，才会去套 app/layouts/default.vue。
       之前这里直接写 <NuxtPage />，所以 layouts/default.vue 一次都没执行过，
       导航栏、页脚、以及 :deep(.page-container) 的卡片样式全部是死代码。

    2. <NuxtLoadingIndicator> 是 Nuxt 内置的顶部进度条。
       放在这里 = 全局生效：只要发生路由跳转或页面级数据加载，
       浏览器顶部就会有一条蓝色进度条，不用每个页面各写一遍 loading。
  -->
  <div>
    <NuxtLoadingIndicator color="#3b82f6" :height="3" :duration="1800" />

    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
