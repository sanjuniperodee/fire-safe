<template>
  <RouterLink :to="`/objects/edit/${route.params.id}`">
    <v-btn
      icon="mdi-pencil"
      class="text-white add-button"
      color="#f57c01"
    >
    </v-btn>
  </RouterLink>
</template>

<script lang="ts" setup>
import { useObjectStore } from '@/stores/ObjectStore'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const objectStore = useObjectStore()
const route = useRoute()

const currentColor = ref('#5b9271')

watch(
  () => objectStore.currentStep,
  () => {
    switch (objectStore.currentStep) {
      case 1:
        currentColor.value = '#5b9271'
        break
      case 2:
        currentColor.value = '#f6c640'
        break
      case 3:
        currentColor.value = '#d20f0d'
        break
    }
  }
)
</script>

<style lang="scss" scoped>
.add-button {
  position: fixed;
  z-index: 999;
  bottom: 71px;
  right: 30px;
}
</style>
