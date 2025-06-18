<template>
  <ObjectOwnerEditStepLayout>
    <v-table class="table">
      <LoaderSpinner v-if="isSaveLoading" />
      <thead>
        <tr>
          <th class="text-left">Создать подздание</th>
          <th class="text-left"></th>
        </tr>
      </thead>
      <tbody class="table-body">
        <template v-for="item in subBuildingInfo" :key="item.key">
          <tr v-if="(item.key !== 'subbuilding_optional_subtype_type' || updateSubOplSubtypeType.length > 0) && 
                   (item.key !== 'subbuilding_characteristics' || filteredCharacteristics.length > 0)">
          <td >
            <b>{{ item.title }}</b>
          </td>
          <td style="width: 400px; padding: 10px 0">
             <v-select
              v-if="item.type === 'select' && item.key === 'subbuilding_type'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              v-model="formState[item.key]"
              :items="item.items"
              @change="updateSubbuildingSubtype"
              @update:model-value="clearSelectAll"
            ></v-select>

            <v-select
              v-if="item.type === 'select' && item.key === 'subbuilding_subtype'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              v-model="formState[item.key]"
              :items="subbuildingSubtype"
              @update:modelValue="clearSelect"
            ></v-select>
            <v-select
              v-if="item.type === 'select' && item.key === 'subbuilding_optional_subtype_type'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              v-model="formState[item.key]"
              :items="updateSubOplSubtypeType"
              @update:modelValue="clearSelectOpt"
            ></v-select>
            <v-select
              v-if="item.type === 'select' && item.key === 'subbuilding_characteristics'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              v-model="formState[item.key]"
              :items="filteredCharacteristics"
              
            ></v-select>
            <v-text-field
              v-if="item.type === 'number'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              type="number"
              :rules="item.rules"
              hide-details="auto"
              variant="solo-filled"
              class="w-100"
              v-model="formState[item.key] "
            ></v-text-field>

            <v-text-field
              v-if="item.type === 'text'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              class="w-100"
              variant="solo-filled"
              clearable
              v-model="formState[item.key]"
            ></v-text-field>

            <v-text-field
                v-if="item.type === 'select' && item.key === 'subbuilding_subtype' && isOtherTypeSelected" 
                color="#f57c01"
                :loading="isSaveLoading"
                :disabled="isSaveLoading"
                :rules="item.rules"
                hide-details="auto"
                class="w-100 mt-2"
                variant="solo-filled"
                clearable
                v-model="other"
                label="Укажите тип подздания"
                placeholder="Введите свой вариант"
              ></v-text-field>

            <v-select
            v-if="item.type === 'select' && !['subbuilding_subtype', 'subbuilding_type', 'subbuilding_optional_subtype_type', 'subbuilding_characteristics', 'fire_resistance_rating', 'structural_po_class', 'stairs_classification'].includes(item.key)"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              v-model="formState[item.key]" 
              :items="item.items"
              variant="solo-filled"
              multiple
              chips
            ></v-select>

            <v-select
            v-if="item.type === 'select' && ['fire_resistance_rating', 'structural_po_class', 'stairs_classification'].includes(item.key)"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              :rules="item.rules"
              hide-details="auto"
              v-model="formState[item.key]" 
              :items="item.items"
              variant="solo-filled"
            ></v-select>

            <v-list v-if="item.type === 'list'">
              <v-list-group
                v-model="formState[item.key]"
                :value="formState[item.key]"
                :title="formState[item.key]"
                class="list-group"
              >
                <template v-slot:activator="{ props }">
                  <v-list-item
                    v-bind="props"
                    :title="formState[item.key]"
                  ></v-list-item>
                </template>
                <v-list-group
                  :multiple="false"
                  v-for="(value, index) in item.items"
                  :key="index"
                >
                  <template v-slot:activator="{ props }">
                    <v-list-item
                      v-bind="props"
                      :title="typeof value === 'object' ? value.title : value"
                    ></v-list-item>
                  </template>
                  <v-list
                    :multiple="false"
                    v-model="selectedValues[index]"
                  >
                    <v-list-item
                      :key="subIndex"
                      v-for="(subValue, subIndex) in typeof value === 'object' ? value.items : []"
                      :title="subValue"
                      @click="formState[item.key] = subValue"
                      :value="subValue"
                    ></v-list-item>
                  </v-list>
                </v-list-group>
              </v-list-group>
            </v-list>

            <v-text-field
              v-if="item.type === 'metrics'"
              color="#f57c01"
              :loading="isSaveLoading"
              :disabled="isSaveLoading"
              type="number"
              hide-details="auto"
              :rules="item.rules"
              v-model="formState[item.key]"
              class="w-100"
              variant="solo-filled"
              :suffix="item.metricType"
            ></v-text-field>

            <div v-if="item.type === 'date'">
              <v-text-field
                class="no-calendar-icon"
                type="date"
                v-model="formState[item.key]"
                variant="solo-filled"
                @update:value-ref="(value:any) => { formState[item.key] = value }"
              ></v-text-field>
            </div>
          </td>
        </tr>
      </template>
      </tbody>
      <v-card-title>Фотография подздание</v-card-title>

      <div>
        <v-file-input 
          label="Загрузите фото"
          multiple
          title="Загрузите фотоо"
          accept="image/png, image/jpeg, video/*"
          show-size
          @change="handleSubbuildingImageChange"
          :rules="escapeLadderRules"
        ></v-file-input>

        <div
          v-if="uploadedSubbuidingImages && uploadedSubbuidingImages.length > 0"
          class="uploaded-files"
        >
        <h3>Загруженные файлы:</h3>
        <div
          v-for="file in uploadedSubbuidingImages"
          :key="file.name"
          class="file-preview"
        >
        <template
           v-if="
          file.url.endsWith('.jpg') || file.url.endsWith('.jpeg') || file.url.endsWith('.png')
          "
          >
        <img
          :src="file.url"
          :alt="file.name"
          class="file-thumbnail"
        />
        </template>
        <template
        v-if="
          file.url.endsWith('.mp4') ||
          file.url.endsWith('.avi') ||
          file.url.endsWith('.quicktime')
        "
      >
      <video
        :src="file.url"
        controls
        class="file-thumbnail"
      ></video>
      </template>
      <p>{{ file.name }}</p>
      <button
        class="delete-btn"
        @click="removeSubbuildingImage(file.name)"
      >
        <v-icon>mdi-delete</v-icon>
      </button>
      </div>
      </div>
      </div>
      <v-btn
        :disabled="isSaveLoading"
        :loading="isSaveLoading"
        class="create-btn"
        @click="createSubBuilding"
      >
        Создать подздание
      </v-btn>
    </v-table>
  </ObjectOwnerEditStepLayout>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import ObjectOwnerEditStepLayout from '../UI/ObjectOwnerEditStepLayout.vue'
