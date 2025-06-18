<template>
  <div class="step-layout">
    <slot />
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss" scoped>
.step-layout {
  width: 80%;
}
@media only screen and (max-width: 1104px) {
  .step-layout {
    width: 95%;
  }
}
</style>
