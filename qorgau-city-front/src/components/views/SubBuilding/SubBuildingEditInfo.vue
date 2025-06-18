<script setup lang="ts">
import { useSubBuildingStore } from '@/stores/SubBuildingStore'
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSnackbarStore } from '@stores/SnackbarStore'
import {
  ObjectOfOrganizationOptionMap,
  ObjectOfOrganizationOptionReverseMap,
  type OrganizationObjectKeys,
  type SubBuilding,
  SubbuildingMaintypes,
  SubbuildingOptionaltypes,
  type SubbuildingTypes,
  SubBuildingСharacteristics
} from '@/types/ObjectBuilding'

import { subBuildingInfo } from '@/utils/LongFormsStorage'
import ObjectAvatar from '@views/Objects/objects-owner/object-card/UI/ObjectAvatar.vue'

const subBuildingStore = useSubBuildingStore()
const snackbarStore = useSnackbarStore()
const router = useRouter()

const route = useRoute()
const objectId = route.params.id as string
const subBuildingId = route.params.subBuilding as string

const showDeleteDialog = ref(false)
const loading = ref(false)

const goBack = () => {
  router.go(-1)
}

const toggleDeleteDialog = () => {
  showDeleteDialog.value = !showDeleteDialog.value
}

const updateSubBuildingStore = (key: keyof SubBuilding, subValue: any) => {
  if (key === 'subbuilding_type' || key === 'subbuilding_subtype' || key === 'functional_purpose') {
    // Обновляем строковые поля
    subBuildingStore.currentSubBuilding![key] = subValue as string;
  } else if (key === 'floor_number' || key === 'total_floors' || key === 'building_height' || key === 'area' || key === 'volume') {
    // Обновляем числовые поля
    subBuildingStore.currentSubBuilding![key] = Number(subValue);
  } else if (key === 'building_foundation' || key === 'date_commissioning' || key === 'change_functional_purpose_date') {
    // Обновляем поля с датами
    subBuildingStore.currentSubBuilding![key] = new Date(subValue);
  } else {
    // Для всех остальных полей используем общий подход
    subBuildingStore.currentSubBuilding![key] = subValue;
  }
}

const confirmDelete = async () => {
  try {
    loading.value = true
    await subBuildingStore.deleteSubBuilding(objectId, subBuildingId)
    toggleDeleteDialog()
    snackbarStore.pullSnackbar('Подздание успешно удалена', 3000, '#5b9271')
    loading.value = false
    await router.push(`/objects/edit/${objectId}`)
  } catch (err) {
    console.log(err)
    snackbarStore.pullSnackbar('Не удалось удалить подздание', 3000, '#d20f0d')
  }
}

const saveChange = (key: keyof SubBuilding) => {
  try {
    loading.value = true
    subBuildingStore.updateSubBuildingInfo(key, objectId, subBuildingId)
    subBuildingStore.toggleEditing(key)
    snackbarStore.pullSnackbar('Подздание успешно обновлено', 3000, '#5b9271')
    loading.value = false
  } catch (error) {
    loading.value = false
    console.log(error)
    snackbarStore.pullSnackbar('Не удалось обновить подздание', 3000, '#d20f0d')
  }
}

const displayFields = computed(() => {
  if (!subBuildingStore.currentSubBuilding) return {}
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { id, ...fields } = subBuildingStore.currentSubBuilding
  return fields
})

console.log("displayFields", displayFields.value)

// //

// Test N1

interface FieldInfo {
  key: string;
  title: string;
  value: string | number | Date;
  type?: string;
  items?: string[] | Record<string, any>;
  metricType?: string;
  // Добавьте другие возможные поля, которые могут быть в ваших данных
}

const getFieldInfo = (key: string): FieldInfo => {
  const foundItem = subBuildingInfo.value.find((item) => item.key === key);
  if (foundItem) {
    return foundItem as FieldInfo; // Используем явное приведение типа
  }
  return {
    key,
    title: key,
    value: '',
    type: 'text',
    items: {},
    metricType: 'metricType'
  };
}

console.log(getFieldInfo('subbuilding_subtype'))

// 

// const getFieldInfo = (key: string) => {
//   return (
//     subBuildingInfo.value.find((item) => item.key === key) || {
//       title: key,
//       type: 'text',
//       items: {},
//       metricType: 'metricType'
//     }
//   )
// }

// //

const getDisplayValue = (key: string, value: any) => {
  const fieldInfo = getFieldInfo(key)
  if (key === 'organization_object') {
    return (
      ObjectOfOrganizationOptionReverseMap[
      value as keyof typeof ObjectOfOrganizationOptionReverseMap
      ] || value
    )
  }
  if (fieldInfo.type === 'date') {
    return new Date(value).toLocaleDateString()
  }
  if (fieldInfo.type === 'metrics') {
    return `${value} ${fieldInfo.metricType}`
  }
  // if (key === 'images'){
  //   return 'this is images'
  // }
  return value
}