import { formatDateForValidation } from '@/helpers/formatTime'
import { type FunctionalPO, subBuildingInfo } from '@/utils/LongFormsStorage'
import { useSnackbarStore } from '@stores/SnackbarStore'
import {
  ObjectOfOrganizationOptionMap,
  type OrganizationObjectKeys,
  type SubBuilding,
  type SubbuildingTypes,
  SubbuildingMaintypes,
  SubbuildingOptionaltypes,
  SubbuildingOptionalMainType,
  OrganizationСharacteristics,
  SubBuildingСharacteristics,
  type OrganizationTypeObject,
} from '@/types/ObjectBuilding'
import { useSubBuildingStore } from '@/stores/SubBuildingStore'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'
import { resetForm } from '@components/forms/subBuildingResetForm'
import router from '@/router'
import { useObjectStore } from '@/stores/ObjectStore'
import { fireResistanceRating, functionalPoClass, getEnglishLightingOptions, getEnglishVentilation, getEnglishHeating, getEnglishSecurity } from '@/utils/subBuildingOptions'

const subBuildingStore = useSubBuildingStore()
const snackbarStore = useSnackbarStore()
const isSaveLoading = ref(false)
const route = useRoute()
const objectId = Number(route.params.id) as number
const selectedValues = ref<string[]>([]);
const subbuildingType = ref<SubbuildingTypes>('Здания')
const prefixSubbuildingType = ref(['Здания', 'Сооружения', 'Иные конструкции', 'Помещения'])
const emergencyLighting = ref(false)
const objectStore = useObjectStore()
const other = ref('')

