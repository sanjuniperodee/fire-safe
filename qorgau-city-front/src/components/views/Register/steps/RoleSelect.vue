<script setup lang="ts">
import { roleRules } from '@views/Register/Rules'
import { computed, ref, watch, onMounted } from 'vue'
import {
  type roles,
  type rolesRussian,
  roleTypesMapping,
  reversedRoleTypesMapping,
  UserRoleOptions,
  type rank,
  type rankRussian,
  rankTypesMapping,
  reversedRankTypesMapping,
  //UserRankOptions,
  type position,
  positionTypesMapping,
  reversedPositionTypesMapping,
} from '@/types/User'
import { 
  type mainType,
  mainTypeTypesMapping,
  organizationTypes,
  reversedMainTypeTypesMapping,
  reversedOrganizationTypesMapping,
  type OrganizationTypes,
  OrganizationSubTypes
  } from '@/types/ObjectBuilding'
import { categories as categoryList } from '@/utils/categoryList'

const props = defineProps<{
  role: roles,
  // PROVIDER
  categories?: number[],
  //organization_type?: OrganizationTypes,
  organization_name?: string,
  main_organization_type?: mainType, 
  organization_type?: OrganizationTypes,
  organization_sub_type?: string,
  bin_field: string,
  // INSPECTOR
  rank: rank,
  position: position,
  certificate_number?: string,
  inspector_jurisdiction_city?: string,
  inspector_jurisdiction_district?: string,
  //CTIZEN, PROVIDER, OBJECT_OWNER
  actual_residence_address?: string,
  residence_address?: string,
}>()

const emit = defineEmits(['updateData'])

const isProvider = computed(() => userRole.value === 'PROVIDER')
const isInspector = computed(() => userRole.value === 'INSPECTOR')
const isCitizen = computed(() => userRole.value === 'CITIZEN')
const isObjectOwner = computed(() => userRole.value === 'OBJECT_OWNER')

const rules = {
  required: (value: any) => !!value || 'Поле обязательно',
  isNumber: (value: any) => !isNaN(value) || 'Должно быть числом',
  certificate:[
    (value: any) => !isNaN(value) || 'Должно быть числом',
    (v: any) => parseInt(v.length) === 5 || 'Длина удостоверение должна быть 5 цифр',
  ],
  optional: (value: any) => true
}

const BINRules = ref([
  (v: any) => !!v || 'БИН обязателен', // Проверка на наличие значения
  (v: any) => !isNaN(Number(v)) || 'БИН должен быть числом', // Проверка на число
  (v: any) => v.length === 12 || 'Длина БИН должна быть 12 цифр' // Проверка на длину
]);

const userRole = ref<roles>(props.role || 'CITIZEN')
const selectedRole = ref(roleTypesMapping[userRole.value])

// PROVIDER
// const selectedPrefix = ref<OrganizationTypesLocales>('ТОО')
// const prefixes = ref(['ТОО', 'ИП', 'АО'])
const selectedCategories = ref<number[]>(props.categories || [])
const organizationName = ref(props.organization_name || '')
const userMainType = ref<mainType>(props.main_organization_type || 'Commercial Organizations')
const mainOrganizationType = ref(mainTypeTypesMapping[userMainType.value])
// const userOrganizationTypes = ref<OrganizationTypes>(props.organization_type || 'State-owned enterprises')
const organizationType = ref<string>('');
const organizationSubType = ref<string>('')
const binField = ref<string>('')


// INSPECTOR
const userRank =  ref<rank>(props.rank || 'PrivateCivilProtection')
const selectedRank = ref(rankTypesMapping[userRank.value])
const userPosition = ref<position>(props.position || 'Chief State Inspector for FireControl')
const selectedPosition = ref(positionTypesMapping[userPosition.value])
const certificateNumber = ref('')
const inspectorJurisdictionCity = ref(props.inspector_jurisdiction_city || '')
const inspectorJurisdictionDistrict = ref(props.inspector_jurisdiction_district || '')

//CITIZEN, PROVIDER, OBJECT_OWNER
const actualResidenceAddress = ref('')
const residenceAddress = ref('')

const handleRoleChange = (newRussianRole: string) => {
  if (newRussianRole in reversedRoleTypesMapping) {
    userRole.value = reversedRoleTypesMapping[newRussianRole as rolesRussian] as roles
    selectedRole.value = newRussianRole as rolesRussian
    binField.value = '';
    updateData()
  }
}

const syncSelectsType = () => {
  organizationType.value = ''
  organizationSubType.value = ''
}

const syncSelectsSubType = () => {
  organizationSubType.value = ''
}