const currentOrganizationObject = computed({
  get: () => {
    const currentKey = subBuildingStore.currentSubBuilding!['subbuilding_type']
    return (
      ObjectOfOrganizationOptionReverseMap[
      currentKey as keyof typeof ObjectOfOrganizationOptionReverseMap
      ] || currentKey
    )
  },
  set: (val: OrganizationObjectKeys) => {
    subBuildingStore.currentSubBuilding!['subbuilding_type'] = ObjectOfOrganizationOptionMap[val]
  }
})

const subbuildingSubtype = ref<string[]>([])

const updateSubbuildingSubtype = computed(() => {
  const selectedType = subBuildingStore.currentSubBuilding!['subbuilding_type'];
  if (selectedType in SubbuildingMaintypes &&
    typeof subbuildingSubtype === 'string') {
    return Object.values(SubbuildingMaintypes[selectedType as keyof typeof SubbuildingMaintypes] || []);
  }
  return [];
});

const updateSubOplSubtypeType = computed(() => {
  const selectedType = subBuildingStore.currentSubBuilding!.subbuilding_type as SubbuildingTypes;
  const subbuildingSubtype = subBuildingStore.currentSubBuilding!.subbuilding_subtype as string;

  const optionalTypesForSelected = SubbuildingOptionaltypes[selectedType];

  if (optionalTypesForSelected && typeof subbuildingSubtype === 'string' && subbuildingSubtype in optionalTypesForSelected) {
    const data = optionalTypesForSelected[subbuildingSubtype as keyof typeof optionalTypesForSelected] || [];

    return Array.isArray(data) ? data : [];
  }

  return [];
});

const filteredCharacteristics = computed(() => {
  const subbuildingSubtype = subBuildingStore.currentSubBuilding!.subbuilding_subtype;

  if (subbuildingSubtype in SubBuildingСharacteristics &&
    typeof subbuildingSubtype === 'string') {
    return Object.values(SubBuildingСharacteristics[subbuildingSubtype as keyof typeof SubBuildingСharacteristics] || []);
  }
  return [];
});

onMounted(() => {
  subBuildingStore.getSubBuildingInfo(objectId, subBuildingId)
  console.log('subbuildingSubtype', subbuildingSubtype.value)
})
</script>

