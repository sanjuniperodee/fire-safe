<script setup lang="ts">
import type { Complaint, ComplaintRoomType } from '@/types/Complaint';
import type { ChatRoomType } from '@/types/Chat'
import { imageIcon } from '@/assets/svg'
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { fi } from 'date-fns/locale';

const userStore = useUserStore()

const searchQuery = ref('')
const tabs = ref(['Ожидает ответа', 'Отвечено', 'Истек срок', 'Не отвечено'])
const activeTab = ref('Ожидает ответа')

const props = defineProps<{
  chatRooms: Complaint[]
  selectedComplaint: ComplaintRoomType | null
}>();

const emit = defineEmits<{
  (e: 'select-chat', id: number): void;
  (e: 'update-status', status: string): void;
}>();

const selectChat = (id: number) => {
  emit('select-chat', id);
};

const tabTranslations: Record<string, string> = {
  'Ожидает ответа': 'PENDING',
  'Отвечено': 'ANSWERED',
  'Истек срок': 'EXPIRED',
  'Не отвечено': 'NOT_ANSWERED'
};

const selectTab = (tab: string) => {
  activeTab.value = tab;
  const translatedTab = tabTranslations[tab] || tab;
  emit('update-status', translatedTab);
}

const search = ref('')

const filteredComplaints = computed(() => {
  if (!props.chatRooms) location.reload();
  
  return props.chatRooms.filter(chat =>
    (chat.author?.first_name?.toLowerCase().includes(search.value.toLowerCase()) ||
     chat.inspector?.first_name?.toLowerCase().includes(search.value.toLowerCase())) ||
    (chat.author?.phone.toString().includes(search.value) || 
     chat.inspector?.phone.toString().includes(search.value))
  );
});

</script>

<template>
  <div class="chat-list">
    <h2>Жалобы</h2>

    <div class="group">
      <svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><g><path d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"></path></g></svg><svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><g><path d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"></path></g></svg>
      <input placeholder="Поиск чата" type="search" v-model="search" class="input">
    </div>

    <div class="status">
      <div class="tabs">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        @click="selectTab(tab)"
        :class="{'active': activeTab === tab}"
        class="tab"
      >
        {{ tab }}
      </button>
    </div>
    </div>

    <div  class="chat-item-non" v-if="filteredComplaints.length === 0">
        <p>Жалоб пока нет</p>
    </div>
    <div
      v-else
      v-for="complaint in filteredComplaints"
      :key="complaint.id"
      class="chat-item"
      :class="{ active: selectedComplaint?.id === complaint.id }"
      @click="selectChat(complaint.id)"
    >
      <div>
        <p :class="complaint?.inspector.phone !== userStore.user?.phone ?'chat-owner owner'  : 'chat-owner provider'">{{ complaint?.inspector.phone !== userStore.user?.phone ? 'Инспектор' : 'Гражданин' }}</p>
        <div class="chat-info">
        <div class="chat-avatar">
          <img src="/user.png" alt="">
        </div>
        <div class="chat-text">
          <h3>{{ complaint.unique_id }}</h3>
          <p>{{ complaint?.inspector.phone === userStore.user?.phone  ?  complaint?.author.first_name  : complaint?.inspector.first_name  }} {{ complaint?.inspector.phone === userStore.user?.phone  ? '' : complaint?.inspector.last_name  }}</p>
        </div>
      </div>
      <div class="chat-date">
        <p>Дата и время архива: {{ selectedComplaint?.archive_date?.slice(0, 10) }} {{ selectedComplaint?.archive_date?.slice(11, 16) }}</p>
        <p>Дата и время окончания срока: {{ selectedComplaint?.expiration_date?.slice(0, 10) }} {{ selectedComplaint?.expiration_date?.slice(11, 16) }}</p>
      </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-list {
  width: 315px;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
  background: #fffefb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

  h2{
    display: flex;
    align-items: center;
    justify-content: start;
    font-size: 22px;
    margin-left: 15px;
    font-weight: 400;
    color: #212121;
    height: 50px;
  }
}

.chat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.chat-item:hover {
  background-color: #eef5ff;
}

.chat-item.active {
  background-color: #e6f2ff;
  border-left: 5px solid #025aaf;
  padding-left: 10px;
}

.chat-info h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  color: #666;
  font-size: 0.8em;
}

.chat-info p {
  margin: 0 0 5px 0;
  font-size: 1.1em;
  font-weight: 500;
  color: #333;
  padding-top: 5px;
}

.chat-owner {
    margin: 5px 0 10px 0;
    font-size: 1.1em;
    font-weight: 500;
    color: #333;
    padding-left: 10px;
    padding-bottom: 5px;
  }

  .provider {
    color: #50AF50;
  }

  .owner {
    color: #FAAB51;
  }

.chat-item-non{
  width: 100%;
  margin: 300px auto;
}
.chat-item-non p{
  margin: 0 0 5px 0;
  font-size: 1.2em;
  font-weight: 500;
  color: #333;
  text-align: center;
}

.group {
  display: flex;
  line-height: 28px;
  align-items: center;
  position: relative;
  width: 100%;
  padding: 0 12px;
  margin-bottom: 10px;
}

.input {
  width: 100%;
  height: 40px;
  line-height: 28px;
  padding: 0 1rem 0 2.5rem;
  border: 2px solid transparent;
  border-radius: 8px;
  outline: none;
  background-color: white;
  color: #0d0c22;
  transition: .3s ease;
}

.input::placeholder {
  color: #9e9ea7;
}

.input:focus, input:hover {
  outline: none;
  border-color: rgb(224, 224, 224);
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(147, 147, 147, 0.1);
}

.icon {
  position: absolute;
  left: 1rem;
  fill: #9e9ea7;
  width: 1rem;
  height: 1rem;
}

/*  */

.status {
  width: 299px;
  overflow-y: auto;
}
.tabs {
  /* width: 300px; */
  display: flex;
  /* overflow-y: auto; */
  border-bottom: 1px solid #e0e0e0;
}

.tab {
  padding: 12px 9px;
  border: none;
  background-color: transparent;
  font-size: 14px;
  cursor: pointer;
  color: #666;
  transition: color 0.3s, border-bottom 0.3s;
}

.tab.active {
  color: black;
  border-bottom: 2px solid black;
}

.tab:hover {
  color: black;
}

.chat-text{
  padding-left: 7px;
}
.chat-info{
  display: flex;
    align-items: center;
    margin-top: 10px;
    border-bottom: 0.5px solid #e0e0e0;
    padding-bottom: 10px;
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
  
  .chat-date p{
    padding: 0 10px;
    gap: 12px;
    margin: 0;
    color: #666;
    font-size: 0.8em;
    margin-top: 10px;
  } 
</style>
