<script setup lang="ts">
import { computed, ref } from 'vue'
import { useProfileStore } from '@/stores/ProfileStore'
import { editField, cancelEditing, saveEditing } from '../utils/editFunctions'
import {
  getEnglishOrganizationType,
  getLocalOrganizationType,
  type OrganizationTypesLocales,
  OrganizationSubTypes,
  getEnglishOrganizationMainType,
  getLocalOrganizationMainType,
  type mainTypeRussian
} from '@/types/ObjectBuilding'
import ProviderInfoBlocks from '@views/Profile/profile-info/RoleProfiles/ProviderInfo/ProviderInfoBlocks.vue'
import ProfileCategories from '@views/Profile/profile-info/utils/ProfileCategories.vue'
import { profileItems } from '@/utils/LongFormsStorage'

const profileStore = useProfileStore()

const prefixesMainType = ref<mainTypeRussian[]>(['Коммерческие организации', 'Некоммерческие организации'])

const currentOrganizationMainType = computed({
  get: () => {
    const currentKey = profileStore.items.main_organization_type
    return getLocalOrganizationMainType(currentKey.value)
  },
  set: (value: mainTypeRussian) => {
    profileStore.items.main_organization_type.value = getEnglishOrganizationMainType(value)
  }
})


const prefixes = ref<OrganizationTypesLocales[]>(['Государственные предприятия', 'Хозяйственные товарищества', 'Акционерное общество(Коммерческие)', 'Производственный кооператив', 'Учреждения', 'Общественное объединение', 'Акционерное общество(Некоммерческие)', 'Производственный кооператив', 'Фонд', 'Религиозные объединения', 'Объединения индивидуальных предпринимателей и (или) юридических лиц в форме ассоциации (союза)', 'Иные формы, предусмотренные законодательством'])

const currentOrganizationType = computed({
  get: () => {
    const currentKey = profileStore.items.organization_type
    return getLocalOrganizationType(currentKey.value)
  },
  set: (value: OrganizationTypesLocales) => {
    profileStore.items.organization_type.value = getEnglishOrganizationType(value)
  }
})

const prefixesSubType = ref<OrganizationSubTypes[]>([])


const russianOperationSubType = computed(() => {
  switch (currentOrganizationType.value) {
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

const providerFields = ref([
  profileStore.items.main_organization_type,
  profileStore.items.organization_type,
  profileStore.items.organization_sub_type,
  profileStore.items.organization_name,
  profileStore.items.bin_field,
  profileStore.items.actual_residence_address,
  profileStore.items.residence_address,
])

</script>

<template>
  <v-card-title class="info__title">Информация о вашей деятельности:</v-card-title>

  <div class="info__block">
    <div class="info__block-item" v-for="providerItem in providerFields" :key="providerItem.name">
      <div class="info__block-box">
        <v-card-title class="info__block-title">{{ providerItem.name }}</v-card-title>
        <v-btn v-if="!providerItem.isEditing" @click="editField(providerItem.key)" icon="mdi-pencil" rounded="lg"
          size="x-small" color="#f57c01" class="text-white"></v-btn>
        <div v-if="providerItem.isEditing" class="info__editing-btns">
          <v-btn v-if="providerItem.key" @click="saveEditing(providerItem.key)" icon="mdi-check-bold" rounded="lg"
            size="x-small" color="#5b9271" class="text-white"></v-btn>
          <v-btn @click="cancelEditing(providerItem.key)" icon="mdi-close" rounded="lg" size="x-small" color="#d20f0d"
            class="text-white"></v-btn>
        </div>
      </div>

      <div v-if="providerItem.key === 'main_organization_type'">
        <v-select v-model="currentOrganizationMainType" :rules="providerItem.rules" :items="prefixesMainType"
          :disabled="!providerItem.isEditing" class="select-prefix" variant="outlined" dense hide-details></v-select>
      </div>

      <div v-else-if="providerItem.key === 'organization_type'">
        <v-select v-model="currentOrganizationType" :rules="providerItem.rules" :items="prefixes"
          :disabled="!providerItem.isEditing" class="select-prefix" variant="outlined" dense hide-details></v-select>
      </div>


      <div v-else-if="providerItem.key === 'organization_sub_type'">
        <v-select v-model="providerItem.value" :rules="providerItem.rules" :items="russianOperationSubType"
          :disabled="!providerItem.isEditing" class="select-prefix" variant="outlined" dense hide-details></v-select>
      </div>

      <v-text-field v-else :rules="providerItem.rules" :disabled="!providerItem.isEditing" v-model="providerItem.value"
        :label="providerItem.name" variant="outlined" :readonly="!providerItem.isEditing"></v-text-field>
    </div>


  </div>

  <ProfileCategories />

  <ProviderInfoBlocks />
</template>


<style scoped lang="scss">
.info {
  margin-top: 10em;
  padding-bottom: 4em;
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;

  &__title {
    padding: 0;
    width: 100%;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 1em;
  }

  &__block {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    background-color: white;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 20px;
  }

  &__block-item {
    gap: 1em;
    display: flex;
    flex-direction: column;
    width: 49%;
  }

  &__block-box {
    height: 32px;
    justify-content: space-between;
    gap: 1em;
    width: 100%;
    align-items: center;
    display: flex;
  }

  &__block-title {
    font-size: 16px;
    padding: 0;
  }

  &__editing-btns {
    display: flex;
    gap: 0.5em;
  }
}

@media only screen and (max-width: 937px) {
  .info__block-item {
    width: 100%;
  }
}
</style>
