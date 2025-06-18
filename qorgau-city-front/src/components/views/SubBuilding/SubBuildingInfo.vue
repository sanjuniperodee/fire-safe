<script setup lang="ts">
import { useSubBuildingStore } from '@/stores/SubBuildingStore'
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ObjectOfOrganizationOptionReverseMap } from '@/types/ObjectBuilding'

const subBuildingStore = useSubBuildingStore()
const sub = computed(() => subBuildingStore.currentSubBuilding)

const router = useRouter()
const route = useRoute()

const objectId = route.params.id as string
const subBuildingId = route.params.subBuilding as string

const goBack = () => {
  router.go(-1)
}

const getOrganizationObjectInRussian = computed(() => {
  if (sub.value?.organization_object) {
    return (
      ObjectOfOrganizationOptionReverseMap[
        sub.value.organization_object as keyof typeof ObjectOfOrganizationOptionReverseMap
      ] || sub.value.organization_object
    )
  }
  return ''
})

const formatArrayField = (array: string[] | null | undefined): string => {
  if (!array?.length) return '—'
  return array.join(', ')
}

onMounted(async () => {
  try {
    await subBuildingStore.getSubBuildingInfo(objectId, subBuildingId)
  } catch (error) {
    console.error('Failed to fetch sub-building info:', error)
  }
})
</script>

<template>
  <div class="wrapper">
    <div class="header">
      <v-btn
        class="back-btn ma-4"
        variant="text"
        prepend-icon="mdi-chevron-left"
        @click="goBack"
      >
        Назад
      </v-btn>

      <v-card-title class="px-4">{{ sub?.title }}</v-card-title>
    </div>

    <v-card-text>
      <div class="field-grid">
        <div class="field-card">
          <strong>Организация:</strong> {{ getOrganizationObjectInRussian }}
        </div>
        <div class="field-card"><strong>Название:</strong> {{ sub?.title }}</div>
        <div class="field-card">
          <strong>Функциональное назначение:</strong> {{ sub?.functional_purpose }}
        </div>
        <div class="field-card"><strong>Этаж:</strong> {{ sub?.floor_number }}</div>
        <div class="field-card"><strong>Всего этажей:</strong> {{ sub?.total_floors }}</div>
        <div class="field-card">
          <strong>Дата основания:</strong> {{ sub?.building_foundation }}
        </div>
        <div class="field-card">
          <strong>Материал внешних стен:</strong> {{ formatArrayField(sub?.external_walls_material) }}
        </div>
        <div class="field-card">
          <strong>Материал внутренних стен:</strong> {{ formatArrayField(sub?.inner_walls_material) }}
        </div>
        <div class="field-card"><strong>Крыша:</strong> {{ formatArrayField(sub?.roof) }}</div>
        <div class="field-card"><strong>Лестницы:</strong> {{ sub?.stairs }}</div>
        <div class="field-card"><strong>Высота здания:</strong> {{ sub?.building_height }}</div>
        <div class="field-card"><strong>Площадь:</strong> {{ sub?.area }}</div>
        <div class="field-card"><strong>Объем:</strong> {{ sub?.volume }}</div>
        <div class="field-card"><strong>Освещение:</strong> {{ formatArrayField(sub?.lighting) }}</div>
        <div class="field-card"><strong>Вентиляция:</strong> {{ formatArrayField(sub?.ventilation) }}</div>
        <div class="field-card"><strong>Отопление:</strong> {{ formatArrayField(sub?.heating) }}</div>
        <div class="field-card"><strong>Охрана:</strong> {{ formatArrayField(sub?.security) }}</div>
        <div class="field-card">
          <strong>Год строительства/реконструкции:</strong>
          {{ sub?.year_construction_reconstruction }}
        </div>
        <div class="field-card">
          <strong>Дата ввода в эксплуатацию:</strong> {{ sub?.date_commissioning }}
        </div>
        <div class="field-card">
          <strong>Класс огнестойкости:</strong> {{ sub?.fire_resistance_rating }}
        </div>
        <div class="field-card">
          <strong>Класс конструкционной ПО:</strong> {{ sub?.structural_po_class }}
        </div>
        <div class="field-card">
          <strong>Класс функциональной ПО:</strong>{{ sub?.functional_po_class }}
        </div>
        <div class="field-card"><strong>Рейтинг:</strong> {{ sub?.rating }}</div>
        <div class="field-card">
          <strong>Дата изменения функционального назначения:</strong>
          {{ sub?.change_functional_purpose_date }}
        </div>
        <!--        <div class="field-card"><strong>Дата создания:</strong> {{ sub?.created_at }}</div>-->
      </div>
    </v-card-text>
  </div>
</template>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - 56px);
  overflow-y: scroll;
  background-color: #f5f5f5;
}

.header {
  display: flex;
  align-items: center;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(calc(50% - 16px), 1fr));
  gap: 16px;
}

.field-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #e7e7e7;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 18px;
  font-weight: 500;
  color: #5b5b5b;
}

strong {
  font-size: 16px;
  color: black;
  display: block;
}

.back-btn {
  background-color: #e5e5e5;
  align-self: flex-start;
}

.v-card-title {
  font-weight: bold;
  font-size: 1.5rem;
}
</style>
