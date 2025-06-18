<template>
  <div class="empty-state">
    <p>{{ message }}</p>
    <img src="/no-content-available.jpg" alt="no-content-available" class="img"/>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>

<style scoped>
.img{
  width: 313px;
  height: 313px;
}
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: auto;
  padding: 2rem;
  font-size: 18px;
  color: #999;
}
</style>
