<template>
  <div class="chat-window">
    <ChatHeader :selectedChat="props.selectedChat" />
    <MessageList :selectedChat="props.selectedChat" />
    <MessageInput
      :selectedChat="props.selectedChat"
      @sendMessage="sendMessage"
      @uploadFile="uploadFile"
      @updateStatus="updateStatus"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import type { ChatRoomType, Message, SendMessage, Files } from '@/types/Chat'
import ChatHeader from './ChatHeader.vue'
import MessageList from './MessageList.vue'
import MessageInput from './MessageInput.vue'
import { useChatStore } from '@stores/ChatStore'
import { chatWebSocketService } from '@/services/chat.service'
import { useComplaintStore } from '@stores/ComplaintStore'
import type { ComplaintRoomType } from '@/types/Complaint'
import { useSnackbarStore } from '@stores/SnackbarStore'

const props = defineProps<{
  selectedChat: ChatRoomType | null
  selectedComplaint: ComplaintRoomType | null
}>()

const emit = defineEmits<{
  (e: 'update-status', previewStatus: string, newStatus: string): void
}>()

const chatStore = useChatStore()
const complaintStore = useComplaintStore()
const uploadedMedia = ref<File | null>(null)
const mediaShow = ref<string | null>(null)
const snackbarStore = useSnackbarStore()

const selectedChat = ref<ChatRoomType | null>(null)

const tabTranslations: Record<string, string> = {
  OPENED: 'открыто',
  IN_WORK: 'в работе',
  COMPLETED: 'выполнено',
  ARCHIVED: 'в архиве'
}

const uploadFile = (file: File | null, preview: string | null) => {
  uploadedMedia.value = file
  mediaShow.value = preview
}

const sendMessage = async (text: string) => {
  if (text.trim() && props.selectedChat) {
    const conversationId = props.selectedChat.id
    const message: SendMessage = {
      conversation_id: props.selectedChat.id,
      sender: props.selectedChat.receiver.id,
      text: text,
      files: [],
      timestamp: new Date()
    }

    if (uploadedMedia.value) {
      const uploadedFile = await chatStore.uploadFile(conversationId, uploadedMedia.value)

      if (uploadedFile) {
        // Добавляем файл в message.files
        message.files?.push(uploadedFile as Files) // Явное приведение типа для uploadedFile
      }
    }

    try {
      await chatStore.sendMessage(message)
    } catch (error) {
      console.error('Ошибка при отправке сообщения:', error)
    }
  }

  if (uploadedMedia.value) {
    console.log('uploadedMedia', uploadedMedia.value)
    // ОТПРАВКА МЕДИА
  }

  uploadedMedia.value = null
  mediaShow.value = null
}

const updateStatus = async (status: string) => {
  try {
    if (props.selectedChat) {
      console.log(props.selectedChat.statement.id)
      console.log(status)
      await complaintStore.updateChangeStatementStatus(
        props.selectedChat.statement.id ?? null,
        status
      )
      emit('update-status', props.selectedChat.status, status)
      snackbarStore.pullSnackbar(
        'Статус объекта успешно изменен на' + tabTranslations[status],
        3000,
        '#5b9271'
      )
      // location.reload();
    }
  } catch (error) {
    console.log(error)
  }
}

watch(
  () => chatStore.message as Message,
  (newMessage: Message) => {
    props.selectedChat?.message_set.unshift(newMessage)
  }
)
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}
</style>
