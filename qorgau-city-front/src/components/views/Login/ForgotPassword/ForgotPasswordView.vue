<template>
  <div class="forgot-password-parent">
    <div class="forgot-password">
      <div class="back-button">
        <v-btn
          @click="() => router.push('/login')"
          prepend-icon="mdi-chevron-left"
          variant="text"
          style="text-transform: none; margin-bottom: 10px"
        >
          <span style="padding: 3px 0 0 0">Вернуться к авторизации</span>
        </v-btn>
      </div>
      <v-card class="forgot-password__box">
        <v-card-title>Забыли пароль?</v-card-title>
        <!-- 1 step -->
        <v-form
          ref="sendSmsForm"
          v-if="!codeSended"
        >
          <v-card-text style="color: #000"
            >Введите номер телефона вашего аккаунта, чтобы подтвердить вашу личность.</v-card-text
          >
          <v-text-field
            :rules="phoneRules"
            :loading="isLoading"
            class="forgot-password__input"
            label="Номер телефона"
            v-model="phone"
            clearable
            variant="outlined"
            :disabled="isLoading"
            hide-details="auto"
            type="text"
            color="#f57c01"
          ></v-text-field>
          <div style="display: flex; justify-content: end">
            <v-btn
              :loading="isLoading"
              :disabled="isLoading"
              color="#f57c01"
              @click="() => sendSmsCode()"
              class="text-white forgot-password__button"
              >Отправить код</v-btn
            >
          </div>
        </v-form>
        <!-- 2 step -->
        <div v-if="codeSended && !codeVerified">
          <v-card-text style="color: #000"
            >Мы вам отправили SMS на ваш номер телефона, напишите код указанный в этом
            сообщении.</v-card-text
          >
          <v-otp-input
            v-model="code"
            :disabled="isLoading"
            :loading="isLoading"
            color="#f57c01"
            length="6"
          ></v-otp-input>
          <div style="display: flex; justify-content: end">
            <v-btn
              :loading="isLoading"
              color="#f57c01"
              @click="() => verifySmsCode()"
              class="text-white forgot-password__button"
              >Подтвердить код</v-btn
            >
          </div>
        </div>
        <!-- 3 step -->
        <v-form
          ref="passwordForm"
          v-if="codeVerified"
        >
          <v-card-text style="color: #000"
            >Мы подтвердили вашу личность, теперь вы можете изменить ваш пароль</v-card-text
          >
          <v-text-field
            :rules="passwordRules"
            :disabled="isLoading"
            :loading="isLoading"
            label="Новый пароль"
            v-model="newPassword"
            variant="outlined"
            placeholder="Введите новый пароль"
            clearable
            class="forgot-password__input"
            hide-details="auto"
            type="password"
            :counter="20"
            color="#f57c01"
          ></v-text-field>
          <v-text-field
            :rules="passwordRules"
            :disabled="isLoading"
            :loading="isLoading"
            label="Подтверждение нового пароля"
            v-model="newPasswordRepeat"
            variant="outlined"
            placeholder="Повторите новый пароль"
            clearable
            class="forgot-password__input"
            hide-details="auto"
            type="password"
            color="#f57c01"
            :counter="20"
          ></v-text-field>
          <div style="display: flex; justify-content: end">
            <v-btn
              :disabled="isLoading"
              :loading="isLoading"
              color="#f57c01"
              @click="() => forgotPassword()"
              class="text-white forgot-password__button"
              >Изменить пароль</v-btn
            >
          </div>
        </v-form>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { authService } from '@/services/auth.service'
import {
  type ForgotPasswordPayload,
  type SendSmsCodePayload,
  type VerifySmsCodePayload
} from '@/types/Auth'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const snackbarStore = useSnackbarStore()

const router = useRouter()
const isLoading = ref<boolean>(false)
const codeSended = ref<boolean>(false)
const codeVerified = ref<boolean>(false)
const phone = ref<string>('+77')
const code = ref<number>(0)
const newPassword = ref<string>('')
const newPasswordRepeat = ref<string>('')

const sendSmsForm = ref(null)
const passwordForm = ref(null)

