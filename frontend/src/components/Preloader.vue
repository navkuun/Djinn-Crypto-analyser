<template>
  <transition name="fade">
    <div v-if="show" class="preloader">
      <div class="logo p-d-flex p-ai-center p-jc-center p-mb-3">
        <img src="../assets/Djinn.png" />
      </div>
      <div class="p-d-inline-block"></div>
      <ProgressSpinner strokeWidth="8" fill="var(--surface-ground)" />
      <!-- <ProgressSpinner
        class="p-my-6 p-ml-3"
        height="20"
        style="width: 100px; height: 100"
        strokeWidth="8"
        fill="var(--surface-ground)"
        animationDuration="1s"
      /> -->
    </div>
  </transition>
</template>
<script>
export default {
  name: "preloader",
  data() {
    return {
      show: true,
    };
  },
  mounted() {
    if (this.show) this.showToggle();
  },
  methods: {
    showToggle() {
      setTimeout(() => {
        this.show = false;
      }, 1000);
    },
  },
};
</script>

<style lang="sass" scoped>
.preloader
  display: flex
  flex-direction: column
  align-items: center
  justify-content: center
  position: absolute
  width: 100%
  height: 100%
  background-color: white
  z-index: 9999
  .logo
    width: 12.5rem
    height: 12.5rem
    background-repeat: no-repeat
    p
      margin-top: 1rem
    .circles
      display: flex
      margin-top: 1rem
      .circle
        width: 1.5rem
        height: 1.5rem
        margin: .75rem
        border-radius: 50%
        background-color: blue
        animation-name: scaleIn
        animation-duration: .7s
        transform: scale(0)
        &:nth-child(1)
          animation-delay: 0s
          &:nth-child(2)
            animation-delay: .05s
            &:nth-child(3)
              animation-delay: .1s
            &:nth-child(4)
              animation-delay: .15s
            &:nth-child(5)
              animation-delay: .2s
</style>
