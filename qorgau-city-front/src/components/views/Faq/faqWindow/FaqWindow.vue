<template>
  <div class="chat-window">
    <FaqHeader :selectedChat="props.selectedChat"
    :selectedComplaint="complaintStore.complaintRoom" />
    <MessageList 
      :selectedChat="props.selectedChat"
      :selectedComplaint="props.selectedComplaint"
    />
    <MessageInput
      :selectedChat="props.selectedChat"
      :selectedComplaint="props.selectedComplaint"
      @sendMessage="sendMessage"
      @uploadFile="uploadFile"
      @markAsAnswered="markAsAnswered"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, toRaw } from 'vue'
import type { ChatRoomType, Message, SendMessage, Files, FileContent } from '@/types/Chat'
import FaqHeader from './FaqHeader.vue'
import MessageList from './MessageList.vue'
import MessageInput from './MessageInput.vue'
import { useChatStore } from '@stores/ChatStore'
import { useComplaintStore } from '@stores/ComplaintStore'
import { chatWebSocketService } from '@/services/chat.service'
import type { ComplaintRoomType } from '@/types/Complaint'

const props = defineProps<{
  selectedChat: ChatRoomType | null
  selectedComplaint: ComplaintRoomType | null
}>();

const chatStore = useChatStore()
const complaintStore = useComplaintStore()
const uploadedMedia = ref<File | null>(null);
const mediaShow = ref<string | null>(null);

const emit = defineEmits<{
  (e: 'update-status', status: string): void;
}>();

const uploadFile = (file: File | null, preview: string | null) => {
  uploadedMedia.value = file;
  mediaShow.value = preview;
};

const sendMessage = async (text: string) => {
  if (text.trim() && props.selectedChat) {
    const conversationId = props.selectedChat.id;
    const message: SendMessage = {
      conversation_id: props.selectedChat.id,
      sender: props.selectedChat.receiver.id,
      text: text,
      files: [],
      timestamp: new Date(),
    };

    if (uploadedMedia.value) {
      const uploadedFile = await complaintStore.uploadFile(conversationId, uploadedMedia.value);

      if (uploadedFile) {
        // Добавляем файл в message.files
        message.files?.push(uploadedFile as Files);  // Явное приведение типа для uploadedFile
      }
    }

    try {
      await complaintStore.sendMessage(message);
    } catch (error) {
      console.error("Ошибка при отправке сообщения:", error);
    }
  }

  uploadedMedia.value = null;
  mediaShow.value = null;
};

const markAsAnswered = async () => {
  try {
    if (toRaw(props.selectedChat)) {
      await complaintStore.createMarkAsAnswered(props.selectedComplaint?.id ?? null);
      emit('update-status', 'ANSWERED');
      location.reload();
    }
  } catch (error) {
    console.log(error);
  }
};

watch(() => chatStore.message as Message, (newMessage: Message) => {
  if (props.selectedChat && props.selectedChat.message_set) {
    props.selectedChat.message_set.unshift(newMessage);
  }
});
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}
</style>