<template>
  <ImageModal
    :visible="isModalVisible"
    :imageUrl="selectedImageUrl"
    @close="closeImageModal"
  />

  <div v-if="selectedChat" class="messages" ref="messagesContainer">
    <div
      v-for="message in (selectedChat?.message_set || []).slice().reverse()"
      @click="handleMessageClick(message)"
      class="message"
      :key="message.id"
      :class="getMessageClass(message.sender)"
    >
      <!-- Отображение вложений -->
      <div v-for="file in message.attachments" :key="file.id" class="attachment">
        <!-- Изображение -->
        <img
          v-if="file?.filename?.endsWith('.jpg') || file.filename.endsWith('.png')" 
          :src="file.file"
          class="img-wrapper" 
          alt="image" 
          @click.stop="openImageModal(file.file)"
        />

        <!-- Видео -->
        <video
          v-else-if="file?.filename?.endsWith('.mp4') || file.filename.endsWith('.webm') || file.filename.endsWith('.ogg')"
          controls
          class="video-wrapper"
        >
          <source :src="file.file" :type="`video/${file.filename.split('.').pop()}`" />
          Ваш браузер не поддерживает видео.
        </video>

        <!-- Другие файлы -->
        <a
          v-else
          :href="file?.file"
          target="_blank"
          class="file-link"
        >
          <div class="file-text">  
            <img src="/computer-file.png" alt="file icon" class="file-icon" />
            <div>
              <p class="file-name">{{ file?.filename || 'Открыть файл' }}</p>
              <p class="file-size">{{ formatFileSize(file?.file_size)}}</p>
            </div>
          </div>
        </a>
      </div>
      <div class="message-content">{{ message.text }}</div>

      <div class="message-time">
        {{ formatDateForChat(message.timestamp) }}
      </div>

      <div v-if="message.sender === selectedChat.initiator.id" class="delete-option" :class="{ 'show': selectedMessage === message }">
        <button @click.stop="deleteMessage(message)">
          Удалить
          <span class="basketIcon" v-html="deleteBasket"></span>
        </button>
      </div>
    </div>

    <div v-if="props.selectedChat?.statement.status === 'ARCHIVED'" class="archived-block">
      <div class="archived-box">
        <h2>Ответьте на предложение клиента</h2>
        <p>Перейдите в заказ и откликнитесь на него — вы сразу получите контакты клиента. Не оставляйте предложение
          без ответа. Если не можете
          взять заказ, откажитесь от него.</p>
      </div>
      <div class="archived-box">
        <p>Вы отметили заказ как неподходящий.
          Причина — не подходит бюджет.</p>
      </div>
    </div>
  </div>

  <div v-else class="no-chat-selected">
    <p>Выберите чат слева, чтобы начать общение</p>
  </div>
</template>

<script setup lang="ts">
import { formatDateForChat } from '@/helpers/formatTime';
import type { ChatRoomType, Message } from '@/types/Chat'
import ImageModal from '../UI/ImageModal.vue'
import { deleteBasket } from '@/assets/svg'
import { ref, watch, onMounted, nextTick } from 'vue'
import { useChatStore } from '@stores/ChatStore'
import { authService } from '@/services/auth.service'
import { useUserStore } from '@/stores/UserStore'
const messagesContainer = ref<HTMLDivElement | null>(null);


const props = defineProps<{
  selectedChat: ChatRoomType | null;
}>();

const emit = defineEmits<{
  (e: 'openImageModal', url: string): void
  (e: 'deleteMessage', message: Message): void
}>();


const isModalVisible = ref(false);
const selectedImageUrl = ref('');
const selectedMessage = ref<Message | null>(null);


const userStore = useUserStore()

const getMessageClass = (senderId: number | string) => {
  if (!props.selectedChat) return '';

  if(senderId === props.selectedChat.initiator.id && userStore.user!.phone === props.selectedChat.initiator.phone){
    return 'user'
  }
  else if(senderId === props.selectedChat.receiver.id && userStore.user!.phone === props.selectedChat.receiver.phone) {
    return 'user'
  }
  else {
    return 'other'
  }
};

