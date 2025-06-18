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
      <h2 class="modal-title">Выберите поставщика</h2>
      <div class="inspectors-list">
        <PersonCard
          v-for="user in filteredUsers"
          @click="(e) => goToCard(e, user.id)"
          :key="user.id"
          :id="user.id"
          :first_name="user.first_name"
          :last_name="user.last_name"
          :iin="user.iin"
          :email="user.email"
          :phone="user.phone"
          :avatar_url="user.avatar_url"
          :middle_name="user.middle_name"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/UserStore'
import { UserRoleOptions } from '@/types/User'
import PersonCard from '@components/modal/utils/PersonCard.vue'

defineProps({
  showModal: Boolean,
  propRole: String
})

const userStore = useUserStore()
const router = useRouter()

const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const filteredUsers = computed(() => {
  return userStore.allUsers.filter((user) =>
    user.role.some((role) => role.role === UserRoleOptions.PROVIDER)
  )
})

const goToCard = (e: any, cardId: number) => {
  if (e.target.className.split(' ')[0] !== 'mdi-dots-horizontal') {
    router.push('/providers/view/' + cardId)
  }
}
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
  background: rgba(0, 0, 0, 0.5);
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

.inspectors-list {
}
</style>
