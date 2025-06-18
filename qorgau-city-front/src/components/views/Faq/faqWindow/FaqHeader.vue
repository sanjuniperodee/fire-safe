<template>
    <div v-if="selectedChat" class="chat-header">
        <div class="chat-main">
          <div class="chat-avatar">
          <img src="/user.png" alt="">
        </div>
        <h2>{{ selectedComplaint?.inspector.phone === userStore.user?.phone  ?  selectedComplaint?.author.first_name : selectedComplaint?.inspector.first_name }} {{ selectedComplaint?.inspector.phone === userStore.user?.phone  ?  '': selectedComplaint?.inspector.last_name }}</h2>
      </div>
    
      <span @click="openDeleteModal" v-html="deleteBasket"></span>
    </div>
  
    <ComplaintRoomDelete
      :chatId="selectedComplaint?.id ?? -1"
      :show-modal="showModal"
      @close="toggleModal"
    />
  </template>
  
  <script setup lang="ts">
  import type { ChatRoomType } from '@/types/Chat'
  import { deleteBasket } from '@/assets/svg'
  import ComplaintRoomDelete from '@components/modal/confirm/ComplaintRoomDelete.vue'
  import { ref } from 'vue'
  import { useUserStore } from '@/stores/UserStore'
import type { ComplaintRoomType } from '@/types/Complaint';


  
  const props = defineProps<{
    selectedChat: ChatRoomType | null;
    selectedComplaint : ComplaintRoomType | null 
  }>();
  
  const userStore = useUserStore()

  const showModal = ref(false)
  
  const toggleModal = () => {
    showModal.value = !showModal.value
  }
  
  const openDeleteModal = () => {
    if (props.selectedChat) {
      showModal.value = true
    }
  }
  </script>
  
  <style scoped>
  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 50px;
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
    background: #ef7901;
    color: white;
    font-size: 1.2em;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
    & span{
      cursor: pointer;
    }
  }

  .chat-main{
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  h2 {
    padding-left: 10px;
  }
  
  .chat-avatar{
    width: 30px;
    height: 30px;
    border-radius: 50%;
  }
  .chat-avatar img{ 
    width: 100%;
    border-radius: 50%;
  }
  </style>
  