const openImageModal = (url: string) => {
  selectedImageUrl.value = url;
  isModalVisible.value = true;
};

const closeImageModal = () => {
  isModalVisible.value = false;
};

const handleMessageClick = (message: Message) => {
  if (message.sender === props.selectedChat?.initiator.id) {
    selectedMessage.value = selectedMessage.value === message ? null : message;
  }
};

const deleteMessage = (message: Message) => {
  console.log('Selected message for deletion:', message);
  emit('deleteMessage', message);
  selectedMessage.value = null;
};

const formatFileSize = (bytes: number) =>  {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let index = 0;

  // Пока размер больше 1024 и есть следующий размерный индекс, продолжаем делить на 1024
    while (bytes >= 1024 && index < units.length - 1) {
      bytes /= 1024;
      index++;
    }

    return `${bytes.toFixed(2)} ${units[index]}`;
  }

  const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    } else {
      console.warn('messagesContainer is not available');
    }
  });
  };

  onMounted(() => {
    scrollToBottom();
  });

  watch(
  () => props.selectedChat?.message_set,
  async (newMessages) => {
    if (newMessages) {
      await nextTick(); // Ждём рендера DOM
      scrollToBottom();
    }
  }
);

</script>

<style scoped>
.messages {
  /* display: flex;
  flex-direction: column;
  justify-content: flex-end; */
  overflow-y: auto;
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f4f7f9;
  height: 100%;
  min-height: 0;
}

.message {
  position: relative;
  max-width: 70%;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}
  .message-content{
    display: flex;
    width: 100%;
    padding-top: 5px;
  }

  .img-wrapper {
  max-width: 200px;
  max-height: 150px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 5px;
}

.video-wrapper {
  max-width: 300px;
  max-height: 200px;
  border-radius: 5px;
  margin-top: 5px;
}

.file-link {
  display: inline-block;
  padding: 10px 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  margin-top: 5px;
}

.file-link:hover {
  background-color: #f0f0f0;
}

.file-icon {
    width: 24px;
    height: 24px;
    margin-right: 10px;
  }
 

.message.user {
  align-self: flex-end;
  background-color: #8fbcf5;
  color: white;
  margin-left: auto;
  width: fit-content;
  border-radius: 10px 10px 0 10px;
}

.message.user .message-time {
  color: #24292e;
}

.message.other {
  background-color: #e6e6e6;
  color: #333;
  width: fit-content;
  max-width: 500px;
  border-radius: 10px 10px 10px 0;
}

.message-time {
  font-size: 0.8em;
  color: #888;
  text-align: right;
  margin-top: 8px;
}

.img-wrapper {
  width: 200px;
  height: auto;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
  cursor: pointer;
}

.no-chat-selected {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background-color: #f4f7f9;
  color: #666;
  font-size: 1.2em;
}

.delete-option {
  position: absolute;
  top: 0;
  right: 110%;
  background-color: #f2f5f7;
  color: #212121;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  padding: 5px 10px;
  border-radius: 5px;
  display: none;
}

.delete-option.show {
  display: block;
}

.delete-option button {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 16px;
  background: none;
  border: none;
  cursor: pointer;
}

.file-text{
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .file-name {
    color: #333;
    font-weight: 500;
  }

  .file-size{
    color: #333;
    font-weight: 500;
    font-size: 12px;
    padding-top: 5px;
  }

  .archived-block {
  /* position: fixed; */
  max-width: 400px;
  margin: auto;
  display: flex;
  padding-top: 50px;
  gap: 16px;
  flex-direction: column;
  background-color: #f4f7f9;
  border-radius: 8px;
  z-index: 2;
}

.archived-box {
  padding: 16px;
  background-color: #f4f7f9;
  border-radius: 8px;
  border: 1px solid #D4D4D4;
  /* box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); */
  text-align: center;
}

.archived-box h2 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.archived-box p {
  margin: 0;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}


</style>