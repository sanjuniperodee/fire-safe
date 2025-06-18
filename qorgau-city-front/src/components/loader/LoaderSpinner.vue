<template>
  <v-progress-circular
    color="#f57c01"
    class="loader"
    indeterminate
    :size="40"
  ></v-progress-circular>
</template>

<script setup lang="ts"></script>

<style scoped>
.loader {
  position: fixed;
  top: 100px;
  left: calc(50vw - 40px);
}
</style>
