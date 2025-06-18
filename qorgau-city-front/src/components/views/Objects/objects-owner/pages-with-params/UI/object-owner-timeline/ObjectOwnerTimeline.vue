<template>
  <v-timeline
    side="start"
    direction="horizontal"
  >
    <v-timeline-item
      v-for="item in items"
      :key="item.id"
      :dot-color="item.color"
      size="small"
    >
      <v-btn
        @click="objectStore.currentStep = item.id"
        :style="{
          transform: objectStore.currentStep === item.id ? 'translateY(0px)' : 'translateY(75px)'
        }"
        style="font-family: 'Overpass', sans-serif; font-size: 16px; z-index: 999"
        :value="true"
        :color="item.color"
        class="text-white navigate-button"
        :prepend-icon="item.icon"
        width="200px"
        stacked
      >
        {{ $t('step') }} {{ item.id }}
      </v-btn>
    </v-timeline-item>
  </v-timeline>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useObjectStore } from '../../../../../../../stores/ObjectStore'

const objectStore = useObjectStore()

const items = ref([
  {
    id: 1,
    color: '#5b9271',
    icon: 'mdi-information'
  },
  {
    id: 2,
    color: '#f6c640',
    icon: 'mdi-ruler'
  },
  {
    id: 3,
    color: '#d20f0d',
    icon: 'mdi-office-building'
  }
])
</script>

<style lang="scss" scoped>
@media only screen and (max-width: 704px) {
  .navigate-button {
    width: 100px !important;
    font-size: 14px !important;
  }
}

@media only screen and (max-width: 400px) {
  .navigate-button {
    width: 65px !important;
    font-size: 12px !important;
  }
}
</style>
