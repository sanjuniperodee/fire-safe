<template>
  <div class="map-parent">
    <LoaderSpinner v-if="isLoading" />
    <div class="h-100">
      <input
        v-show="!isLoading"
        id="pac-input"
        class="controls"
        type="text"
        placeholder="Найти по адресу, названию, городу..."
      />
      <MapRoot
        v-show="!isLoading"
        rootId="map"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import MapRoot from './root/MapRoot.vue'
import { useGoogleMaps } from '@/hooks/useGoogleMaps'
import type { ObjectCoordinatesType } from '@/types/Map'
import { mapService } from '@/services/map.service'
import { useUserStore } from '@/stores/UserStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'
const isLoading = ref(false)
const markers = ref<ObjectCoordinatesType[]>([])
const userStore = useUserStore()
const snackbarStore = useSnackbarStore()

onMounted(async () => {
  await userStore.getUser()
  try {
    isLoading.value = true
    markers.value = await mapService.getMarkers()
    const { addMarkers, clusterizeMarkers, placeOnUserLocation } = await useGoogleMaps(
      'map',
      { lng: 71.43051762734937, lat: 51.12842004128779 },
      markers.value
    )
    placeOnUserLocation()
    addMarkers()
    clusterizeMarkers()
    isLoading.value = false
  } catch (error) {
    // snackbarStore.pullSnackbar(
    //   'Не удалось получить паспорты ПБО. Попробуйте позже.',
    //   3000,
    //   '#d20f0d'
    // )
    isLoading.value = false
    console.log(error)
  }
})
</script>

<style scoped>
.map-parent {
  height: calc(100vh - 56px);
  background-color: #e8e8e8;
}
</style>
