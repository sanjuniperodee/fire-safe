<script setup lang="ts">
import MyStatementsCore from './MyStatementsCore.vue'

</script>

<template>
  <div class="wrapper">
    <MyStatementsCore />
  </div>
</template>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - 56px);
  overflow-y: scroll;
}
</style>
