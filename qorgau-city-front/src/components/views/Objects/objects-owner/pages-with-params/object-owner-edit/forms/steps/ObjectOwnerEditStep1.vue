<template>
  <ObjectOwnerEditStepLayout>
    <div block class="update-btn-block">
      <v-btn
            @click="() => uploadContent()"
            class="update-btn"
            style="text-transform: none"
            size="large"
            color="#f57c01"
            >  {{ ubdateInfo ? 'Редактировать' : 'Сохранить' }}
        </v-btn>
      </div>
      
    <v-table class="table">
      <thead>
        <tr>
          <th class="text-left"></th>
          <th class="text-left"></th>
        </tr>
      </thead>
      <tbody class="table-body">
        <template v-for="item in objectInfoStore.generalObjectInfo"
          :key="item.key">
        <tr
            v-if="(item.key !== 'organization_optional_type' || filteredOptionalTypes.length > 0) && 
                   (item.key !== 'organization_characteristics' || filteredCharacteristics.length > 0)"
        >
          <td>
            <b>{{ item.title }}</b>
          </td>
          <td style="width: 400px; padding: 10px 0">
            <div class="info__block-box">
          </div>
          <v-select
              v-if="item.type === 'select' && item.key === 'organization_type'"
              v-model="selectedPrefix"
              class="role-select"
              :loading="objectInfoStore.isSaveLoading"
              :disabled="ubdateInfo"
              :items="prefixes"
              label="Выберите"
              variant="solo-filled"
              @update:modelValue="syncSelectsSubTypeObject"
            ></v-select>
            <v-select
            v-if="item.type === 'select' && item.key === 'organization_optional_type'"
              v-model="organizationOptionalType"
              class="role-select"
              :loading="objectInfoStore.isSaveLoading"
              :disabled="ubdateInfo"
              :items="filteredOptionalTypes"
              label="Выберите"
              variant="solo-filled"
            ></v-select>
            <v-select
            v-if="item.type === 'select' && item.key === 'organization_sub_type'"
              v-model="organizationSubType"
              class="role-select"
              :loading="objectInfoStore.isSaveLoading"
              :disabled="ubdateInfo"
              :items="filteredSubTypes"
              label="Выберите"
              variant="solo-filled"
              @update:modelValue="syncSelectsCharacteristicsObject"
            ></v-select>
            <v-select 
            v-if="item.type === 'select' && item.key === 'organization_characteristics'"
              v-model="characteristics"
              class="role-select"
              :loading="objectInfoStore.isSaveLoading"
              :disabled="ubdateInfo"
              :items="filteredCharacteristics"
              label="Выберите"
              variant="solo-filled"
            ></v-select>
            <v-text-field
              v-if="item.type === 'text' && item.key === 'address'"
              v-model="address"
              :loading="objectInfoStore.isSaveLoading"
              :disabled="ubdateInfo"
              :rules="item.rules"
              hide-details="auto"
              class="w-100"
              variant="solo-filled"
              clearable
              color="#f57c01"
            >
            </v-text-field>
            <v-text-field
              v-if="item.type === 'text' && item.key !== 'address'"
              v-model="item.value"
              :loading="objectInfoStore.isSaveLoading"
              :disabled="ubdateInfo"
              :rules="item.rules"
              hide-details="auto"
              class="w-100"
              variant="solo-filled"
              clearable
              color="#f57c01"
            >
            </v-text-field>
          </td>
        </tr>
      </template>
        <tr>
          <th class="text-left"></th>
          <th class="text-left"></th>
        </tr>
      </tbody>
    </v-table>

         <div 
            :class="ubdateInfo ? 'not-map' : 'map'">
            <input
              type="text"
              id="pac-input"
            />
            <MapRoot rootId="map-form" 
            @address-selected="handleAddressSelected"/>
            
          </div>

    <div class="avatar-wrapper">
      <div class="avatar-title">
        <h1 >Фото Обьекта:</h1>
        <span v-html="plus" class="plus" @click="uploadAvatar"></span>
      </div>

      <ObjectAvatar v-if="images" :images="images"/>

      <ObjectAvatar v-else :images="null"/>
    </div>

    <div class="avatar-wrapper">
      <div class="avatar-title">
        <h1 >Фото эвакуационная лестница:</h1>
        <span v-html="plus" class="plus" @click="uploadEscapeLadder"></span>
      </div>

      <ObjectEscapeLadderImage v-if="escapeLadderImages" :images="escapeLadderImages"/>

      <ObjectEscapeLadderImage v-else :images="null"/>
    </div>

    <SubBuildingCard />
    <ObjectRemarks />
  </ObjectOwnerEditStepLayout>
</template>

