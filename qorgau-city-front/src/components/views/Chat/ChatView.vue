<template>
  <div>
    <!-- <LoaderSpinner  v-if="isLoading" /> -->
    <div class="chat-container">
      <RoomsNavbar
        :selectedChat="chatStore.chatRoom"
        :chat-rooms="chatStore.chatRooms"
        @select-chat="selectChat"
        @update-status="updateStatus"
      />

      <ChatWindow
        :selectedChat="chatStore.chatRoom"
        :selectedComplaint="complaintStore.complaintRoom"
        @update-status="updateChatStatus"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import RoomsNavbar from './RoomsNavbar.vue'
import ChatWindow from './chatWindow/ChatWindow.vue'
import type { ChatRoomType, Message } from '@/types/Chat'
import { useChatStore } from '@stores/ChatStore'
import { chatWebSocketService } from '@/services/chat.service'
import { useRoute } from 'vue-router'
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'
import { useComplaintStore } from '@/stores/ComplaintStore'

const route = useRoute()
const chatStore = useChatStore()
const selectedChat = ref<ChatRoomType | null>(null)
const messageChat = ref<Message | null>(null)
const isLoading = ref(false)
const complaintStore = useComplaintStore()
const status = ref('OPENED')

const updateStatus = (newStatus: string) => {
  console.log('updated', newStatus)
  status.value = newStatus
}

const updateChatStatus = (previewStatus: string, newStatus: string) => {
  console.log('updated', newStatus)
  chatStore.getAllChatRooms(previewStatus)
}

const selectChat = async (id: number) => {
  // Disconnect from the current WebSocket connection if it's active

  if (selectedChat.value) {
    chatWebSocketService.disconnect()
  }

  try {
    isLoading.value = true
    await chatStore.getChatRoomById(id)
    selectedChat.value = chatStore.chatRoom

    isLoading.value = false
    if (selectedChat.value) {
      await chatWebSocketService.connect(selectedChat.value.id)
    } else {
      console.error('Error connecting to WebSocket:')
    }
  } catch (error) {
    console.error(error)
    isLoading.value = false
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await chatStore.getAllChatRooms(status.value)
  if (chatStore.lastChatRoom) {
    await selectChat(chatStore.lastChatRoom.id)
  }
})

watch(
  status,
  async (newStatus) => {
    await chatStore.getAllChatRooms(newStatus)
  },
  { immediate: true }
)

// watch(() => chatStore.chatRooms, (newChatRooms) => {
//   if (!selectedChat.value && newChatRooms.length > 0) {
//     selectChat(chatStore.lastChatRoom!.id)
//   }
// }, { deep: true })
</script>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 56px);
  font-family: Arial, sans-serif;
  background: #f4f7f9;
}
</style>
