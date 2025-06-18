<script setup lang="ts">
import { emailRules, fullNameRules, IINRules } from '@views/Register/Rules'
import { ref, watch } from 'vue'
import { formatDateForValidation } from '@/helpers/formatTime'
import type { Ref } from 'vue';

const props = defineProps<{
  name: string,
  surname: string,
  middlename: string,
  email: string,
  birthdate: Date,
  IIN: string
}>()

const emit = defineEmits(['updateData'])

const userName = ref(props.name)
const userSurname = ref(props.surname)
const userMiddlename = ref(props.middlename)
const userMail = ref(props.email)
const userBirthDate = ref<Date>(props.birthdate || formatDateForValidation(new Date()))
const userIIN = ref<string>(props.IIN)
const fullName = ref('')

const processFullName = () => {
  const names = fullName.value.split(' ')
  userSurname.value = names[0] || ''
  userName.value = names[1] || ''
  userMiddlename.value = names.slice(2).join(' ') || ''
  updateData()
}

const updateData = () => {
  emit('updateData', {
    first_name: userName.value,
    last_name: userSurname.value,
    middle_name: userMiddlename.value,
    email: userMail.value,
    birthdate: userBirthDate.value,
    iin: userIIN.value
  })
}

watch([userMail, userBirthDate, userIIN], updateData)
</script>

<template>
  <div class="step1-container">
    <h1>Общая информация</h1>

    <v-text-field
      :rules="fullNameRules"
      class="form__input"
      :label="$t('fullName')"
      v-model="fullName"
      clearable
      variant="outlined"
      hide-details="auto"
      @blur="processFullName"
    ></v-text-field>

    <v-text-field
      :rules="emailRules"
      class="form__input"
      :label="$t('emailLabel')"
      v-model="userMail"
      clearable
      variant="outlined"
      hide-details="auto"
      type="email"
      name="email"
    ></v-text-field>

<!--    <div class="birth-date-field">-->
<!--      <span class="birth-date-label">{{ $t('birthDateLabel') }}: </span>-->
<!--    </div>-->

    <v-text-field
      :label="$t('birthDateLabel')"
      class="form__input no-calendar-icon"
      type="date"
      v-model="userBirthDate"
      variant="outlined"
      hide-details
    ></v-text-field>

    <v-text-field
      :rules="IINRules"
      :counter="12"
      :label="$t('IINLabel')"
      v-model="userIIN"
      variant="outlined"
      clearable
      class="form__input"
      hide-details="auto"
    ></v-text-field>
  </div>
</template>

<style scoped lang="scss">
.step1-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h1{
  font-size: 20px;
  font-weight: 500;
}

.form__input {
  width: 100%;
}

.birth-date-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.birth-date-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
}

.no-calendar-icon {
  :deep(input[type="date"]::-webkit-calendar-picker-indicator) {
    display: none;
  }
}
</style>