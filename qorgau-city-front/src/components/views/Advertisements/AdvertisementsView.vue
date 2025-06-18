<script setup lang="ts">
import CabinetProviderLayout from '@/layouts/CabinetProviderLayout.vue'
import { ref, onMounted } from 'vue'
import { advertisementService } from '@/services/advertisements.service'
import AdvertisementCard from './AdvertisementCard.vue'
import { type Advertisement } from '@/types/Advertisements'
import { useRouter } from 'vue-router'

const advertisements = ref<Advertisement[]>([])
const router = useRouter()

const fetchAdvertisements = async () => {
  try {
    advertisements.value = await advertisementService.getAdvertisements()
  } catch (error) {
    console.error('Ошибка загрузки объявлений:', error)
  }
}

const goToCard = (e: any, cardId?: number) => {
  if (cardId) {
    if (e.target.className.split(' ')[0] !== 'mdi-dots-horizontal') {
      router.push('/advertisements/view/' + cardId)
    }
  }
}

onMounted(() => {
  fetchAdvertisements()
})
</script>

<template>
  <CabinetProviderLayout>
    <h1>Объявления</h1>
    <v-container>
      <div class="card-container">
        <AdvertisementCard
          v-for="advertisement in advertisements"
          @click="goToCard($event, advertisement.id)"
          :key="advertisement.id"
          :advertisement="advertisement"
        />
      </div>
    </v-container>
  </CabinetProviderLayout>
</template>

<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
</style>