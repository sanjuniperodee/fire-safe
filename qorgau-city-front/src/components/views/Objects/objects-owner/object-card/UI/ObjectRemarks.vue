<template>
     <h1>
      Примечание от Инспектора
      <Empty
        v-if="remarks.length > 0"
        message="Отсутствуют примечание"
      />
    </h1>
    <div class="block" v-if="remarks.length > 0">  <!-- Рендерим блок только если есть замечания -->
      <div 
        class="remark" 
        v-for="remark in remarks" 
        :key="remark.id"
      >
        <p class="remark-content">{{ remark.content }}</p>
        <p class="remark-date">{{ formatDate(remark.created_at) }}</p>
      </div>
    </div>
    <p v-else class="no-remarks">Нет замечаний</p> <!-- Сообщение если нет замечаний -->
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useObjectStore } from '@/stores/ObjectStore';
  import { useRoute } from 'vue-router';
  
  type Remark = {
    id: number;
    building: number;
    inspector: number;
    content: string;
    created_at: Date;
  };
  
  const route = useRoute();
  const buildingId = route.params.id as string;
  
  const objectStore = useObjectStore();
  const remarks = ref<Remark[]>([]);
  
  // Загрузка замечаний при загрузке компонента
  onMounted(async () => {
    try {
      remarks.value = await objectStore.getRemarks(buildingId);
    } catch (error) {
      console.error('Ошибка загрузки замечаний:', error);
    }
  });
  
  // Функция для форматирования даты
  const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }) + ' ' + new Date(date).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};
  </script>
  
  <style lang="css" scoped>
  .block {
    padding: 1rem;
    /* background-color: #f9f9f9;
    border: 1px solid #ddd; */
    border-radius: 8px;
    margin: 0 0.4rem;
  }
  
  h1 {
  padding-left: 25px;
  font-weight: 600;
  font-size: 20px;
  margin-top: 50px;
  margin-bottom: 20px;
}
  .remark {
    margin-bottom: 1rem;
    padding: 0.5rem;
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .remark-content {
    margin: 0;
    font-size: 0.9rem;
    color: #333;
    line-height: 1.4;
  }
  
  .remark-date {
    font-size: 0.8rem;
    color: #888;
    margin-top: 0.5rem;
  }

  .no-remarks {
     margin: 20px 0;
  text-align: center;
  font-size: 1.2rem;
  color: #555;
  font-weight: bold;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 8px;
  margin-top: 20px;
  border: 1px dashed #ccc;
}

  </style>