<script setup lang="ts">
import ObjectOwnerEditStepLayout from '../UI/ObjectOwnerEditStepLayout.vue'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import SubBuildingCard from '@views/SubBuilding/SubBuildingCard.vue'
import ObjectRemarks from '../../../../object-card/UI/ObjectRemarks.vue'
import ObjectAvatar from '@views/Objects/objects-owner/object-card/UI/ObjectAvatar.vue'
import { useObjectStore } from '@stores/ObjectStore'
import { computed, ref, watch, onMounted } from 'vue'
import { plus } from '@/assets/svg'
import { useRoute } from 'vue-router'
import { useSnackbarStore } from '@stores/SnackbarStore'
import ObjectEscapeLadderImage from '../../../../object-card/UI/ObjectEscapeLadderImage.vue'
import { type UpdateObject, type UpdateObjectInfoPayload, type RatingOption, type OrganizationTypeObject,   OrganizationSubTypesObject, OrganizationСharacteristics, } from '@/types/ObjectBuilding'
import { useGoogleMaps } from '@/hooks/useGoogleMaps'
import MapRoot from '@/components/views/Map/root/MapRoot.vue'
import { useMapStore } from '@/stores/MapStore'
import type { Coordinates } from '@/types/Map'
import { type BuildingCoordinatesValidator } from '@/types/ObjectBuilding'
import { objectService } from '@/services/object.service'
import { mapService } from '@/services/map.service'
import type { ObjectCoordinatesType } from '@/types/Map'
import ObjectPassport from '../../UI/ObjectPassport.vue'
import { useUserStore } from '@/stores/UserStore'

const snackbarStore = useSnackbarStore()
const objectInfoStore = useObjectInfoStore()
const objectStore = useObjectStore()

const userStore = useUserStore()
const route = useRoute()
const routeId = Number(route.params.id) as number
const ubdateInfo = ref(true)

const images = computed(() => objectStore.objectImages)
const escapeLadderImages = computed(() => objectStore.objectEscapeLadderImages)
const selectedAddress = ref('')
const dialog = ref(false)
const addressByHand = ref(false)
const mapStore = useMapStore()
const markers = ref<ObjectCoordinatesType[]>([])
const name = ref(
  `${userStore.user?.last_name} ${userStore.user?.first_name} ${userStore.user?.middle_name}`
)


const selectedPrefix = ref(objectInfoStore.generalObjectInfo.find(item => item.key === 'organization_type')?.value || '')
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
  'Производственные объекты Госбанка',
]);
const organizationOptionalType = ref(objectInfoStore.generalObjectInfo.find(item => item.key === 'organization_optional_type')?.value);
const prefixOptionalType = ref(['Диспансеры', 'Лечебно-профилактические учреждения', 'Амбулаторно-поликлинические учреждения', 'Учреждения скорой медицинской помощи', 'Учреждения для матерей и детей', 'Санитарно-противоэпидемические учреждения', 'Промышленные предприятия', 'Магазины', 'Здания общественного питания'])
const organizationSubType = ref(objectInfoStore.generalObjectInfo.find(item => item.key === 'organization_sub_type')?.value);
const characteristics = ref(objectInfoStore.generalObjectInfo.find(item => item.key === 'organization_characteristics')?.value )
const address = computed(() => {
  return mapStore.address 
    ? mapStore.address 
    : objectInfoStore.generalObjectInfo.find(item => item.key === 'address')?.value;
});
console.log(mapStore.address)

const uploadContent = async () => {
  ubdateInfo.value = !ubdateInfo.value
  addressByHand.value = !ubdateInfo.value

  if(ubdateInfo.value){
   
    try {
      const objectData: UpdateObject = {
        address: address.value || '',
        organization_type: selectedPrefix.value || '',
        organization_sub_type: organizationSubType.value || '',
        organization_characteristics: characteristics?.value|| '',
        organization_optional_type: organizationOptionalType?.value || '',
        organization_name: objectInfoStore.generalObjectInfo.find(item => item.key === 'organization_name')?.value || '',
        iin: objectInfoStore.generalObjectInfo.find(item => item.key === 'iin')?.value || '',
        rating: objectInfoStore.generalObjectInfo.find(item => item.key === 'rating')?.value as RatingOption,
        escape_ladder: objectInfoStore.generalObjectInfo.find(item => item.key === 'escape_ladder')?.value === 'true'
        }
     
        await objectStore.updateObject(routeId, objectData)
        snackbarStore.pullSnackbar('Объект успешно обновлен.', 2000, '#5b9271')



         // Получаем текущие маркеры
        markers.value = await mapService.getMarkersByBuildingId(routeId)

        console.log(markers.value[0].id)    
        console.log(routeId)

        // Определяем координаты
        const locationLatLng: Coordinates = {
          lat: mapStore.latLng ? mapStore.latLng.lat : 
          (markers.value.length > 0 ? markers.value[0].lat : 0),
          lng: mapStore.latLng ? mapStore.latLng.lng : 
          (markers.value.length > 0 ? markers.value[0].lng : 0)
        }

        // Создаем координаты через mapService
        const coordinatesBody: BuildingCoordinatesValidator = {
          lat: locationLatLng.lat,
          lng: locationLatLng.lng,
          building: routeId
        }

        await objectService.updateCoordinates(markers.value[0].id ,coordinatesBody)

    } catch (error) {
      snackbarStore.pullSnackbar('Не удалось обновить объект.', 2000, '#d20f0d')
      ubdateInfo.value = true
    }
  }     
}

