<template>
  <ObjectOwnerEditStepLayout>
    <div class="step3">
      <v-card-title
        style="font-size: 1.5vw; text-align: center; margin: 0 0 20px 0"
        class="step3__subtitle"
        >Общий рейтинг</v-card-title
      >
      <CircularProgress
        class="circular__progress"
        :percentage="progress"
      />
    </div>
    <v-tabs
      v-model="tab"
      color="#f57c01"
      style="font-family: 'Montserrat', sans-serif"
      align-tabs="center"
    >
      <v-tab
        density="compact"
        value="passport"
        class="tab"
      >
        <v-icon style="margin-right: 4px">mdi-domain</v-icon>
        <span>Система обеспечения ПБ</span>
      </v-tab>
      <v-tab
        density="compact"
        value="doc"
        class="tab"
      >
        <v-icon style="margin-right: 4px">mdi-file-document-plus</v-icon>
        <span>Создание документов</span>
      </v-tab>
      <v-tab
        density="compact"
        value="history"
        class="tab"
      >
        <v-icon style="margin-right: 4px">mdi-history</v-icon>
        <span>История</span>
      </v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item value="passport">
        <PasspostSecuritySystem />
      </v-window-item>
      <v-window-item value="doc">
        <PassportDocuments />
      </v-window-item>
      <v-window-item value="history">
        <PassportHistory />
      </v-window-item>
    </v-window>
    <!-- <PassportHistory />
    <PassportDocuments /> -->
  </ObjectOwnerEditStepLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import ObjectOwnerEditStepLayout from '../UI/ObjectOwnerEditStepLayout.vue'
import PasspostSecuritySystem from './passport/PassportSecuritySystem.vue'
import PassportHistory from './passport/PassportHistory.vue'
import PassportDocuments from './passport/PassportDocuments.vue'
import CircularProgress from '@/components/progress/circular-progress/CircularProgress.vue'
import type { RatingOption } from '@/types/ObjectBuilding'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { useObjectStore } from '@/stores/ObjectStore'
import { calculateRating } from '@/utils/constants'

const route = useRoute()
const tab = ref('passport')

const objectStore = useObjectStore()
const objectInfoStore = useObjectInfoStore()
const progress = ref(objectInfoStore.calculateGeneralProgress())

let rating = ref<RatingOption>('3')

onMounted(() => {
  const progress = ref(objectInfoStore.calculateGeneralProgress())
  rating.value = calculateRating(progress.value)
  const objectId = route.params.id as string

  try {
    objectStore.updateRating(objectId, rating.value)
  } catch (error) {
    console.error('Не удалось обновить рейтинг:', error)
  }
})
</script>

<style lang="scss" scoped>
.step3 {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  right: 10px;
  top: 80px;
  width: 17vw;
  height: auto;
  z-index: 999;
  background-color: rgba(255, 255, 255, 0.5);
  padding: 10px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
}
.tab {
  text-transform: none;
  font-weight: 700 !important;
  width: 300px;
  display: flex;
  align-items: center;

  & span {
    margin-bottom: -4px;
  }
}

@media only screen and (max-width: 1110px) {
  .tab {
    width: 160px;
    font-weight: 500 !important;
    font-size: 10px;
  }
  .step3 {
    font-size: 12px;
  }
}

@media only screen and (max-width: 634px) {
  .tab {
    width: 130px;
    font-weight: 500 !important;
    font-size: 8px;
  }
}
</style>
