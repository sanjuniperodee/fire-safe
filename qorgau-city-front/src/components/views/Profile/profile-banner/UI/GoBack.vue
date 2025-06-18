<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
const goBack = () => {
  router.go(-1)
}
</script>

<template>
  <v-btn
    variant="flat"
    style="text-transform: none; color: #fff"
    prepend-icon="mdi-chevron-left"
    color="#ff9124"
    @click="goBack"
  >
    <span style="padding-top: 4px">Назад</span>
  </v-btn>
</template>

<style scoped lang="scss"></style>
