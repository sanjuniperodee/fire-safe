<template>
  <div style="padding-top: 10px">
    <v-card-title
      class="title"
      style="font-size: 28px; margin-bottom: 1em"
    >
      История изменений документов
    </v-card-title>
    <HistoryTable />
  </div>
</template>

<script setup lang="ts">
import HistoryTable from './history/HistoryTable.vue'
</script>

<style scoped>
.title {
  hyphens: none !important;
  text-overflow: initial !important;
  white-space: initial;
}
</style>
