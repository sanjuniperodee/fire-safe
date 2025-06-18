<template>
  <v-snackbar
    class="snack text-center"
    :color="snackbarStore.color"
    v-model="snackbarStore.isOpen"
    :timeout="snackbarStore.timeout"
  >
    {{ snackbarStore.text }}
    <template v-slot:actions>
      <v-btn
        color="#fff"
        variant="text"
        size="small"
        density="compact"
        style="text-transform: none"
        @click="() => (snackbarStore.isOpen = false)"
      >
        Закрыть
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
import { useSnackbarStore } from '@stores/SnackbarStore'

const snackbarStore = useSnackbarStore()
</script>

<style lang="scss" scoped>
.snack {
  font-family: 'Overpass', sans-serif;
}
</style>
