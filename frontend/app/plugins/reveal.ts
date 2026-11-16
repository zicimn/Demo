/**
 * v-reveal 指令：元素进入视口后播放一次上浮淡入。
 *
 * 之所以用指令而不是组件：不改变 DOM 结构，可以直接挂在任意已有的
 * 区块元素上，避免为了动效再包一层 wrapper 影响布局。
 *
 * 降级策略：
 * - 服务端通过 getSSRProps 返回空对象，SSR 阶段不输出任何内容；
 * - .reveal 类只在客户端挂载时添加，因此 JS 不可用时元素保持默认可见；
 * - 观察器回调里先 unobserve 再加类，动画只播放一次，不会来回抖动。
 */
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('reveal', {
    getSSRProps() {
      return {};
    },
    mounted(el: RevealTarget) {
      // 观察器不支持时直接显示，不做降级动画
      if (typeof IntersectionObserver === 'undefined') {
        return;
      }

      el.classList.add('reveal');

      const observer = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-in');
              observer.unobserve(entry.target);
            }
          }
        },
        // 底部内缩 10%：元素刚露头时先不动，避免动画被裁在视口边缘
        { rootMargin: '0px 0px -10% 0px', threshold: 0.05 },
      );

      observer.observe(el);
      // 挂在元素上，供 unmounted 钩子断开
      el.__revealObserver = observer;
    },
    unmounted(el: RevealTarget) {
      el.__revealObserver?.disconnect();
      delete el.__revealObserver;
    },
  });
});

/** 指令内部使用的元素类型，仅为承载观察器实例 */
type RevealTarget = HTMLElement & {
  __revealObserver?: IntersectionObserver;
};
