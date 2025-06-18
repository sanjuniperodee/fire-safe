<template>
  <div v-if="!userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER) && selectedChat && props.selectedComplaint?.status === 'PENDING'" class="message-input">
    <button @click="emit('markAsAnswered')" class="complaint-btn">Жалоба отработана</button>
  </div>
  <div v-if="selectedChat">
    <div v-if="props.selectedComplaint?.status !== 'EXPIRED' && props.selectedComplaint?.status !== 'NOT_ANSWERED'" class="message-input">
    <div v-if="uploadedFile" class="uploaded-file-preview">
      <img v-if="fileType === 'image'" :src="filePreview!" alt="uploaded" class="preview-image" />
      <video v-else-if="fileType === 'video'" :src="filePreview!" controls class="preview-video"></video>
      <div v-else class="preview-file">
        <img src="/computer-file.png" alt="file icon" class="file-icon" />
        <span>{{ uploadedFile.name }}</span>
      </div>
      <button @click="removeFile" class="remove-file-btn" v-html="close"></button>
    </div>

    <span class="custom-file-upload">
      <input class="file-input" type="file" accept="application/word, application/vnd.ms-excel, application/vnd.ms-powerpoint,
                  text/plain, application/pdf, image/*, video/*" :disabled="isUploadLoading" @change="uploadFile" />
      <span v-html="paperclip" class="paperclipIcon"></span>
    </span>

    <input v-model="textMessage" @keyup.enter="sendMessage" placeholder="Введите сообщение..." />
    <button @click="sendMessage" class="send-btn">Отправить</button>
    </div>
    <div v-else="props.selectedComplaint?.status === 'EXPIRED' && props.selectedComplaint?.status === 'NOT_ANSWERED'" class="message-input">
      <p class="text-archived">Вы не можете писать в этот чат</p>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ChatRoomType } from '@/types/Chat'
import { paperclip, close } from '@/assets/svg'
import { chatWebSocketService } from '@/services/chat.service'
import type { ComplaintRoomType } from '@/types/Complaint';
import { useUserStore } from '@/stores/UserStore'
import { UserRoleOptions } from '@/types/User'

const props = defineProps<{
  selectedChat: ChatRoomType | null;
  selectedComplaint: ComplaintRoomType | null
  
}>();

const emit = defineEmits<{
  (e: 'sendMessage', text: string): void
  (e: 'uploadFile', file: File | null, preview: string | null): void
  (e: 'markAsAnswered'): void
}>();

const userStore = useUserStore()
const textMessage = ref('');
const isUploadLoading = ref(false);
const uploadedFile = ref<File | null>(null);
const filePreview = ref<string | null>(null);

const fileType = computed(() => {
  if (!uploadedFile.value) return null;
  if (uploadedFile.value.type.startsWith('image/')) return 'image';
  if (uploadedFile.value.type.startsWith('video/')) return 'video';
  return 'other';
});


const uploadFile = (e: Event) => {
  isUploadLoading.value = true;

  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (files && files.length > 0) {
    uploadedFile.value = files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      filePreview.value = reader.result as string;
      emit('uploadFile', uploadedFile.value!, filePreview.value);
    };

    if (fileType.value === 'image' || fileType.value === 'video') {
      reader.readAsDataURL(uploadedFile.value);
    } else {
      // Для других типов файлов не нужно создавать превью
      filePreview.value = null;
      emit('uploadFile', uploadedFile.value, '');
    }
  }

  isUploadLoading.value = false;
};

const removeFile = () => {
  uploadedFile.value = null;
  filePreview.value = null;
  emit('uploadFile', null, null);
};

const sendMessage = () => {
  if (textMessage.value.trim() || uploadedFile.value) {
    emit('sendMessage', textMessage.value);
    textMessage.value = '';
    removeFile();
  }
};
</script>
  
<style scoped>
.message-input {
  position: relative;
  display: flex;
  align-items: center;
  padding: 15px;
  border-top: 1px solid #e0e0e0;
  background: #f4f7f9;
}

.message-input input {
  flex: 1;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: border 0.3s ease;

  &:focus {
    border-color: #1a73e8;
    outline: none;
  }
}

.send-btn {
  padding: 15px 20px;
  margin-left: 10px;
  background-color: #f17a01;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #de7000;
  }
}

.custom-file-upload {
  position: relative;
  display: inline-block;
  padding: 10px 13px;
  margin-right: 10px;
  background: none;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  transition: 0.2s ease-out;
  width: 40px;
  height: 40px;
}

.custom-file-upload .file-input {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  cursor: pointer;
}

.custom-file-upload .paperclipIcon {
  color: #68696e;
  cursor: pointer;
}

.custom-file-upload .paperclipIcon:hover {
  color: #212121;
}

.uploaded-file-preview {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;

}

.preview-image,
.preview-video {
  max-width: 80px;
  max-height: 80px;
  border-radius: 5px;
  object-fit: cover;
}

.preview-video {
  filter: none;
}

.preview-file {
  display: flex;
  align-items: center;
  background-color: #f0f0f0;
  padding: 5px 10px;
  border-radius: 5px;
}

.file-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.preview-file span {
  font-size: 0.9em;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.remove-file-btn {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  padding: 4px;
  background-color: #333;
  border: none;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.complaint-btn {
  padding: 10px 15px;
  background-color: #0e0e0e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-right: 10px;
}

.complaint-btn:hover {
  background-color: #d13f3f;
}

.text-archived{
  margin: 0;
  padding: 7px;
  font-size: 16px;
  color: #888; /* Серый текст для неактивного состояния */
  background-color: #f9f9f9; /* Легкий фон для отделения от чата */
  text-align: center; /* Центрирование текста */
  line-height: 1.5;
}
</style>