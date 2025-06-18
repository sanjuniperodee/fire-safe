<template>
  <v-card
    @click="() => documentsStore.openDialog(button.title)"
    v-ripple
    class="card"
  >
    <v-card-title class="card__title">{{ button.title }}</v-card-title>
    <v-btn
      @click="() => documentsStore.openDialog(button.title)"
      style=""
      variant="text"
      icon="mdi-plus"
    ></v-btn>
  </v-card>
</template>

<script setup lang="ts">
import type { DocumentButton } from '../PassportDocuments.vue'
import { useDocumentsStore } from '@/stores/DocumentsStore'
defineProps<{
  button: DocumentButton
}>()

const documentsStore = useDocumentsStore()
</script>

<style lang="scss" scoped>
.add-button {
  width: 100%;
}

.card {
  margin: 0 20px;
  display: flex;
  align-items: center;
  padding: 10px;

  &__title {
    flex: 1 1 auto;
    margin-bottom: -4px;
  }
}
</style>
