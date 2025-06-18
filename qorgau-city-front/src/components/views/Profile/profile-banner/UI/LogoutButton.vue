<template>
  <v-btn
    :loading="userStore.isLogoutLoading"
    :disabled="userStore.isLogoutLoading"
    variant="flat"
    style="text-transform: none; color: #fff"
    prepend-icon="mdi-exit-to-app"
    color="#ff9124"
    @click="
      () => {
        userStore.logout()
      }
    "
  >
    <span style="padding-top: 4px">Выйти</span>
  </v-btn>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'

const userStore = useUserStore()
</script>

<style scoped></style>
