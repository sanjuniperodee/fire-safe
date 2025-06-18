<template>
  <v-dialog
    class="add-form-dialog"
    v-model="dialog"
    fullscreen
    :scrim="false"
    transition="dialog-bottom-transition"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        icon="mdi-plus"
        v-bind="props"
        class="text-white add-button"
        color="#f57c01"
      >
      </v-btn>
    </template>
    <v-card class="card">
      <v-toolbar
        color="#f57c01"
        class="text-white"
      >
        <v-btn
          icon
          dark
          @click="dialog = false"
          class="text-white"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title class="toolbar-title"
          >Добавить новый паспорт Пожарной Безопасности Объекта (ПБО)</v-toolbar-title
        >
      </v-toolbar>
      <div class="dialog-body w-100">
        <v-form
          ref="objectBuildingAddForm"
          class="form"
        >
          <v-card-title>Наименование организации</v-card-title>
          <div>
            <!-- <v-select
              v-model="selectedPrefix"
              :items="prefixes"
              class="select-prefix"
              outlined
              dense
              hide-details
            ></v-select>
            <v-text-field
              v-model="organizationName"
              :rules="rules"
              label="Введите наименование организации"
              placeholder="Введите наименование без 'кавычек'"
              class="text-organization-name"
              outlined
              hide-details
            ></v-text-field> -->
            <v-select
              v-model="selectedPrefix"
              class="role-select"
              :items="prefixes"
              label="Выберите"
              variant="outlined"
              @update:modelValue="syncSelectsSubTypeObject"
            ></v-select>
            <v-select
              v-if="filteredOptionalTypes.length > 0"
              v-model="organizationOptionalType"
              class="role-select"
              :items="filteredOptionalTypes"
              label="Выберите"
              variant="outlined"
            ></v-select>
            <v-select
              v-model="organizationSubType"
              class="role-select"
              :items="filteredSubTypes"
              label="Выберите"
              variant="outlined"
              @update:modelValue="syncSelectsCharacteristicsObject"
            ></v-select>
            <v-select
              v-if="filteredCharacteristics.length > 0"
              v-model="characteristics"
              class="role-select"
              :items="filteredCharacteristics"
              label="Выберите"
              variant="outlined"
            ></v-select>
            <v-text-field
              v-model="organizationName"
              :rules="rules"
              label="Введите наименование организации"
              placeholder="Введите наименование без 'кавычек'"
              class="text-organization-name"
              outlined
              hide-details
            ></v-text-field>
          </div>
          <v-card-title>ИИН / БИН</v-card-title>
          <v-text-field
            :rules="IINRules"
            v-model="IIN"
            label="Введите ИИН / БИН вашей организации"
            variant="solo-filled"
            clearable
            class="form__password"
            hide-details="auto"
          ></v-text-field>
          <v-card-title>Собственник объекта защиты</v-card-title>
          <v-text-field
            :rules="rules"
            v-model="name"
            label="ФИО"
            variant="solo-filled"
            clearable
            class="form__password"
            hide-details="auto"
          ></v-text-field>
          <!-- <v-card-title>Хотите ввести адрес здания вручную?</v-card-title> -->
          <!-- <v-switch
            color="#f57c01"
            hide-details="auto"
            v-model="addressByHand"
            :label="addressByHand ? 'Ввести адрес вручную' : 'Использовать карту'"
          ></v-switch> -->
          <!-- If couldn't found your address -->
          <v-card-title>Адрес местонахождения</v-card-title>
          <v-select
            v-model="oblast"
            label="Область"
            :rules="rules"
            :items="oblastList"
            variant="solo-filled"
            hide-details="auto"
          ></v-select>
          <v-text-field
            :rules="rules"
            v-model="city"
            label="Город"
            variant="solo-filled"
            placeholder="Пример: Астана"
            clearable
            class="form__password"
            hide-details="auto"
          ></v-text-field>
          <v-text-field
            :rules="rules"
            v-model="buildingAddress"
            label="Адрес здании"
            variant="solo-filled"
            placeholder="Пример: Сейфуллина 65/1"
            clearable
            class="form__password"
            hide-details="auto"
          ></v-text-field>

          <!-- Map -->
          <div>
            <input
              type="text"
              id="pac-input"
            />
            <MapRoot
              rootId="map-form"
              @address-selected="handleAddressSelected"
            />
          </div>
          <div
            v-show="!addressByHand"
            class="form__your-address"
          >
            <b>Адрес вашего здания: </b>
            <p>{{ mapStore.address }}</p>
          </div>
          <v-card-title>Эвакуационная лестница</v-card-title>

          <v-switch
            color="#f57c01"
            hide-details="auto"
            v-model="escapeLadder"
            :label="escapeLadder ? 'Эвакуационная лестница есть' : 'Эвакуационная лестница нет'"
          ></v-switch>

          <div v-if="escapeLadder">
            <v-file-input
              label="Загрузите фото"
              multiple
              title="Загрузите фотоо"
              accept="image/png, image/jpeg, video/*"
              show-size
              @change="handleFileChange"
              :rules="escapeLadderRules"
            ></v-file-input>

            <div
              v-if="uploadedFiles && uploadedFiles.length > 0"
              class="uploaded-files"
            >
              <h3>Загруженные файлы:</h3>
              <div
                v-for="file in uploadedFiles"
                :key="file.name"
                class="file-preview"
              >
                <template
                  v-if="
                    file.url.endsWith('.jpg') ||
                    file.url.endsWith('.jpeg') ||
                    file.url.endsWith('.png')
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
                  @click="removeFile(file.name)"
                >
                  <v-icon>mdi-delete</v-icon>
                </button>
              </div>
            </div>
          </div>
          <v-card-title>Фотография объекта</v-card-title>

          <div>
            <v-file-input
              label="Загрузите фото"
              multiple
              title="Загрузите фотоо"
              accept="image/png, image/jpeg, video/*"
              show-size
              @change="handleAvatarChange"
              :rules="escapeLadderRules"
            ></v-file-input>

            <div
              v-if="uploadedAvatar && uploadedAvatar.length > 0"
              class="uploaded-files"
            >
              <h3>Загруженные файлы:</h3>
              <div
                v-for="file in uploadedAvatar"
                :key="file.name"
                class="file-preview"
              >
                <template
                  v-if="
                    file.url.endsWith('.jpg') ||
                    file.url.endsWith('.jpeg') ||
                    file.url.endsWith('.png')
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
                  @click="removeAvatar(file.name)"
                >
                  <v-icon>mdi-delete</v-icon>
                </button>
              </div>
            </div>
          </div>

          <v-btn
            @click="() => createObject()"
            block
            class="text-white"
            style="text-transform: none"
            size="large"
            :color="isLoading ? '#FAAB51' : '#f57c01'"
            :disabled="isLoading"
            >Создать паспорт ПБО</v-btn
          >
          <LoaderSpinner v-if="isLoading" />
          <div
            v-show="!isLoading"
            class="owner__content"
          ></div>
        </v-form>
      </div>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useGoogleMaps } from '@/hooks/useGoogleMaps'
