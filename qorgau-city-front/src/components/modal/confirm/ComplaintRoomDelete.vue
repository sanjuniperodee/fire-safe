<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useChatStore } from '@stores/ChatStore'
import { useComplaintStore } from '@/stores/ComplaintStore';
import { chatWebSocketService } from '@/services/chat.service'
import type { ChatRoomType, Message } from '@/types/Chat'

const complaintStore = useComplaintStore()
const chatStore = useChatStore()
const isLoading = ref(false)
const selectedChat = ref<ChatRoomType | null>(null);

const props = defineProps<{
  chatId: number
  showModal: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const toggleModal = () => {
  emit('close')
}

const deleteChatRoom = async() => {
  isLoading.value = true
  try {
    await chatWebSocketService.disconnect();

    await complaintStore.removeComplaint(props.chatId)
    emit('close')
    location.reload()
  } catch (error) {
    console.error('Error deleting chat room:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
<div class="modal-wrapper" v-if="showModal">
  <div class="modal-content">
    <v-card style="font-family: 'Overpass', sans-serif">
      <v-card-title class="text-center"><b>Вы уверены что хотите удалить чат?</b></v-card-title>
      <v-card-actions>
        <v-btn
          :loading="isLoading"
          class="d-flex align-center ga-3"
          style="width: 50%"
          @click="deleteChatRoom"
          color="#d20f0d"
          prepend-icon="mdi-delete"
          :disabled="isLoading"
          stacked
        >
          Удалить
        </v-btn>
        <v-btn
          @click="toggleModal"
          class="d-flex align-center ga-3"
          style="width: 50%"
          color="#d20f0d"
          prepend-icon="mdi-cancel"
          stacked
        >
          Отмена
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</div>
</template>

<style scoped lang="scss">
.text-center{
    font-size: 18px;
    font-weight: 300;
}
.modal-wrapper{
  position: fixed;
  top: 0;
  left: 0;
  width: 100dvw;
  height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1000;

  &.modal-content{
    max-width: 600px;
    width: 350px;
    min-height: 250px;
    padding: 20px;
  }
}
</style>