const phoneRules = ref([
  (v: any) => !!v || 'Номер телефона обязателен',
  (v: any) => {
    const phoneNumberPattern = /^\+77\d{9}$/ // Match the pattern for +77 followed by 9 digits
    return v.match(phoneNumberPattern) ? true : 'Некорректный формат телефона (+77...)'
  }
])

const passwordRules = ref([
  (v: any) => !!v || 'Пароль обязателен',
  (v: any) => (v && v.length >= 8) || 'Пароль должен быть более чем 8 символов',
  (v: any) => (v && v.length <= 20) || 'Пароль должен быть менее чем 20 символов'
])

const isSendSmsValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await sendSmsForm.value!.validate()
  return valid
}

const isPasswordValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await passwordForm.value!.validate()
  return valid
}

const sendSmsCode = async () => {
  if (await isSendSmsValid()) {
    try {
      isLoading.value = true
      const payload: SendSmsCodePayload = {
        phone: phone.value
      }
      const message = await authService.sendSmsCode(payload)
      isLoading.value = false
      codeSended.value = true
      snackbarStore.pullSnackbar(message, 3000, '#5b9271')
    } catch (e) {
      isLoading.value = false
      snackbarStore.pullSnackbar(
        'Произошла ошибка. Возможно, вы ввели некорректный номер.',
        3000,
        '#d20f0d'
      )
    }
  }
}

const verifySmsCode = async () => {
  if (code.value.toString().length === 6) {
    try {
      isLoading.value = true
      const payload: VerifySmsCodePayload = {
        code: code.value.toString(),
        phone: phone.value
      }
      const message = await authService.verifySmsCode(payload)
      isLoading.value = false
      codeVerified.value = true
      snackbarStore.pullSnackbar(message, 3000, '#5b9271')
    } catch (e) {
      isLoading.value = false
      snackbarStore.pullSnackbar(
        'Произошла ошибка. Возможно, вы ввели некорректный код подтверждения.',
        3000,
        '#d20f0d'
      )
    }
  } else {
    snackbarStore.pullSnackbar('Длина кода подтверждения должна быть из 6 цифр.', 3000, '#d20f0d')
    code.value = 0
  }
}

const forgotPassword = async () => {
  if ((await isPasswordValid()) && newPassword.value.trim() === newPasswordRepeat.value.trim()) {
    try {
      isLoading.value = true
      const payload: ForgotPasswordPayload = {
        phone: phone.value,
        password: newPassword.value
      }
      const message = await authService.forgotPassword(payload)
      isLoading.value = false
      await router.push('/login')
      snackbarStore.pullSnackbar(message, 3000, '#5b9271')
    } catch (e) {
      isLoading.value = false
      snackbarStore.pullSnackbar('Произошла ошибка. Попробуйте позже.', 3000, '#d20f0d')
    }
  }
}
</script>

<style lang="scss" scoped>
.back-button {
  width: 500px;
}

.forgot-password-parent {
  height: 100vh;
  overflow-y: scroll;
}

.forgot-password {
  padding: 40px 0;
  background-color: $white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100%;

  &__box {
    border-radius: 1em;
    padding: 10px;
    background-color: #fff;
    display: flex;
    flex-direction: column;
    color: #000;
    width: 500px;
  }

  &__input {
    margin: 10px 15px;
  }

  &__button {
    margin: 5px 15px;
    width: fit-content;
    padding: 0 20px;
    text-transform: none;
  }
}

::-webkit-scrollbar {
  width: 13px;

  background-color: $white;

  &-track {
    background-color: $white;
    margin-block: 0.5em;
  }

  &-thumb {
    background-color: rgba(47, 47, 47, 0.836);
    border-radius: 100vw;
    transition: 0.4s;
    border: 4px solid $white;
    background-clip: padding-box;

    &:hover {
      background-color: rgb(28, 28, 28);
      transition: 0.4s;
    }
  }
}

@media only screen and (max-width: 550px) {
  .back-button {
    width: 80%;
  }

  .forgot-password {
    &__box {
      width: 80%;
    }
  }
}
</style>