const updateData = () => {
  if(userRole.value === UserRoleOptions.PROVIDER){
    emit('updateData', {
      role: userRole.value,
      categories: selectedCategories.value,
      //organization_type: selectedPrefix.value,
      organization_name: organizationName.value,
      actual_residence_address: actualResidenceAddress.value,
      residence_address: residenceAddress.value,
      main_organization_type: reversedMainTypeTypesMapping[mainOrganizationType.value],
      organization_type: reversedOrganizationTypesMapping[organizationType.value],
      organization_sub_type: organizationSubType.value,
      bin_field: binField.value,
    })
  } else if(userRole.value === UserRoleOptions.INSPECTOR){
    emit('updateData', {
      role: userRole.value,
      rank: reversedRankTypesMapping[selectedRank.value],
      position: reversedPositionTypesMapping[selectedPosition.value],
      certificate_number: certificateNumber.value,
      inspector_jurisdiction_city: inspectorJurisdictionCity.value,
      inspector_jurisdiction_district: inspectorJurisdictionDistrict.value,
    })
  } else if (userRole.value === UserRoleOptions.OBJECT_OWNER) {
    emit('updateData', {
      role: userRole.value, // Явно указываем роль OBJECT_OWNER
      actual_residence_address: actualResidenceAddress.value,
      residence_address: residenceAddress.value,
    });
  } else if (userRole.value === UserRoleOptions.CITIZEN) {
    emit('updateData', {
      role: userRole.value, // Явно указываем роль CITIZEN
      actual_residence_address: actualResidenceAddress.value,
      residence_address: residenceAddress.value,
    });
  }else {
    emit('updateData', {
      role: userRole.value,
    })
  }
}

const updateList = [selectedCategories, organizationName, selectedRank, selectedPosition, certificateNumber, actualResidenceAddress,  residenceAddress, inspectorJurisdictionCity, inspectorJurisdictionDistrict, mainOrganizationType, organizationType, binField]

watch(updateList, updateData)

const russianRoles = Object.values(roleTypesMapping)
const russianRank = Object.values(rankTypesMapping)
const russianPosition = Object.values(positionTypesMapping)
const russianMainType = Object.values(mainTypeTypesMapping)
const russianOperationType = computed(() => {
  if(mainOrganizationType.value === 'Коммерческие организации'){
    return Object.values(organizationTypes.CommercialOrganizations)
  }
  else if(mainOrganizationType.value === 'Некоммерческие организации'){
   return Object.values(organizationTypes.NonCommercialOrganizations)
  }
  else {
    return []
  }

  // return mainOrganizationType.value === 'Коммерческие организации'
  //   ? Object.values(organizationTypes.CommercialOrganizations)
  //   : Object.values(organizationTypes.NonCommercialOrganizations)
})



const russianOperationSubType = computed(() => {
  switch (organizationType.value) {
    case 'Государственные предприятия':
      return Object.values(OrganizationSubTypes.StateOwnedEnterprises);
    case 'Хозяйственные товарищества':
      return Object.values(OrganizationSubTypes.BusinessPartnerships);
    case 'Акционерное общество(Коммерческие)':
      return Object.values(OrganizationSubTypes.JointStockCompany);
    case 'Производственный кооператив':
      return Object.values(OrganizationSubTypes.ProductionCooperative);
    case 'Учреждения':
      return Object.values(OrganizationSubTypes.Institutions);
    case 'Общественное объединение':
      return Object.values(OrganizationSubTypes.PublicAssociation);
    case 'Акционерное общество(Некоммерческие)':
      return Object.values(OrganizationSubTypes.JointStockCompany_NonCommercial);
    case 'Потребительский кооператив':
      return Object.values(OrganizationSubTypes.ConsumerCooperative);
    case 'Фонд':
      return Object.values(OrganizationSubTypes.Fund);
    case 'Религиозные объединения':
      return Object.values(OrganizationSubTypes.ReligiousAssociations);
    case 'Объединения индивидуальных предпринимателей и (или) юридических лиц в форме ассоциации (союза)':
      return Object.values(OrganizationSubTypes.AssociationsOfEntrepreneurs);
    case 'Иные формы, предусмотренные законодательством':
      return Object.values(OrganizationSubTypes.OtherForms);
    default:
      return [];
  }
});

</script>