const uploadAvatar = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e: any) => {
    try {
      const formData = new FormData()
      formData.append('images', e.target.files[0])

      await objectStore.createObjectAvatar(routeId, formData)
      snackbarStore.pullSnackbar('Ваше фото успешно загружено.', 2000, '#5b9271')
    } catch (error) {
      snackbarStore.pullSnackbar('Не удалось загрузить ваше фото.', 2000, '#d20f0d')
    }
  }
  input.click()
}

const uploadEscapeLadder = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e: any) => {
    try {
      const formData = new FormData()
      formData.append('images', e.target.files[0])

      await objectStore.createEscapeLadder(routeId, formData)
      snackbarStore.pullSnackbar('Ваше фото успешно загружено.', 2000, '#5b9271')
    } catch (error) {
      snackbarStore.pullSnackbar('Не удалось загрузить ваше фото.', 2000, '#d20f0d')
    }
  }
  input.click()
}


const filteredOptionalTypes = computed(() => {
  const data = OrganizationSubTypesObject[selectedPrefix.value as keyof typeof OrganizationSubTypesObject] || [];
  if (Array.isArray(data)) {
    return []; 
  } else if (data !== null && typeof data === 'object') {
    const keys = Object.keys(data);
    return keys; 
  } else {
    console.warn("data не является массивом или объектом.");
    return [];
  }
});

console.log(filteredOptionalTypes.value)

const filteredSubTypes = computed(() => {
  const data = OrganizationSubTypesObject[selectedPrefix.value as keyof typeof OrganizationSubTypesObject] || [];
  if (Array.isArray(data)) {
    return data;
  } else if (data !== null && typeof data === 'object') {
    const nestedData = data[organizationOptionalType.value as keyof typeof data];
    if (Array.isArray(nestedData)) {
      return nestedData;
    } else if (nestedData !== null && typeof nestedData === 'object') {
      return Object.values(nestedData);
    } else {
      console.warn("nestedData не является массивом или объектом.");
      return [];
    }
  } else {
    console.warn("Не удалось определить подтипы: данные не являются массивом или объектом.");
    return [];
  }
});

const filteredCharacteristics = computed(() => {
    if (organizationSubType.value as keyof typeof OrganizationСharacteristics && 
        typeof organizationSubType.value === 'string') {
        return Object.values(OrganizationСharacteristics[organizationSubType.value as keyof typeof OrganizationСharacteristics] || []);
    }
    return [];
});

const handleAddressSelected = (address: string) => {
  selectedAddress.value = address
}

const syncSelectsSubTypeObject = () => {
  organizationOptionalType.value = ''
  organizationSubType.value = ''
  characteristics.value = ''
}

const syncSelectsCharacteristicsObject = () => {
  characteristics.value = ''
}

// watch(() => ubdateInfo.value, async (newValue) => {
//   if (!newValue) { // Когда ubdateInfo становится false
//     const { allowClicking, placeOnUserLocation } = await useGoogleMaps('map-form', {
//       lng: 71.430,
//       lat: 51.128
//     })
//     allowClicking()
//     placeOnUserLocation()
//   }
// })

watch(() => ubdateInfo.value, async (newValue) =>  {
  if (!newValue) {
    name.value = `${userStore.user?.last_name} ${userStore.user?.first_name} ${userStore.user?.middle_name}`
    const { allowClicking, placeOnUserLocation } = await useGoogleMaps('map-form', {
      lng: 71.430,
      lat: 51.128
    })
    allowClicking()
    placeOnUserLocation()
  }
})

</script>

<style lang="scss" scoped>
.thead,
.table {
  width: 100%;
}

.table-body {
  font-size: 18px;
}

h1{
  font-size: 20px;
  font-weight: 600;
}

.avatar-wrapper{
  padding: 20px;

  & .avatar-title{
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px 0;
  }

  & .plus{
    color: #ffffff;
    background-color: #68696e;
    border-radius: 30%;
    display: flex;
    align-items: center;
    cursor: pointer;
  }
}

.update-btn-block{
  display: flex;
  justify-content: end;
}
.update-btn{
  width: 200px;
}

.not-map{
  display: none;
}

.map{
  max-width: 500px;
  margin: auto;
  display: block;
}

#map-form {
  height: 500px;
  width: 100%;
}

#pac-input {
  width: 200px;
}

@media only screen and (max-width: 524px) {
  .table-body {
    font-size: 14px;
  }
}
</style>
