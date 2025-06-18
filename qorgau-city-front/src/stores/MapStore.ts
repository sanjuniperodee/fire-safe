import type { Coordinates } from '@/types/Map'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMapStore = defineStore('MapStore', () => {
  const address = ref<string>('')
  const latLng = ref<Coordinates>()
  return {
    address,
    latLng
  }
})
