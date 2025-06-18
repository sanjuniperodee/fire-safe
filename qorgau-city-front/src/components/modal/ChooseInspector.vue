<template>
  <div
    v-if="showModal"
    class="modal-overlay"
    @click.self="toggleModal"
  >
    <div class="modal">
      <button
        @click="toggleModal"
        class="close-btn"
      >
        &times;
      </button>
      <h2 class="modal-title">Выберите инспектора</h2>
      <div class="inspectors-list">
        <v-select
            v-model="city"
            label="Город"
            :rules="rules"
            :items="cityList"
            variant="solo-filled"
            hide-details="auto"
          ></v-select>
          <v-text-field
            :rules="rules"
            v-model="district"
            label="Область"
            variant="solo-filled"
            placeholder="Пример: Есил"
            clearable
            class="form__password"
            hide-details="auto"
          ></v-text-field>

          <button
          class="req-btn"
          @click="noteComplaint"
          >
          Cделать заявление/жалобу
          </button>
        <!-- <PersonCard
          v-for="user in filteredUsers"
          :key="user.id"
          :id="user.id"
          :first_name="user.first_name"
          :last_name="user.last_name"
          :iin="user.iin"
          :email="user.email"
          :phone="user.phone"
          :avatar_url="user.avatar_url"
          :middle_name="user.middle_name"
        /> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@stores/UserStore'
import { UserRoleOptions } from '@/types/User'
import PersonCard from '@components/modal/utils/PersonCard.vue'
import { useComplaintStore } from '@/stores/ComplaintStore'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { cityList } from './utils'

const complaintStore = useComplaintStore()
const snackbarStore = useSnackbarStore()

defineProps({
  showModal: Boolean,
  propRole: String
})

const userStore = useUserStore()
const router = useRouter()

const city = ref('')
const district = ref('')

const rules = ref([(value: any) => !!value || 'Поле обязательно'])

const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const goToPage = (route: string) => {
  router.push({ name: route })
}

const noteComplaint = async () => {
  try {
    const data = {
      city: city.value,
      district: district.value
    }

    await complaintStore.createComplaint(data)
    emit('close')
    
    // Переход на страницу "Faq"
    goToPage('Faq')

    // Проверяем текущий маршрут и обновляем страницу, если мы на странице 'Faq'
    if (router.currentRoute.value.name === 'Faq') {
      location.reload()
    }
    
    snackbarStore.pullSnackbar(
      'Жалоб отправлен, жалоб добавлена в "Избранные заявки"',
      3000,
      '#5b9271'
    )
  } catch (err) {
    snackbarStore.pullSnackbar('Не удалось отправить отклик!', 3000, '#d20f0d')
    console.error(err)
  }
}

const filteredUsers = computed(() => {
  return userStore.allUsers.filter((user) =>
    user.role.some((role) => role.role === UserRoleOptions.INSPECTOR)
  )
})

onMounted(async () => {
  await userStore.getAllUsers()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 550px;
  max-height: 500px;
  overflow-y: scroll;
  position: relative;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
.modal-title {
  font-size: 18px;
  margin-bottom: 20px;
}

.form__password{
  margin-top: 10px;
}

.req-btn {
  background-color: #f37b01;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.2s ease-out;
  text-align: center;
  margin: 12px 133px;
}
.req-btn:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}

.inspectors-list {
}
</style>
