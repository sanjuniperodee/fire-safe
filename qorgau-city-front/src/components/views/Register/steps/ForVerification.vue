<script setup lang="ts">
import { passwordRules, phoneRules } from '@views/Register/Rules'
import { vMaska } from 'maska'
import { ref, watch } from 'vue'

const props = defineProps<{
  phone: string,
  password: string,
  password2: string
}>()

const emit = defineEmits(['updateData'])

const userPhone = ref(props.phone)
const password = ref(props.password)
const password2 = ref(props.password2)
const showPassword = ref(false)
const error = ref('')

userPhone.value = JSON.parse(localStorage.getItem('phone') || '{}');

const options = { mask: '+77#########' }

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const volidatePassword = () => {
  if(password.value === password2.value){
    return true
  }else {
    return false
  }
}

const updateData = () => {
  emit('updateData', {
    phone: userPhone.value,
    password: password.value,
    password2: password2.value
  })
  
  if(volidatePassword() === true){
    emit('updateData', {
    phone: userPhone.value,
    password: password.value,
    password2: password2.value
  })
  localStorage.removeItem('phone')
  }else{
    error.value = 'Пароли не совпадают'
  }
}

watch([userPhone, password, password2], updateData)
</script>

<template>
  <div class="step2-container">
    <h1>Номер и пароль</h1>

    <v-text-field
      :rules="phoneRules"
      class="form__input"
      :label="$t('phoneNumberLabel')"
      v-maska:[options]
      v-model="userPhone"
      clearable
      variant="outlined"
      hide-details="auto"
      type="tel"
      name="phone"
      disabled
    ></v-text-field>

    <v-text-field
      :rules="passwordRules"
      :counter="20"
      :label="$t('passwordLabel')"
      v-model="password"
      variant="outlined"
      clearable
      class="form__input"
      hide-details
      :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
      @click:append="togglePasswordVisibility"
      :type="showPassword ? 'text' : 'password'"
    ></v-text-field>

    <v-text-field
      :rules="passwordRules"
      :counter="20"
      :label="$t('confirmPasswordLabel')"
      v-model="password2"
      variant="outlined"
      clearable
      class="form__input"
      hide-details="auto"
      :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
      @click:append="togglePasswordVisibility"
      :type="showPassword ? 'text' : 'password'"
    ></v-text-field>
  </div>
</template>

<style scoped lang="scss">
.step2-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

h1{
  font-weight: 500;
  font-size: 20px;
}

.form__input {
  width: 100%;

  :deep(.v-field__append-inner) {
    cursor: pointer;
  }
}

:deep(.v-field__append-inner) {
  transition: opacity 0.3s ease;

  &:hover {
    opacity: 0.7;
  }
}

:deep(.v-field--focused) {
  .v-field__outline {
    border-color: #1976D2 !important;
  }
}

:deep(.v-field:hover) {
  .v-field__outline {
    border-color: #1976D2;
  }
}

.errorMessage {
  font-family: "Overpass", sans-serif;
  color: #B00020;
  font-size: 14px;
  line-height: 17px;
}
</style>