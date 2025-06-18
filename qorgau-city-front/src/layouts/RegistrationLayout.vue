<script setup lang="ts">
const props = defineProps<{
  title: string,
}>()
</script>

<template>
  <div class="layout-wrapper">
    <header class="header">
      <h1 class="login-title">
        {{ props.title }}
        <span class="login-logo"></span>
      </h1>
    </header>
    <div class="login-container">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="scss">
.layout-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.header {
  height: 100px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 5px 0 rgba(0,0,0,0.3);
  z-index: 999;
}

.login-container {
  position: relative;
  flex: 1;
  width: 100%;
  overflow-y: auto;
  padding: 20px 20px 80px 20px;
}

.login-title {
  font-size: 24px;
  font-weight: 500;
  color: #333;
}

.login-logo {
  font-size: 24px;
  font-family: 'Overpass', sans-serif;
  white-space: nowrap;
  color: #FD7E14FF;
}

@media (max-width: 1200px) {
  .login-container {
    padding-bottom: 80px;
  }
}
</style>