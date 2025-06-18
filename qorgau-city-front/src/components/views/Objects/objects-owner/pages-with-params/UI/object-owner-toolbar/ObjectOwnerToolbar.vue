<template>
  <v-toolbar
    style="transition: 0.2s"
    color="#f57c01"
    class="text-white"
  >
    <v-btn
      @click="goTo('Objects')"
      icon
      class="text-white"
    >
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <v-toolbar-title class="toolbar-title">{{
      'Паспорт Пожарной Безопасности Объекта'
    }}</v-toolbar-title>
  </v-toolbar>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goTo = (route: string) => {
  router.push({ name: route })
}
</script>

<style lang="scss" scoped>
@media only screen and (max-width: 716px) {
  .toolbar-title {
    font-size: 14px;
  }
}

@media only screen and (max-width: 538px) {
  .toolbar-title {
    line-height: normal !important;
    hyphens: none !important;
    text-overflow: initial !important;
    white-space: initial !important;
  }
}
</style>
