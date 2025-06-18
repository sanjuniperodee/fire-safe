<script setup lang="ts">
import type { ChatRoomType, ChatRooms,  } from '@/types/Chat';
import { imageIcon } from '@/assets/svg'
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { fi } from 'date-fns/locale';
import { categories, categories as categoryList } from '@/utils/categoryList'

const userStore = useUserStore()

const searchQuery = ref('')
const tabs = ref(['Открыто', 'В работе', 'Выполнено', 'В архиве'])
const activeTab = ref('Открыто')

const props = defineProps<{
  chatRooms: ChatRooms
  selectedChat: ChatRoomType | null
}>();

const emit = defineEmits<{
  (e: 'select-chat', id: number): void;
  (e: 'update-status', status: string): void;
}>();


const selectChat = (id: number) => {
  emit('select-chat', id);
};

const tabTranslations: Record<string, string> = {
  'Открыто': 'OPENED',
  'В работе': 'IN_WORK',
  'Выполнено': 'COMPLETED',
  'В архиве': 'ARCHIVED'
};

const selectTab = (tab: string) => {
  activeTab.value = tab;
  const translatedTab = tabTranslations[tab] || tab;
  emit('update-status', translatedTab);
}

const search = ref('')


const filteredChats = computed(() => {
  if (!props.chatRooms) location.reload()
  return props.chatRooms.filter(chat =>
    chat.receiver.username.toLowerCase().includes(search.value.toLowerCase()) ||
    chat.receiver.phone.toString().includes(search.value)
  )
})

</script>

<template>
  <div class="chat-list">
    <h2>Чаты</h2>

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

    <div  class="chat-item-non" v-if="filteredChats.length === 0">
        <p>Заказов пока нет</p>
    </div>
    <div
      v-else
      v-for="chat in filteredChats"
      :key="chat.id"
      class="chat-item"
      :class="{ active: selectedChat?.id === chat.id }"
      @click="selectChat(chat.id)"
    >
    <div>
      <p :class="chat?.initiator.phone === userStore.user?.phone || !chat.is_statement_owner ? 'chat-owner owner'  : 'chat-owner provider' ">{{  chat?.initiator.phone === userStore.user?.phone || !chat.is_statement_owner ? 'Собственник'   : 'Поставщик' }}</p>
      <p class="chat-categories">{{ chat?.categories.map(categoryId => {
        const categoria = categoryList.find(c => c.id === categoryId);
        return categoria?.name;}).filter(Boolean).join(', ') }}</p>
      <p class="chat-city"><v-icon>mdi-home</v-icon>Город: {{ chat?.location }}</p>
        <div class="chat-info">
          <div class="chat-avatar">
          <img src="/user.png" alt="">
          </div>
          <div class="chat-text">
            <h3>{{ chat?.initiator.phone === userStore.user?.phone  ?  chat?.author_name : chat?.provider_name }}</h3>
            <p v-if="!chat.last_message?.text">
          <span v-html="imageIcon"></span>
          Нет сообщения
        </p>

        <p v-else-if="chat.last_message.text && chat.last_message.attachments">
          <span v-html="imageIcon"></span>
          {{ chat.last_message.text }}
        </p>

        <p v-else>
          {{ chat.last_message.text }}
        </p>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-list {
  width: 300px;
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
  margin: 0 0 5px 0;
  font-size: 1.1em;
  font-weight: 500;
  color: #333;
}

.chat-info p {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  color: #666;
  font-size: 0.9em;
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
  font-size: 12px;
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

.chat-city{
  padding-left: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  color: #666;
  font-size: 0.9em;
}

.chat-text {
  padding-left: 15px;
}
.chat-info{
    display: flex;
    align-items: center;
    margin-top: 10px;
    border-top: 0.5px solid #e0e0e0;
    padding-top: 10px;
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

  .chat-categories {
  display: -webkit-box; /* Используем для многоточия */
  -webkit-line-clamp: 2; /* Ограничиваем количество строк */
  -webkit-box-orient: vertical; /* Вертикальная ориентация */
  overflow: hidden; /* Скрываем текст, выходящий за пределы */
  text-overflow: ellipsis; /* Добавляем многоточие */
  max-height: 3em; /* Высота, соответствующая двум строкам текста */
  line-height: 1.5em; /* Высота строки */
  white-space: normal; /* Убеждаемся, что текст переносится */
}

  .chat-owner {
    margin: 5px 0 10px 0;
    font-size: 0.9em;
    font-weight: 500;
    color: #333;
    padding-left: 10px;
  }

  .provider {
    color: #50AF50;
  }

  .owner {
    color: #FAAB51;
  }
</style>