import MapRoot from '@/components/views/Map/root/MapRoot.vue'
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'
import { watch } from 'vue'
import { useMapStore } from '@/stores/MapStore'
import type { Coordinates } from '@/types/Map'
import { useUserStore } from '@/stores/UserStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import ObjectAvatar from '@views/Objects/objects-owner/object-card/UI/ObjectAvatar.vue'
import { objectService } from '@/services/object.service'
import { plus } from '@/assets/svg'
import {
  OrganizationSubTypesObject,
  OrganizationСharacteristics,
  type BuildingCoordinatesValidator,
  type CreateObjectValidator,
  type ImagesLadder,
  type OrganizationTypeObject,
  type OrgananizationSubTypeLocal
} from '@/types/ObjectBuilding'
import { useObjectStore } from '@/stores/ObjectStore'
import { oblastList } from './utils'

const objectStore = useObjectStore()
const isLoading = ref(false)
const snackbarStore = useSnackbarStore()
const mapStore = useMapStore()
const userStore = useUserStore()
const dialog = ref(false)
const addressByHand = ref(false)
const organizationName = ref('')
const selectedPrefix = ref<OrganizationTypeObject>(
  'Объекты культурно-зрелищного и спортивного назначения'
)
const prefixes = ref([
  'Объекты культурно-зрелищного и спортивного назначения',
  'Объекты административного, общественного и бытового назначения',
  'Здания детских, учебных, научно-исследовательских и проектных учреждений',
  'Здания учреждений здравоохранения, отдыха и туризма',
  'Здания предприятий торговли и общественного питания',
  'Здания коммунального хозяйства и социального обеспечения',
  'Многофункциональные здания и комплексы',
  'Жилые здания и общежития',
  'Складские здания и сооружения общего назначения',
  'Складские здания и сооружения специального назначения',
  'Промышленне предприятия',
  'Киноиндустрия',
  'Объекты связи и коммуникаций',
  'Объекты воздушного транспорта',
  'Объекты железнодорожного транспорта',
  'Объекты метрополитена',
  'Объекты морского и речного флота',
  'Объекты городского электрического транспорта',
  'Объекты автомобильного транспорта',
  'Объекты легкой промышленности',
  'Объекты пищевой промышленности',
  'Объекты лесной, целлюлозно-бумажной и деревообрабатывающей промышленность',
  'Объекты промышленности по производству строительных материалов',
  'Объекты медицинской, фармакологической и микробиологической промышленности',
  'Предприятия черной и цветной металлургии',
  'Предприятия энергетики',
  'Химическая промышленность',
  'Радиоэлектронная промышленность и приборостроение',
  'Нефтяная, нефтеперерабатывающая, нефтехимическая и газовая промышленность',
  'Объекты угольной промышленности',
  'Производственные объекты Госбанка'
])
const organizationOptionalType = ref('')
const prefixOptionalType = ref([
  'Диспансеры',
  'Лечебно-профилактические учреждения',
  'Амбулаторно-поликлинические учреждения',
  'Учреждения скорой медицинской помощи',
  'Учреждения для матерей и детей',
  'Санитарно-противоэпидемические учреждения',
  'Промышленные предприятия',
  'Магазины',
  'Здания общественного питания'
])
const organizationSubType = ref('')
const characteristics = ref('')
const escapeLadder = ref(false)