const {
  uploadSubbuidingImages,
  uploadedSubbuidingImages,
  handleSubbuildingImageChange,
  subbuildingImages,
  removeSubbuildingImage
} = useObjectStore()

const escapeLadderRules = ref([
  (v: any) => !!v || 'Фото обязателен',
])


const formState = ref<Record<string, any>>({
  subbuilding_type: '',
  subbuilding_subtype: '',
  subbuilding_optional_subtype_type: '',
  subbuilding_characteristics: '',
  title: '',
  functional_purpose: '',
  floor_number: 0,
  total_floors: 0,
  building_foundation: formatDateForValidation(new Date()),
  external_walls_material: [],
  inner_walls_material: [],
  roof: [],
  stairs_material: [],
  stairs_type: [],
  stairs_classification: [],
  building_height: 0,
  area: 0,
  volume: 0,
  lighting: [],
  ventilation: [],
  heating: [],
  security: [],
  year_construction_reconstruction: 0,
  date_commissioning: formatDateForValidation(new Date()),
  fire_resistance_rating: '',
  structural_po_class: '',
  functional_po_class: [] as FunctionalPO[],
  rating: '3',
  change_functional_purpose_date: formatDateForValidation(new Date())
})

const keyToTitleMap: Record<string, string> = {}
subBuildingInfo.value.forEach((item) => {
  keyToTitleMap[item.key] = item.title
})

const isFormValid = () => {
  for (const key in formState.value) {
    if (
      key !== 'subbuilding_optional_subtype_type' && key !== 'subbuilding_characteristics' &&
      (formState.value[key] === null || 
       formState.value[key] === '' || 
       formState.value[key] === undefined)
    ) {
      const title = keyToTitleMap[key] || key // Get Russian name if available
      snackbarStore.pullSnackbar(`Поле "${title}" не заполнено`, 3000, '#d20f0d')
      return false
    }
  }
  return true
}

// 

const subbuildingSubtype = ref<string[]>([])

const updateSubbuildingSubtype = () => {
  const selectedType = formState.value.subbuilding_type
  subbuildingSubtype.value = SubbuildingMaintypes.value[selectedType] || []

  // Сбрасываем выбранное значение подтипа
  formState.value.subbuilding_subtype = ''
  formState.value.subbuilding_optional_subtype_type = ''
}


const isOtherTypeSelected = computed(() => {
  const selectedType = formState.value.subbuilding_subtype || '';
  const typePrefix = selectedType.split(' ')[0]; // Извлекаем первую часть строки
  return ['Другие', 'Прочие', 'Другой'].includes(typePrefix); // Возвращаем true для указанных вариантов, false иначе
});

const updateSubOplSubtypeType = computed(() => {
    const selectedType = formState.value.subbuilding_type as SubbuildingTypes;
    const subbuildingSubtype = formState.value.subbuilding_subtype as string; // Убедитесь, что это правильный тип
    // const selectOptionalType = formState.value.subbuilding_optional_subtype_type as string

    // Проверяем, что selectedType существует в SubbuildingOptionaltypes
    const optionalTypesForSelected = SubbuildingOptionaltypes[selectedType];

    if (optionalTypesForSelected && typeof subbuildingSubtype === 'string' && subbuildingSubtype in optionalTypesForSelected) {  
        const data = optionalTypesForSelected[subbuildingSubtype as keyof typeof optionalTypesForSelected] || [];
        if(Array.isArray(data)){
          return data;
        }else {
          return []; // Если данные не массив и не объект, возвращаем пустой массив
      }
    }

    return []; // Возвращаем пустой массив, если ничего не найдено
});

const filteredCharacteristics = computed(() => {
    if (formState.value.subbuilding_subtype in SubBuildingСharacteristics && 
        typeof formState.value.subbuilding_subtype === 'string') {
        return Object.values(SubBuildingСharacteristics[formState.value.subbuilding_subtype as keyof typeof SubBuildingСharacteristics] || []);
    }
    return [];
});

const clearSelectAll = () => {
  formState.value.subbuilding_subtype = ''
  formState.value.subbuilding_optional_subtype_type = ''
  formState.value.subbuilding_characteristics = ''
}

const clearSelect = () => {
  formState.value.subbuilding_optional_subtype_type = ''
  formState.value.subbuilding_characteristics = ''
}

