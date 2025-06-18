<script setup lang="ts">
import { ref } from 'vue'
import type { ChangePasswordValidator } from '@/types/Auth'
import { authService } from '@/services/auth.service'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { useUserStore } from '@stores/UserStore'

const snackbarStore = useSnackbarStore()
const userStore = useUserStore()

const newPassword = ref<string>('')
const oldPassword = ref<string>('')
const newPasswordRepeat = ref<string>('')

const passwordRules = ref([
  (v: any) => !!v || 'Пароль обязателен',
  (v: any) => (v && v.length >= 8) || 'Пароль должен быть более чем 8 символов',
  (v: any) => (v && v.length <= 20) || 'Пароль должен быть менее чем 20 символов'
])

const isPasswordLoading = ref(false)
const isPasswordEditing = ref(false)

const changePassword = async () => {
  const payload: ChangePasswordValidator = {
    phone: userStore.user?.phone!,
    new_password: newPassword.value,
    old_password: oldPassword.value,
    confirm_password: newPasswordRepeat.value
  }

  try {
    isPasswordLoading.value = true
    const message = await authService.changePassword(payload)
    snackbarStore.pullSnackbar(message, 3000, '#5b9271')
    isPasswordLoading.value = false
  } catch (error) {
    snackbarStore.pullSnackbar('Не удалось обновить ваш пароль.', 3000, '#d20f0d')
    isPasswordLoading.value = false
  }
}
</script>

<template>
  <div class="password_wrapper">
    <v-card-title
      class="info__title"
      style="margin-top: 20px"
    >Изменить пароль:</v-card-title>
    <div class="info__passwords">
      <v-text-field
        :disabled="!isPasswordEditing"
        :rules="passwordRules"
        :loading="isPasswordLoading"
        name="password"
        label="Старый пароль"
        v-model="oldPassword"
        variant="outlined"
        placeholder="Введите старый пароль"
        clearable
        class="password-input"
        hide-details="auto"
        type="password"
        :counter="20"
      ></v-text-field>
      <v-text-field
        :disabled="!isPasswordEditing"
        :rules="passwordRules"
        :loading="isPasswordLoading"
        name="password"
        label="Новый пароль"
        v-model="newPassword"
        variant="outlined"
        placeholder="Введите новый пароль"
        clearable
        class="password-input"
        hide-details="auto"
        type="password"
        :counter="20"
      ></v-text-field>
      <v-text-field
        :disabled="!isPasswordEditing"
        :rules="passwordRules"
        :loading="isPasswordLoading"
        label="Подтверждение нового пароля"
        name="password"
        v-model="newPasswordRepeat"
        variant="outlined"
        placeholder="Повторите новый пароль"
        clearable
        class="password-input"
        hide-details="auto"
        type="password"
        :counter="20"
      ></v-text-field>
      <v-btn
        v-if="!isPasswordEditing"
        prepend-icon="mdi-pencil"
        class="object-btn"
        @click="isPasswordEditing = true"
        color="#f57c01"
      >
        <span style="padding-top: 4px">Изменить пароль</span>
      </v-btn>
      <div
        v-if="isPasswordEditing"
        style="display: flex; justify-content: space-between; gap: 8px"
      >
        <v-btn
          prepend-icon="mdi-content-save"
          class="w-50 object-btn"
          @click="changePassword"
          color="#5b9271"
        >
          <span style="padding-top: 4px">Сохранить пароль</span>
        </v-btn>
        <v-btn
          prepend-icon="mdi-cancel"
          @click="isPasswordEditing = false"
          class="w-50 object-btn"
          color="#f57c01"
          variant="tonal"
        >
          <span style="padding-top: 4px">Отмена</span>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.password_wrapper{
  flex: 1;
}

.info {
  margin-top: 10em;
  padding-bottom: 4em;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;

  &__title {
    padding: 0;
    margin-bottom: 1em;
    font-size: 20px;
    font-weight: 600;
    width: 100%;
  }

  &__passwords {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 80%;
    gap: 10px;
    margin-bottom: 20px;
    background-color: white;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 20px;
  }

  &__editing-btns {
    display: flex;
    gap: 0.5em;
  }
}

@media only screen and (max-width: 720px) {
  .password-input {
    width: 50%;
  }

  .object-btn {
    width: 70% !important;
    font-size: 12px !important;
  }
}

@media only screen and (max-width: 440px) {
  .password-input {
    width: 80%;
  }

  .object-btn {
    width: 100% !important;
    font-size: 10px !important;
  }
}
</style>