const filteredOptionalTypes = computed(() => {
  const data =
    OrganizationSubTypesObject[selectedPrefix.value as keyof typeof OrganizationSubTypesObject] ||
    []

  // Проверяем, является ли data массивом
  if (Array.isArray(data)) {
    return [] // Если это массив, возвращаем пустой массив
  } else if (data !== null && typeof data === 'object') {
    // Если это объект, возвращаем массив его ключей
    const keys = Object.keys(data)
    return keys // Возвращаем имена объектов (ключи)
  } else {
    console.warn('data не является массивом или объектом.')
    return [] // Если данные не массив и не объект, возвращаем пустой массив
  }
})

const filteredSubTypes = computed(() => {
  // Получаем данные подтипов по выбранному значению `selectedPrefix`
  const data =
    OrganizationSubTypesObject[selectedPrefix.value as keyof typeof OrganizationSubTypesObject] ||
    []

  if (Array.isArray(data)) {
    // Если `data` — массив, возвращаем его значения
    return data
  } else if (data !== null && typeof data === 'object') {
    // Если `data` — объект, получаем значения для `organizationOptionalType`
    const nestedData = data[organizationOptionalType.value as keyof typeof data]

    // Проверяем, является ли `nestedData` массивом или объектом
    if (Array.isArray(nestedData)) {
      return nestedData
    } else if (nestedData !== null && typeof nestedData === 'object') {
      return Object.values(nestedData)
    } else {
      // Если `nestedData` не массив и не объект, возвращаем пустой массив
      console.warn('nestedData не является массивом или объектом.')
      return []
    }
  } else {
    // Если данные не соответствуют массиву или объекту, возвращаем пустой массив
    console.warn('Не удалось определить подтипы: данные не являются массивом или объектом.')
    return []
  }
})
const filteredCharacteristics = computed(() => {
  if (
    organizationSubType.value in OrganizationСharacteristics &&
    typeof organizationSubType.value === 'string'
  ) {
    return Object.values(
      OrganizationСharacteristics[
        organizationSubType.value as keyof typeof OrganizationСharacteristics
      ] || []
    )
  }
  return []
})

const {
  uploadedFiles,
  uploadedAvatar,
  files,
  avatar,
  handleAvatarChange,
  handleFileChange,
  uploadAvatar,
  uploadFiles,
  removeAvatar,
  removeFile
} = useObjectStore()

const images = computed(() => objectStore.objectImages)
const file = computed(() => objectStore.objectImages)

const IIN = ref('')
const name = ref(
  `${userStore.user?.last_name} ${userStore.user?.first_name} ${userStore.user?.middle_name}`
)
const oblast = ref('Акмолинская')
const city = ref('')
const buildingAddress = ref('')

const emit = defineEmits(['close'])

const objectBuildingAddForm = ref(null)

const rules = ref([(value: any) => !!value || 'Поле обязательно'])

const isValid = async () => {
  //@ts-expect-error objectBuildingAddForm type gives automaticcaly in vuetify
  const { valid } = await objectBuildingAddForm.value!.validate()
  return valid
}

const syncSelectsSubTypeObject = () => {
  organizationOptionalType.value = ''
  organizationSubType.value = ''
  characteristics.value = ''
}

const syncSelectsCharacteristicsObject = () => {
  characteristics.value = ''
}

const IINRules = ref([
  (v: any) => !!v || 'ИИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
])

const escapeLadderRules = ref([(v: any) => !!v || 'Фото обязателен'])

const selectedAddress = ref('')

const handleAddressSelected = (address: string) => {
  selectedAddress.value = address
}

