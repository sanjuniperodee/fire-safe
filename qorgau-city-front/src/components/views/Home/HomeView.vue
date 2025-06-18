<template>
  <div></div>
</template>

<script setup lang="ts">
import router from '@/router'
import { useUserStore } from '@/stores/UserStore'
import { onMounted } from 'vue'

const userStore = useUserStore()

onMounted(async () => {
  await userStore.getUser()
  if (localStorage.getItem('token')) {
    router.push({ name: 'Map' })
    return
  }
})
</script>

<style scoped></style>
