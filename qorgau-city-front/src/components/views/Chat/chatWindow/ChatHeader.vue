<template>
  <div v-if="selectedChat" class="chat-header">
    <div class="chat-main">
        <div class="chat-avatar">
          <img src="/user.png" alt="">
        </div>
        <div>
          <h2>{{ selectedChat.initiator.phone === userStore.user?.phone  ?  selectedChat.author_name : selectedChat.provider_name }}</h2>
          <p :class="selectedChat?.initiator.phone === userStore.user?.phone || !selectedChat.is_statement_owner ? 'chat-owner owner'  : 'chat-owner provider' ">{{  selectedChat?.initiator.phone === userStore.user?.phone || !selectedChat.is_statement_owner ? 'Собственник'   : 'Поставщик' }}</p>
        </div>
    </div>
    <!-- <span @click="openDeleteModal" v-html="deleteBasket"></span> -->
  </div>

  <!-- <ChatRoomDelete
    :chatId="selectedChat?.id ?? -1"
    :show-modal="showModal"
    @close="toggleModal"
  /> -->
</template>

<script setup lang="ts">
import type { ChatRoomType} from '@/types/Chat'
import { deleteBasket } from '@/assets/svg'
import ChatRoomDelete from '@components/modal/confirm/ChatRoomDelete.vue'
import { ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'

const props = defineProps<{
  selectedChat: ChatRoomType | null;
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
  
  .chat-avatar{
    width: 30px;
    height: 30px;
    border-radius: 50%;
  }
  .chat-avatar img{ 
    width: 100%;
    border-radius: 50%;
  }
  h2 {
    margin-left: 10px;
    padding-top: 5px;
  }

  .chat-owner {
    margin: 5px 0 0 0;
    font-size: 0.7em;
    font-weight: 500;
    color: #333;
    padding-left: 10px;
  }

  .provider {
    color: #7dcea0;
  }

  .owner {
    color: #f7dc6f;
  }
</style>
