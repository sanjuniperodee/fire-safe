<template>
  <div class="login-parent">
    <div class="login">
      <div class="login__logo"></div>

      <div class="login__box">
        <div class="login__image">
          <img
            src="/login-logo.jpg"
            alt=""
          />
        </div>
        <v-form
          ref="loginForm"
          @submit.prevent="handlerSubmit"
          action=""
          class="login__form form"
        >
          <div class="form__box">
            <div class="form__title">{{ $t('loginTitle') }}</div>
            <div class="form__subtitle">
              {{ $t('registerLink') }}
              <RouterLink
                :to="{ name: 'CodeVerification' }"
                style="text-decoration: underline"
              >
                <v-btn
                  variant="tonal"
                  color="#f57c01"
                  class="ml-1 text-capitalize"
                  >{{ $t('registerLink') }}</v-btn
                >
              </RouterLink>
            </div>
          </div>
          <div
            class="w-100 text-black"
            style="display: flex; flex-direction: column; gap: 1em"
          >
            <v-text-field
              :rules="phoneRules"
              :loading="isLoading"
              class="form__login"
              :label="$t('phoneNumberLabel')"
              v-model="number"
              clearable
              variant="outlined"
              hide-details="auto"
              type="text"
              v-maska:[options]
            ></v-text-field>
            <v-text-field
              :rules="passwordRules"
              :loading="isLoading"
              :label="$t('passwordLabel')"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              clearable
              class="form__password"
              hide-details="auto"
              :counter="20"
              :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append="togglePasswordVisibility"
            ></v-text-field>
          </div>
          <span
            @click="() => router.push('/forgot-password')"
            class="forgot-password"
            >{{ $t('forgotPassword') }}</span
          >
          <span
            @click="() => router.push('/code-verification')"
            class="forgot-password"
            >{{ $t('activateAccount') }}</span
          >
          <v-btn
            :loading="isLoading"
            color="#f57c01"
            class="w-100 text-white text-capitalize form-submit-btn"
            type="submit"
            rounded="0"
            size="large"
            >{{ $t('loginButton') }}</v-btn
          >
        </v-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import { useUserStore } from '@stores/UserStore'
import { useRouter } from 'vue-router'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { authService } from '@/services/auth.service'
import { type LoginValidator } from '@/types/Auth'

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

import { vMaska } from 'maska'
import { ChatLogin } from '@views/Chat/ChatAuth'
const options = { mask: '+77#########' }
const i18n = useI18n()

const currentLanguage = ref('ru') // Define as reactive ref

const setLanguage = (locale: string) => {
  i18n.locale.value = locale
  currentLanguage.value = locale
}

const router = useRouter()

const userStore = useUserStore()
const snackbarStore = useSnackbarStore()
const loginForm = ref(null)
let showPassword = ref(false)

const number = ref('')
const password = ref('')
const isLoading = ref<boolean>(false)

const isValid = async () => {
  // @ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await loginForm.value!.validate()
  return valid
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  loginForm.value?.reset()
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const phoneRules = ref([
  (v: any) => !!v || 'Номер телефона обязателен',
  (v: any) => {
    const phoneNumberPattern = /^\+77\d{9}$/ // Match the pattern for +77 followed by 9 digits
    return v.match(phoneNumberPattern) ? true : 'Некорректный формат телефона (+77...)'
  }
])

const passwordRules = ref([
  (v: any) => !!v || 'Пароль обязателен',
  (v: any) => (v && v.length >= 1) || 'Пароль должен быть более чем 8 символов',
  (v: any) => (v && v.length <= 20) || 'Пароль должен быть менее чем 20 символов'
])
const handlerSubmit = async () => {
  const body: LoginValidator = {
    phone: number.value,
    password: password.value
  }

  if (await isValid()) {
    try {
      isLoading.value = true
      const message = await authService.login(body)
      userStore.isAuthenticated = true
      isLoading.value = false
      resetForm()
      await router.push({ name: 'Home' })
      snackbarStore.pullSnackbar(message, 3000, '#5b9271')
    } catch (e) {
      console.log('error', e)
      isLoading.value = false
      snackbarStore.pullSnackbar('Не удалось войти.', 3000, '#d20f0d')
    }
  } else {
    snackbarStore.pullSnackbar('Введите все поля корректно.', 3000, '#d20f0d')
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

.login-parent {
  height: 100vh;
  overflow-y: scroll;
}

.forgot-password {
  color: #343434;

  &:hover {
    text-decoration: underline;
  }
}

.login {
  padding: 40px 0;
  background-color: $white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100%;

  &__logo {
    font-size: 45px;
    font-family: 'Overpass', sans-serif;
    letter-spacing: 1px;
    color: $orange;
    margin-bottom: 1em;
  }

  &__box {
    filter: drop-shadow(0.4em 0.4em 0.4em #0000002f);
    border-radius: 1em;
    padding: 40px;
    background-color: #fff;
    display: flex;
    align-items: center;
    color: #000;
    width: 1000px;
  }

  &__image {
    width: 50%;
    height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;

    & img {
      border-radius: 1em;
      height: 400px;
    }
  }

  &__form {
    width: 50%;
    justify-content: center;
    // height: 100%;
    display: flex;
    gap: 1em;
    flex-direction: column;
    align-items: center;
  }
}

.form {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 1em;

  &__box {
    display: flex;
    gap: 0.7em;
    flex-direction: column;
    align-items: center;
  }

  &__title {
    color: #000;
    text-align: center;
    font-size: 32px;
    letter-spacing: 1px;
    font-family: 'Overpass', sans-serif;
    color: #000;
  }

  &__subtitle {
    text-align: center;
    font-family: 'Overpass', sans-serif;
    font-size: 16px;
    color: #000;

    & a {
      color: #000;
    }
  }

  &__login {
    width: 100%;
  }

  &__password {
    width: 100%;
  }
}

@media only screen and (max-width: 1024px) {
  .login {
    &__image {
      height: 150px;

      & img {
        height: 150px;
      }
    }

    &__box {
      flex-direction: column;
      gap: 2em;
      width: 300px;
    }
  }

  .form {
    width: 90%;

    &__title {
      font-size: 20px;
    }

    &__subtitle {
      line-height: 1.4em;
    }
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
</style>
