<template>
  <div class="info">
    <div class="language-switch">
      <button
        :class="{ active: currentLanguage === 'ru' }"
        @click="setLanguage('ru')"
      >
        Русский
      </button>
      <button
        :class="{ active: currentLanguage === 'en' }"
        @click="setLanguage('en')"
      >
        English
      </button>
      <button
        :class="{ active: currentLanguage === 'kz' }"
        @click="setLanguage('kz')"
      >
        Қазақша
      </button>
    </div>
    <div class="info__box">
      <v-card-title class="info__title">Личная информация:</v-card-title>
      <v-form
        ref="userInfoFormRef"
        class="info__block"
      >
        <div
          class="info__block-item"
          v-for="item in generalFields"
          :key="item.name"
        >
          <div class="info__block-box">
            <v-card-title class="info__block-title">{{ item.name }}</v-card-title>
            <v-btn
              v-if="!item.isEditing && item.key !== 'birthdate'"
              @click="editField(item.key)"
              icon="mdi-pencil"
              rounded="lg"
              size="x-small"
              color="#f57c01"
              class="text-white"
            ></v-btn>
            <div
              v-if="item.isEditing && item.key !== 'birthdate'"
              class="info__editing-btns"
            >
              <v-btn
                @click="saveEditing(item.key)"
                icon="mdi-check-bold"
                rounded="lg"
                size="x-small"
                color="#5b9271"
                class="text-white"
              ></v-btn>
              <v-btn
                @click="cancelEditing(item.key)"
                icon="mdi-close"
                rounded="lg"
                size="x-small"
                color="#d20f0d"
                class="text-white"
              ></v-btn>
            </div>
          </div>

          <v-text-field
            :rules="item.rules"
            v-if="item.key !== 'birthdate'"
            :disabled="!item.isEditing"
            v-model="item.value"
            :label="item.name"
            variant="outlined"
            :readonly="!item.isEditing"
          ></v-text-field>

          <v-text-field
            class="no-calendar-icon"
            v-if="item.key === 'birthdate'"
            type="date"
            v-model="formattedBirthdate"
            variant="outlined"
            @change="(event: any) => saveBirthdate(new Date(event.target.value))"
          ></v-text-field>

        </div>
      </v-form>

      <div v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)">
        <InspectorProfile/>
      </div>

      <div v-if="userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER)">
        <ProviderProfile/>
      </div>

      <div v-if="!userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER) && !userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)">
        <CitizenProfile/>
      </div>

      <div class="role_password_wrapper">
        <ChangePassword/>
        <UserRole />
      </div>

      <v-card-title class="info__title">Объекты ({{ objectStore?.objects.length }}):</v-card-title>

      <router-link :to="{ name: 'Objects' }">
        <v-btn
          :prepend-icon="
            userStore.acceptedRoles.includes(UserRoleOptions.CITIZEN)
              ? 'mdi-map-search-outline'
              : 'mdi-domain'
          "
          class="w-50 object-btn"
          color="#f57c01"
          variant="tonal"
        >
          <span style="padding-top: 10px">
            {{
              userStore.acceptedRoles.includes(UserRoleOptions.CITIZEN)
                ? 'Перейти к просмотру тепловой карты'
                : 'Перейти к моим объектам'
            }}
          </span>
        </v-btn>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { useProfileStore } from '@stores/ProfileStore'
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import UserRole from './utils/EditRole.vue'
import { UserRoleOptions } from '@/types/User'
import { formatDateForValidation } from '@/helpers/formatTime'
import { useObjectStore } from '@stores/ObjectStore'
import { editField, saveEditing, save, cancelEditing } from './utils/editFunctions'
import InspectorProfile from './RoleProfiles/InspectorProfile.vue'
import ProviderProfile from './RoleProfiles/ProviderProfile.vue'
import CitizenProfile from './RoleProfiles/CitizenProfile.vue'
import ChangePassword from './utils/ChangePassword.vue'

const i18n = useI18n()
const currentLanguage = ref('ru')

const setLanguage = (locale: string) => {
  i18n.locale.value = locale
  currentLanguage.value = locale
}

const profileStore = useProfileStore()
const userStore = useUserStore()
const objectStore = useObjectStore()
const userInfoFormRef = ref(null)

let excludingFields = [
  'rank', 'position', 'certificate_number', 'main_organization_type', 'organization_type',
  'organization_sub_type', 'organization_name', 'bin_field', 'categories', 'inspector_jurisdiction_city', 'inspector_jurisdiction_district', 'actual_residence_address', 'residence_address'
]

const generalFields = ref(
  Object.values(profileStore.items).filter(
    (item) => !excludingFields.includes(item.key)
  )
)

const formattedBirthdate = computed(() => {
  const item = generalFields.value.find(i => i.key === 'birthdate');
  if (item && item.value) {
    return formatDateForValidation(item.value as Date);
  }
  return '';
});

const saveBirthdate = (value: Date) => {
   const timeZoneOffset = value.getTimezoneOffset()
  value.setMinutes(value.getMinutes() - timeZoneOffset)
  userStore.user!.birthdate = formatDateForValidation(value)
  save()
}

onMounted(() => {
  if (userStore.user) {
    profileStore.fillItemsValues(userStore.user)
  }
})
</script>

<style lang="scss" scoped>
.language-switch {
  display: flex;
  margin-bottom: 30px;
}

.language-switch button {
  padding: 8px 12px;
  margin-right: 8px;
  border-radius: 4px;
  background-color: transparent;
  color: #333;
  cursor: pointer;
}

.language-switch button.active {
  background-color: #ff6a00 !important;
  color: #fff !important;
}

.info {
  margin-top: 10em;
  padding-bottom: 4em;
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;

  &__title {
    padding: 0;
    margin-bottom: 1em;
    font-size: 20px;
    font-weight: 600;
    width: 100%;
  }

  &__box {
    display: flex;
    flex-direction: column;
    width: 80%;
  }

  &__block {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    margin-bottom: 20px;
    background-color: white;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 20px;
  }

  &__block-item {
    display: flex;
    flex-direction: column;
    width: 49%;
  }

  &__block-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 32px;
    margin-bottom: 10px;
  }

  &__block-title {
    font-size: 16px;
    padding: 0 0 5px 0;
  }

  &__editing-btns {
    display: flex;
    gap: 0.5em;
  }
}

.role_password_wrapper{
  display: flex;
  align-items: stretch;
  gap: 1.5em;
  margin-bottom: 30px;
}

span{
  margin-bottom: 15px;
}

.no-calendar-icon input[type='date']::-ms-clear,
.no-calendar-icon input[type='date']::-ms-expand,
.no-calendar-icon input[type='date']::-webkit-inner-spin-button {
  display: none;
}
.no-calendar-icon {
  :deep(input[type="date"]::-webkit-calendar-picker-indicator) {
    display: none;
  }
}

@media only screen and (max-width: 937px) {
  .info__block-item {
    width: 100%;
  }

  .role_password_wrapper{
    flex-direction: column;
    gap: 0;
  }

  .object-btn {
    width: 70% !important;
    font-size: 12px !important;
  }
}

@media only screen and (max-width: 440px) {
  .object-btn {
    width: 100% !important;
    font-size: 10px !important;
  }
}
</style>