<template>
  <div class="step2-container">
    <h1 class="step-title">Выберите роль</h1>
    <v-select
      :rules="roleRules"
      v-model="selectedRole"
      class="role-select"
      :label="$t('roleLabel')"
      :items="russianRoles"
      variant="outlined"
      @update:modelValue="handleRoleChange"
    ></v-select>

    <div v-if="isProvider">
      <h1 class="step-title">Заполните поля для Поставщика</h1>
      <div class="input-group">
        <!-- <v-select
          v-model="selectedPrefix"
          :rules="[rules.required]"
          :items="prefixes"
          class="select-prefix"
          variant="outlined"
          dense
          hide-details
        ></v-select> -->
        <v-text-field
          v-model="organizationName"
          :rules="[rules.required]"
          label="Введите наименование организации"
          class="text-organization-name"
          variant="outlined"
          clearable
          hide-details
        ></v-text-field>
      </div>

      <v-select
        v-model="selectedCategories"
        :items="categoryList"
        item-title="name"
        item-value="id"
        label="Выберите категории"
        multiple
        chips
        :rules="[rules.required]"
      ></v-select>
      <v-select
        v-model="mainOrganizationType"
        class="role-select"
        :items="russianMainType"
        label="Выбирает из вариантов"
        variant="outlined"
        @update:modelValue="syncSelectsType"
      ></v-select>

      <v-select
        v-model="organizationType"
        class="role-select"
        :items="russianOperationType"
        label="Выберите"
        variant="outlined"
        @update:modelValue="syncSelectsSubType"
      ></v-select>
      <v-select
        v-model="organizationSubType"
        class="role-select"
        :items="russianOperationSubType"
        label="Выберите"
        variant="outlined"
      ></v-select>

      <div class="input-address">
        <v-text-field
          v-model="actualResidenceAddress"
          label="⁠Адрес фактического проживания"
          variant="outlined"
          dense
          :rules="[rules.optional]"
          hide-details="auto"
        ></v-text-field>
        <v-text-field
          v-model="residenceAddress"
          label="⁠Адрес прописки"
          variant="outlined"
          dense
          :rules="[rules.optional]"
          hide-details="auto"
        ></v-text-field>
        <v-text-field
          :rules="BINRules"
          :counter="12"
          v-model="binField"
          variant="outlined"
          label="БИН"
          clearable
          class="form__input"
          hide-details="auto"
    ></v-text-field>
      </div>
    </div>

    <div v-if="isInspector">
      <h1 class="step-title">Заполните поля для Инспектора</h1>
      <div class="inspector-wrapper">
        <v-select
          v-model="selectedRank"
          class="rank-select"
          label="Звание"
          :items="russianRank"
          variant="outlined"
          dense
          hide-details="auto"
        ></v-select>
        <v-select
          v-model="selectedPosition"
          class="rank-select"
          label="Должность"
          :items="russianPosition"
          variant="outlined"
          dense
          hide-details="auto"
        ></v-select>
        <v-text-field
          v-model="inspectorJurisdictionCity"
          label="Город"
          variant="outlined"
          dense
          hide-details="auto"
        ></v-text-field>
        <v-text-field
          v-model="inspectorJurisdictionDistrict"
          label="Район"
          variant="outlined"
          dense
          hide-details="auto"
        ></v-text-field>
        <v-text-field
          v-model="certificateNumber"
          :rules="rules.certificate"
          :counter="5"
          label="Номер удостоверении CO №"
          variant="outlined"
          clearable
          hide-details="auto"
        ></v-text-field>
      </div>
    </div>
    <div v-if="isObjectOwner">
      <h1 class="step-title">Заполните поля для Владелец объекта</h1>
      <div class="citizen-wrapper">
        <v-text-field
          v-model="actualResidenceAddress"
          label="⁠Адрес фактического проживания"
          variant="outlined"
          dense
          :rules="[rules.optional]"
          hide-details="auto"
        ></v-text-field>
        <v-text-field
          v-model="residenceAddress"
          label="⁠Адрес прописки"
          variant="outlined"
          dense
          :rules="[rules.optional]"
          hide-details="auto"
        ></v-text-field>
      </div>
    </div>
    <div v-if="isCitizen">
      <h1 class="step-title">Заполните поля для Гражданина</h1>
      <div class="citizen-wrapper">
        <v-text-field
          v-model="actualResidenceAddress"
          label="⁠Адрес фактического проживания"
          variant="outlined"
          dense
          :rules="[rules.optional]"
          hide-details="auto"
        ></v-text-field>
        <v-text-field
          v-model="residenceAddress"
          label="⁠Адрес прописки"
          variant="outlined"
          dense
          :rules="[rules.optional]"
          hide-details="auto"
        ></v-text-field>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.step2-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-title {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 10px;
}

.role-select {
  width: 100%;
}

.rank-select {
  width: 100%;
}
//PROVIDER FIELDS
.input-group {
  display: flex;
  align-items: center;
  gap: 0.5em;
  margin-bottom: 15px;
}
.text-organization-name {
  width: 80%;
}
.select-prefix {
  width: 20%;
}
.input-address{
   display: flex;
  flex-direction: column;
  gap: 15px;
}
//INSPECTOR FIELDS
.inspector-wrapper{
  display: flex;
  flex-direction: column;
  gap: 15px;
}
//CITIZEN FIELDS
.citizen-wrapper{
  display: flex;
  flex-direction: column;
  gap: 15px;
}
</style>