const createObject = async () => {
  const finalAddress = `${oblast.value} область, г. ${city.value}, ${buildingAddress.value}`
  let locationLatLng: Coordinates = {
    lat: mapStore.latLng ? mapStore.latLng!.lat : 0,
    lng: mapStore.latLng ? mapStore.latLng!.lng : 0
  }

  if (await isValid()) {
    const body: CreateObjectValidator = {
      organization_type: selectedPrefix.value,
      organization_optional_type: organizationOptionalType.value,
      organization_sub_type: organizationSubType.value,
      organization_characteristics: characteristics.value,
      organization_name: organizationName.value,
      iin: IIN.value,
      address: finalAddress,
      rating: '3',
      escape_ladder: escapeLadder.value
    }
    try {
      console.log(isLoading.value)
      isLoading.value = true
      const object = await objectService.createObject(body)

      const coordinatesBody: BuildingCoordinatesValidator = {
        lat: locationLatLng.lat,
        lng: locationLatLng.lng,
        building: object.id
      }

      await objectService.createCoordinates(coordinatesBody)
      await uploadFiles(object.id)
      await uploadAvatar(object.id)
      snackbarStore.pullSnackbar('Паспорт ПБО был успешно создан.', 3000, '#5b9271')
      dialog.value = false
      emit('close')
      resetForm()
      isLoading.value = false
      console.log(isLoading.value)
    } catch (error) {
      isLoading.value = false
      console.error('Ошибка создания ПБО:', error)
      snackbarStore.pullSnackbar('Неудалось создать ваш паспорт ПБО.', 3000, '#d20f0d')
    }
  }
}

const resetForm = () => {
  organizationName.value = ''
  IIN.value = ''
  city.value = ''
  buildingAddress.value = ''
  selectedPrefix.value = 'Объекты культурно-зрелищного и спортивного назначения'
  organizationOptionalType.value = ''
  organizationSubType.value = ''
  characteristics.value = ''
  escapeLadder.value = false
  oblast.value = 'Акмолинская'
}

watch(dialog, async () => {
  if (dialog.value) {
    name.value = `${userStore.user?.last_name} ${userStore.user?.first_name} ${userStore.user?.middle_name}`
    const { allowClicking, placeOnUserLocation } = await useGoogleMaps('map-form', {
      lng: 71.43,
      lat: 51.128
    })
    allowClicking()
    placeOnUserLocation()
  }
})

const oblastByPostcode: { [key: string]: string } = {
  '010000': 'Акмолинская',
  '020000': 'Акмолинская',
  '030000': 'Актюбинская',
  '040000': 'Алматинская',
  '050000': 'Алматинская',
  '060000': 'Атырауская',
  '070000': 'Западно-Казахстанская',
  '080000': 'Жамбылская',
  '090000': 'Костанайская',
  '100000': 'Карагандинская',
  '110000': 'Мангистауская',
  '120000': 'Туркестанская',
  '130000': 'Павлодарская',
  '140000': 'Северо-Казахстанская',
  '150000': 'Восточно-Казахстанская',
  '160000': 'Южно Казакстан'
}

watch(
  () => mapStore.address,
  (newAddress) => {
    if (!newAddress) return

    try {
      const addressParts = newAddress.split(',').map((part) => part.trim())

      if (addressParts[0]) {
        buildingAddress.value = addressParts[0]
      }

      if (addressParts[1]) {
        const cityParts = addressParts[1].split(' ')
        city.value = cityParts[0]

        const postcode = cityParts.find((part) => /^\d{6}$/.test(part))

        if (postcode && oblastByPostcode[postcode]) {
          oblast.value = oblastByPostcode[postcode]
        } else {
          // Fallback для Астаны и Алматы, если индекс не найден
          if (city.value === 'Астана') {
            oblast.value = 'Акмолинская'
          } else if (city.value === 'Алматы') {
            oblast.value = 'Алматинская'
          }
        }
      }
    } catch (error) {
      console.error('Error parsing address:', error)
    }
  }
)
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  height: 60px;
  min-height: 0 !important;
}

.select-prefix {
  flex: 0 0 150px;
}

.text-organization-name {
  flex-grow: 1;
}

.v-card-title {
  padding: 0 !important;
  margin-top: 1em;
}

.add-button {
  position: fixed;
  z-index: 999;
  bottom: 71px;
  right: 15px;
}

.add-form-dialog {
  font-family: 'Overpass', sans-serif;
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden !important;
}

.dialog-body {
  overflow-y: scroll !important;
  display: flex;
  justify-content: center;
  height: 100%;
}

.form {
  gap: 1em;
  display: flex;
  flex-direction: column;
  padding: 30px 0;
  width: 50%;
  height: fit-content;
}

#map-form {
  height: 500px;
  width: 100%;
}

#pac-input {
  width: 200px;
}

@media only screen and (max-width: 544px) {
  .form {
    width: 90%;
  }

  .toolbar-title {
    font-size: 14px;
  }

  .v-card-title {
    font-size: 16px;
  }
}
</style>
