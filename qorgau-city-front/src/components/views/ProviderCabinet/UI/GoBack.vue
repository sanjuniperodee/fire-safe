<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
const goBack = () => {
  router.go(-1)
}
</script>

<template>
  <v-btn
    class="btn"
    variant="flat"
    style="text-transform: none; color: black"
    prepend-icon="mdi-chevron-left"
    @click="goBack"
  >
    <span style="padding-top: 4px">Назад</span>
  </v-btn>
</template>

<style scoped lang="scss">
.btn {
  position: absolute;
  display: flex;
  align-items: center;
  top: 20px;
  left: 20px;
  background-color: #dcdcdc;
}
</style>
