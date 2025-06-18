<template>
  <div>
    <!-- <LoaderSpinner v-if="isLoading" /> -->
    <div 
    class="chat-container"
>
    <RoomsNavbar
      :selectedComplaint="complaintStore.complaintRoom"
      :chat-rooms="complaintStore.complaints"
      @select-chat="selectComplate"
      @update-status="updateStatus"
    />

    <FaqWindow
      :selectedComplaint="complaintStore.complaintRoom"
      :selectedChat="complaintStore.chatRoom"
      @updateStatus="updateStatus"
    />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, toRaw, nextTick } from 'vue'
import RoomsNavbar from './RoomsNavbar.vue';
import FaqWindow from './faqWindow/FaqWindow.vue';
import type { Message, Complaint, ComplaintRoomType } from '@/types/Complaint'
import { useComplaintStore } from '@stores/ComplaintStore'
import { useChatStore } from '@/stores/ChatStore'
import { chatWebSocketService } from '@/services/chat.service'
import type { ChatRoomType} from '@/types/Chat'
import { useRoute } from 'vue-router';
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'


const route = useRoute();
const complaintStore = useComplaintStore()
const chatStore = useChatStore()
const complaints = ref<Complaint | null>(null)
const selectedComplaint = ref<ComplaintRoomType | null>(null);
const selectedChat = ref<ChatRoomType | null>(null);
const isLoading = ref(false)
const messageChat = ref<Message | null>(null)
  const status = ref('PENDING')

const updateStatus = (newStatus: string) => {
  // Обновите статус в родительском компоненте
  status.value = newStatus;
};

const selectComplate = async (id: number) => {
  // Disconnect from the current WebSocket connection if it's active
  if (selectedChat.value) {
    chatWebSocketService.disconnect();
  }

  try {
    isLoading.value = true
    // Fetch the selected complaint room and set it
    await complaintStore.getComplaintById(id);
    selectedComplaint.value = toRaw(complaintStore.complaintRoom);
    await complaintStore.getComplaint(selectedComplaint.value?.id || 1);
    selectedChat.value = complaintStore.chatRoom;
    isLoading.value = false
    // Check if selectedChat exists before connecting WebSocket
    if (selectedComplaint.value && selectedComplaint.value?.chat_room_id) {
      await chatWebSocketService.connect(selectedComplaint.value.chat_room_id);
      console.log('Connected to WebSocket for complaint room:', selectedComplaint.value);
    } else {
      console.error('Complaint room not found or invalid chat room ID');
    }
  } catch (error) {
    console.error('Error while selecting complaint:', error);
    isLoading.value = false
  }
};



onMounted(async () => {
  await complaintStore.getComplaints(status.value)
  if (complaintStore.lastComplaintRoom) {
    isLoading.value = true
    await selectComplate(complaintStore.lastComplaintRoom.id)
    isLoading.value = false
  }
})

watch(status, async (newStatus) => {
  await complaintStore.getComplaints(newStatus)
}, { immediate: true })


// watch(() => complaintStore.complaints, (newComplaintsRooms) => {
//   if (!selectedComplaint.value && newComplaintsRooms.length > 0) {
//     selectComplate(complaintStore.lastComplaintRoom!.id)
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