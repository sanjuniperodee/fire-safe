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
      <h2 class="modal-title">Cвязаться с инспектором</h2>
      <div class="modal-actions">
        <ChooseInspector
          :showModal="showChooseModal"
          @close="toggleChooseModal"
        />
        <button
          class="req-btn"
          @click="toggleChooseModal"
        >
          Cделать заявление/жалобу
        </button>
        <button
          class="req-btn"
          @click="goToPage('Chat')"
        >
          Cообщить о пожаре 112
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import ChooseInspector from '@components/modal/ChooseInspector.vue'
import { ref } from 'vue'

const router = useRouter()

defineProps({
  showModal: Boolean
})

const showChooseModal = ref(false)
const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const toggleChooseModal = () => {
  showChooseModal.value = !showChooseModal.value
}

const goToPage = async (route: string) => {
  await router.push({ name: route })
  emit('close')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 550px;
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
.modal-actions {
  display: flex;
  justify-content: space-around;
}
.req-btn {
  background-color: #f37b01;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.2s ease-out;
}
.req-btn:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}
</style>
