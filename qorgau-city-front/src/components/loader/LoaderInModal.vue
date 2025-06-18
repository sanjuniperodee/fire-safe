<template>
  <div class="loader">
    <v-progress-circular
      color="#f57c01"
      indeterminate
      :size="50"
    ></v-progress-circular>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.loader {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.3);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}
</style>
