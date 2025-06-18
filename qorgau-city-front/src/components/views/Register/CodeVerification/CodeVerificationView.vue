<script setup lang="ts">
import { authService } from '@/services/auth.service'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { useUserStore } from '@stores/UserStore'
import { onMounted, ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import RegistrationLayout from '@/layouts/RegistrationLayout.vue'
const userStore = useUserStore()
const isLoading = ref<boolean>(false)
const codeVerified = ref<boolean>(false)
const code = ref<string | number>('')
const snackbarStore = useSnackbarStore()
const router = useRouter()
const codeVerificationForm = ref(null)
const phoneRules = ref([
  (v: any) => !!v || 'Номер телефона обязателен',
  (v: any) => {
    const phoneNumberPattern = /^\+77\d{9}$/
    return v.match(phoneNumberPattern) ? true : 'Некорректный формат телефона (+77...)'
  }
])

const continueButtonRef = ref<HTMLElement | null>(null)

const isValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await codeVerificationForm.value!.validate()
  return valid
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  codeVerificationForm.value?.reset()
}

const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    // Если код еще не отправлен, запускаем sendCode, иначе - verifyCode
    if (!userStore.codeSended) {
      event.preventDefault() // Предотвращаем действие Enter только здесь
      sendCode()
    } else if (!codeVerified.value && code.value.toString().length === 6) {
      event.preventDefault() // Предотвращаем действие Enter только здесь
      verifyCode()
    }
  }
}

const sendCode = async () => {
  try {
    isLoading.value = true
    const message = await authService.resendCode(userStore.codeVerificationPhoneNumber)
    isLoading.value = false
    userStore.codeSended = true
    snackbarStore.pullSnackbar(message, 3000, '#5b9271')
  } catch (e) {
    isLoading.value = false
    snackbarStore.pullSnackbar('Произошла ошибка.', 3000, '#d20f0d')
  }
}

const resendCode = async () => {
  try {
    isLoading.value = true
    const message = await authService.resendCode(userStore.codeVerificationPhoneNumber)
    isLoading.value = false
    userStore.codeSended = true
    snackbarStore.pullSnackbar(message, 3000, '#5b9271')
  } catch (e) {
    isLoading.value = false
    console.log(e)
    snackbarStore.pullSnackbar('Произошла ошибка.', 3000, '#d20f0d')
  }
}

const verifyCode = async () => {
  if ((await isValid()) && code.value.toString().length === 6) {
    try {
      isLoading.value = true
      const payload = {
        phone: userStore.codeVerificationPhoneNumber,
        code: code.value.toString()
      }

      await authService.verifySmsCode(payload)
      resetForm()
      localStorage.setItem('phone', JSON.stringify(userStore.codeVerificationPhoneNumber));
      isLoading.value = false
      snackbarStore.pullSnackbar('Смс код был подтвержден, далее заполните поля', 3000, '#5b9271')
      await router.push('/register')
    } catch (e) {
      console.log(e)
      isLoading.value = false
      snackbarStore.pullSnackbar(
        'Произошла ошибка. Возможно, вы ввели неправильный код.',
        3000,
        '#d20f0d'
      )
    }
  }
}

onMounted(async () => {
  if (userStore.isAuthenticated || localStorage.getItem('token')) {
    try {
      await userStore.getUser()
      await router.push({ name: 'Home' })
    } catch (error) {
      return
    }
  }
  window.addEventListener('keydown', handleKeyPress)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyPress) // Clean up listener on unmount
})

</script>

<template>
  <RegistrationLayout title="Подтверждение номера для">
    <!-- Step 1: Phone Number Input -->
    <div v-if="!userStore.codeSended" class="wrapper">
      <div class="back-button">
        <v-btn
          @click="() => router.push('/login')"
          prepend-icon="mdi-chevron-left"
          variant="text"
          style="text-transform: none; margin-bottom: 10px"
        >
          <span style="padding: 3px 0 0 0">Вернуться назад</span>
        </v-btn>
      </div>

      <p class="login-subtitle">Отправим на телефон уведомление для подтверждения входа</p>

      <v-form ref="loginForm" class="login-form">
        <v-text-field
          v-model="userStore.codeVerificationPhoneNumber"
          label="Телефон"
          :rules="phoneRules"
          placeholder="+7 000 000 00 00"
          variant="outlined"
          class="phone-input"
          @keyup.enter="sendCode"
        ></v-text-field>

        <v-btn
          ref="continueButtonRef"
          block
          class="login-button"
          @click="sendCode"
        >
          Продолжить
        </v-btn>
      </v-form>
    </div>

    <!-- Step 2: Code Verification -->
    <div v-if="userStore.codeSended && !codeVerified" class="wrapper">
      <h1 class="login-title">Подтверждение кода</h1>
      <p class="login-subtitle">
        Мы отправили SMS на ваш номер телефона. Введите код, указанный в этом сообщении.
      </p>

      <v-form ref="codeVerificationForm" class="login-form">
        <v-otp-input
          v-model="code"
          :length="6"
          class="code-input"
          autofocus

        ></v-otp-input>

        <v-btn
          :loading="isLoading"
          color="#f57c01"
          @click="verifyCode"
          class="text-white code-verification__button"
        >
          Подтвердить код
        </v-btn>

      </v-form>

      <a href="#" class="resend-code" @click="resendCode">Отправить код еще раз</a>
    </div>
  </RegistrationLayout>
</template>

<style scoped>
.wrapper{
  width: 100%;
  max-width: 600px;
  margin: 0 auto;

}

.login-title {
  font-size: 24px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
}

.login-subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.login-form {
  margin-bottom: 20px;
}

.phone-input, .code-input {
  margin-bottom: 20px;
}

.login-button {
  font-size: 18px;
  padding: 30px;
  background-color: #FD7E14FF;
  color: white;
  text-transform: none;
  font-weight: bold;
}
.code-verification__button{
  width: 100%;

}

.resend-code {
  font-size: 14px;
  color: #1a73e8;
  text-decoration: none;
}
</style>