<template>
  <div class="wrapper">
    <v-container fluid class="pa-4 m-0">
      <v-card v-if="subBuildingStore.currentSubBuilding" class="sub-building-info">
        <v-card-title class="d-flex flex-column align-start">
          <v-btn variant="text" class="back-btn mb-4" prepend-icon="mdi-chevron-left" @click="goBack">
            Назад
          </v-btn>
          <h2 class="text-h4 font-weight-bold">{{ subBuildingStore.currentSubBuilding?.title }}</h2>
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col v-for="(value, key) in displayFields" :key="key" cols="12" sm="12" md="6">
              <v-card flat class="pa-4 info-card">
                <strong class="field-title">{{ getFieldInfo(key).title }}:</strong>

                <template v-if="!subBuildingStore.editingFields[key]">
                  <div v-if="key === 'images'">
                    <ObjectAvatar :images="subBuildingStore.currentSubBuilding[key]" />
                  </div>

                  <div v-else-if="Array.isArray(value)" class="d-flex justify-space-between mt-2 text-body-1">
                    <!-- Явно указываем, что value - это массив -->
                    <div>
                      <span v-for="(item, index) in value as string[]" :key="index">
                        {{ item }}<span v-if="index !== (value as string[]).length - 1">, </span>
                      </span>
                    </div>

                    <v-btn icon="mdi-pencil" rounded="lg" size="x-small" color="#24669f" class="edit-btn ml-2"
                      @click="subBuildingStore.toggleEditing(key)">
                    </v-btn>
                  </div>

                  <div v-else class="d-flex justify-space-between mt-2 text-body-1">
                    {{ getDisplayValue(key, value) }}

                    <v-btn icon="mdi-pencil" rounded="lg" size="x-small" color="#24669f" class="edit-btn ml-2"
                      @click="subBuildingStore.toggleEditing(key)">
                    </v-btn>
                  </div>
                </template>

                <template v-else>
                  <v-text-field v-if="getFieldInfo(key).type === 'text' || getFieldInfo(key).type === 'number'"
                    v-model="subBuildingStore.currentSubBuilding[key]" :type="getFieldInfo(key).type" dense outlined
                    class="mt-2"></v-text-field>

                  <v-select v-if="getFieldInfo(key).type === 'select' && getFieldInfo(key).key === 'subbuilding_type'"
                    v-model="subBuildingStore.currentSubBuilding.subbuilding_type"
                    :items="(getFieldInfo(key).items as any[])" dense outlined class="mt-2"></v-select>

                  {{ console.log(getFieldInfo(key).value) }}

                  <v-select v-if="getFieldInfo(key).type === 'select' && getFieldInfo(key).key === 'subbuilding_subtype'"
                    color="#f57c01" v-model="subBuildingStore.currentSubBuilding.subbuilding_subtype" dense outlined
                    class="mt-2" :items="updateSubbuildingSubtype"></v-select>
                  <v-select
                    v-if="getFieldInfo(key).type === 'select' && getFieldInfo(key).key === 'subbuilding_optional_subtype_type'"
                    color="#f57c01" v-model="subBuildingStore.currentSubBuilding.subbuilding_optional_subtype_type" dense
                    outlined class="mt-2" :items="updateSubOplSubtypeType"></v-select>
                  <v-select
                    v-if="getFieldInfo(key).type === 'select' && getFieldInfo(key).key === 'subbuilding_characteristics'"
                    v-model="subBuildingStore.currentSubBuilding.subbuilding_characteristics" dense outlined class="mt-2"
                    :items="filteredCharacteristics"></v-select>

                  <v-select
                    v-else-if="getFieldInfo(key).type === 'select' && !['subbuilding_subtype', 'subbuilding_type', 'subbuilding_optional_subtype_type', 'subbuilding_characteristics', 'fire_resistance_rating', 'structural_po_class', 'stairs_classification'].includes(getFieldInfo(key).key)"
                    v-model="subBuildingStore.currentSubBuilding[key]" :items="(getFieldInfo(key).items as any[])" dense
                    outlined class="mt-2" multiple chips></v-select>

                  <v-select
                    v-if="getFieldInfo(key).type === 'select' && ['fire_resistance_rating', 'structural_po_class', 'stairs_classification'].includes(getFieldInfo(key).key)"
                    v-model="subBuildingStore.currentSubBuilding[key]" :type="getFieldInfo(key).type"
                    :items="(getFieldInfo(key).items as any[])" dense outlined class="mt-2"></v-select>

                  <v-list v-if="getFieldInfo(key).type === 'list'">
                    <v-list-group v-model="subBuildingStore.currentSubBuilding[key]" class="list-group">
                      <template v-slot:activator="{ props }">
                        <v-list-item v-bind="props">
                          <v-list-item-title>{{
                            subBuildingStore.currentSubBuilding[key]
                          }}</v-list-item-title>
                        </v-list-item>
                      </template>
                      <v-list-group :multiple="false" v-for="(value, index) in getFieldInfo(key).items" :key="index">
                        <template v-slot:activator="{ props }">
                          <v-list-item v-bind="props">
                            <v-list-item-title>{{ value?.title }}</v-list-item-title>
                          </v-list-item>
                        </template>
                        <v-list :multiple="false">
                          <v-list-item :key="subIndex" v-for="(subValue, subIndex) in value.items"
                            @click="updateSubBuildingStore(key, subValue)" :value="subValue">
                            <v-list-item-title>{{ subValue }}</v-list-item-title>
                          </v-list-item>
                        </v-list>
                      </v-list-group>
                    </v-list-group>
                  </v-list>

                  <div v-else-if="getFieldInfo(key).type === 'date'">
                    <v-text-field class="mt-2" type="date" v-model="subBuildingStore.currentSubBuilding[key]"
                      variant="solo-filled"></v-text-field>
                  </div>

                  <div v-else-if="getFieldInfo(key).type === 'metrics'" class="d-flex align-center mt-2">
                    <v-text-field v-model="subBuildingStore.currentSubBuilding[key]" type="number" dense outlined
                      class="mr-2"></v-text-field>
                    <span>{{ getFieldInfo(key).metricType }}</span>
                  </div>

                  <div class="d-flex mt-2">
                    <v-btn color="primary" small class="mr-2" @click="saveChange(key)">
                      Сохранить
                    </v-btn>
                    <v-btn color="error" small @click="subBuildingStore.toggleEditing(key)">
                      Отмена
                    </v-btn>
                  </div>
                </template>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-btn class="delete-btn" @click="toggleDeleteDialog">
            Удалить подздание
          </v-btn>
        </v-card-actions>
      </v-card>

      <!--Delete-->
      <v-dialog v-model="showDeleteDialog" max-width="400px">
        <v-card>
          <v-card-title class="text-h5"> Подтверждение удаления </v-card-title>
          <v-card-text>
            Вы уверены, что хотите удалить это подздание? Это действие нельзя отменить.
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" @click="toggleDeleteDialog">Отмена</v-btn>
            <v-btn color="red darken-1" @click="confirmDelete" :loading="loading">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - 56px);
  overflow-y: scroll;
  background-color: #f5f5f5;
}

.field-title {
  font-size: 18px;
}

.sub-building-info {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.back-btn {
  align-self: flex-start;
  background-color: #e5e5e5;
}

.delete-btn {
  transition: 0.4s ease-in-out;
  background-color: #d50503;
  color: white;
}

.delete-btn:hover {
  background-color: #e50b0b;
}

.info-card {
  background: #fafafa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