const clearSelectOpt = () => {
  formState.value.subbuilding_characteristics = ''
}

const updateFireResistanceRating = (value: string) => {
  formState.value.fire_resistance_rating = value;
}

// Инициализация при загрузке
watch(
  () => formState.value.subbuilding_type, updateSubbuildingSubtype)
// 


const createSubBuilding = async () => {
  if (!isFormValid()) return

  isSaveLoading.value = true
  
  try {
    const organizationObjectKey = formState.value.organization_object as OrganizationObjectKeys

    const subBuilding: SubBuilding = {
      subbuilding_type: formState.value.subbuilding_type,
      subbuilding_subtype: isOtherTypeSelected.value ? other.value : formState.value.subbuilding_subtype,
      subbuilding_optional_subtype_type: formState.value.subbuilding_optional_subtype_type,
      subbuilding_characteristics: formState.value.subbuilding_characteristics,
      title: formState.value.title,
      functional_purpose: formState.value.functional_purpose,
      floor_number: formState.value.floor_number,
      total_floors: formState.value.total_floors,
      building_foundation: formState.value.building_foundation.toString().split('T')[0],
      external_walls_material: Array.isArray(formState.value.external_walls_material)
      ? formState.value.external_walls_material
      : [formState.value.external_walls_material],
      inner_walls_material: Array.isArray(formState.value.inner_walls_material)
      ? formState.value.inner_walls_material
      : [formState.value.inner_walls_material],
      roof: Array.isArray(formState.value.roof) ? formState.value.roof : [formState.value.roof],
      stairs_material: Array.isArray(formState.value.stairs_material)
      ? formState.value.stairs_material
      : [formState.value.stairs_material],
      stairs_type: Array.isArray(formState.value.stairs_type)
      ? formState.value.stairs_type
      : [formState.value.stairs_type],
      stairs_classification: [formState.value.stairs_classification.split('-')[0]],
      building_height: formState.value.building_height,
      area: formState.value.area,
      volume: formState.value.volume,
      lighting: Array.isArray(formState.value.lighting) ? formState.value.lighting : [formState.value.lighting],
      emergency_lighting: emergencyLighting.value,
      ventilation: Array.isArray(formState.value.ventilation)
      ? formState.value.ventilation
      : [formState.value.ventilation],
      heating: Array.isArray(formState.value.heating) ? formState.value.heating : [formState.value.heating],
      security: Array.isArray(formState.value.security)
      ? formState.value.security
      : [formState.value.security],
      year_construction_reconstruction: formState.value.year_construction_reconstruction,
      date_commissioning: formState.value.date_commissioning.toString().split('T')[0],
      fire_resistance_rating: formState.value.fire_resistance_rating,
      structural_po_class: formState.value.structural_po_class,
      functional_po_class: formState.value.functional_po_class,
      rating: formState.value.rating,
      change_functional_purpose_date: formState.value.change_functional_purpose_date
        .toString()
        .split('T')[0]
    }
    
    const subbuild = await subBuildingStore.createSubBuilding(objectId, subBuilding);
    await objectStore.uploadSubbuidingImages(objectId, subbuild.id)
    resetForm(formState, selectedValues)
    snackbarStore.pullSnackbar('Подздание создано успешно!', 3000, '#5b9271')
    router.push({ name: 'Objects' })
  } catch (err) {
    console.log(err)
    snackbarStore.pullSnackbar('Не удалось создать подздание', 3000, '#d20f0d')
  } finally {
    isSaveLoading.value = false
  }
  
}
</script>

<style lang="scss" scoped>
.thead,
.table {
  width: 100%;
}

.list-group {
  background-color: rgba(0, 0, 0, 0.035);
  border-bottom: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
  padding: 7px 0;
  border-radius: 5px;
}

.text-left {
  font-size: 24px;
  font-weight: 700 !important;
  color: #f37b01;
  text-align: left;
}

.no-calendar-icon {
  :deep(input[type="date"]::-webkit-calendar-picker-indicator) {
    display: none;
  }
}

.create-btn {
  margin: 30px 0;
  background-color: #f37b01;
  color: white;
}

.table-body {
  font-size: 18px;
}

@media only screen and (max-width: 524px) {
  .table-body {
    font-size: 14px;
  }
}
</style>
