<template>
  <RegisterLayout title="Регистрация для">
    <LoaderSpinner v-if="isLoading" />

    <div class="register-container">
      <div class="register">
        <keep-alive>
          <component
            :is="activeTabComponent"
            v-bind="formData"
            @updateData="updateFormData"
          />
        </keep-alive>

        <div class="navigation-buttons">
          <v-btn
            v-if="activeTab !== 'step1'"
            @click="prevStep"
            color="grey lighten-1"
            class="mr-4"
          >
            Назад
          </v-btn>
          <v-btn
            v-if="activeTab !== 'step3'"
            @click="nextStep"
            color="#FD7E14FF"
          >
            Далее
          </v-btn>
          <v-btn
            v-if="activeTab === 'step3'"
            @click="submitForm"
            color="primary"
          >
            Завершить
          </v-btn>
        </div>
      </div>
    </div>
  </RegisterLayout>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import RegisterLayout from '@/layouts/RegistrationLayout.vue'
import Step1 from './steps/GeneralInfo.vue'
import Step2 from './steps/RoleSelect.vue'
import Step3 from './steps/ForVerification.vue'
import { authService } from '@/services/auth.service'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { useRouter } from 'vue-router'
import type { RegisterValidator } from '@/types/Auth'
import { UserRoleOptions } from '@/types/User'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'
import { ChatRegistration } from '@views/Chat/ChatAuth'

const activeTab = ref('step1')

const formData = ref<RegisterValidator>({
  birthdate: '',
  email: '',
  first_name: '',
  iin: '',
  last_name: '',
  middle_name: '',
  role: UserRoleOptions.CITIZEN,
  phone: '',
  password: '',
  password2: ''
})

const snackbarStore = useSnackbarStore()
const router = useRouter()
const isLoading = ref(false)

const switchTab = (tab: string) => {
  activeTab.value = tab
}

const activeTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'step1':
      return Step1
    case 'step2':
      return Step2
    case 'step3':
      return Step3
    default:
      return Step1
  }
})

const nextStep = () => {
  if (activeTab.value === 'step1') {
    switchTab('step2')
  } else if (activeTab.value === 'step2') {
    switchTab('step3')
  }
}
const prevStep = () => {
  if (activeTab.value === 'step2') {
    switchTab('step1')
  } else if (activeTab.value === 'step3') {
    switchTab('step2')
  }
}

const updateFormData = (newData: any) => {
  formData.value = { ...formData.value, ...newData }
}

const submitForm = async () => {
  isLoading.value = true

  const chatPayload = ref({
    phone: formData.value.phone,
    password1: formData.value.password,
    password2: formData.value.password2
  })
  try {
    const response = await authService.register(formData.value)
    console.log(response)

    snackbarStore.pullSnackbar('Регистрация прошла успешно!', 3000, '#5b9271')
    isLoading.value = false
    await router.push('/login')
  } catch (err: any) {
    console.error('Ошибка регистрации:', err)

    let errorMessage = 'Не удалось зарегистрировать.'

    try {
      // Check if err.message contains a JSON string and parse it
      const errorData = JSON.parse(err.message)

      if (errorData) {
        const firstError = Object.values(errorData).flat()[0] // Extract the first error message
        if (firstError) {
          errorMessage = String(firstError)
        }
      }
    } catch (parseError) {
      console.error('Ошибка парсинга JSON:', parseError)
    }

    snackbarStore.pullSnackbar(errorMessage, 3000, '#d20f0d')
  } finally {
    isLoading.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.register {
  width: 100%;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.navigation-buttons > *:only-child {
  margin-left: auto;
  justify-content: flex-end;
}

.step-indicator {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.step {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #e0e0e0;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 5px;
  font-weight: bold;
  transition: background-color 0.3s ease;

  &.active {
    background-color: #1976d2;
  }
}
</style>
