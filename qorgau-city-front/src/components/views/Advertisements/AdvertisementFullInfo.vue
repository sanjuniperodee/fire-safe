<template>
  <v-container>
    <v-card
      class="full-card"
      variant="outlined"
      v-for="advertisement in advertisements"
      :key="advertisement.id"
    >
      <v-card-title class="full-card__title">{{ advertisement.title }}</v-card-title>
      <v-card-subtitle class="full-card__subtitle">{{ advertisement.category }}</v-card-subtitle>
      <v-card-text class="full-card__text">
        <div><strong>Автор:</strong> {{ advertisement.author }}</div>
        <div><strong>Описание:</strong> {{ advertisement.text }}</div>
        <div><strong>Мин. цена:</strong> {{ advertisement.min_price }}</div>
        <div><strong>Макс. цена:</strong> {{ advertisement.max_price }}</div>
        <div><strong>Контактное лицо:</strong> {{ advertisement.contract_name }}</div>
        <div><strong>Телефон:</strong> {{ advertisement.phone }}</div>
        <div><strong>Адрес:</strong> {{ advertisement.address }}</div>
        <div><strong>Спецификация:</strong> {{ advertisement.specification }}</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { type Advertisement } from '@/types/Advertisements'
import { onMounted, ref } from 'vue'
import { advertisementService } from '@/services/advertisements.service'
import { useRoute } from 'vue-router'
const route = useRoute()

const advertisements = ref<Advertisement[]>([{
  title: '',
  category: '',
  author: 0,
  text: '',
  min_price: 0,
  max_price: 0,
  contract_name: '',
  phone: '',
  address: '',
  specification: ''
}])

const fetchAdvertisements = async () => {
  try {
    advertisements.value = await advertisementService.getAdvertisementById(Number(route.params.id))
  } catch (error) {
    console.error('Ошибка загрузки объявлений:', error)
  }
}

onMounted(() => {
  fetchAdvertisements()
})
</script>

<style lang="scss" scoped>
.full-card {
  margin: 20px;
  padding: 20px;
  max-width: 800px;
  width: 100%;
  background-color: #fff;

  &__title {
    font-size: 24px;
    margin-bottom: 10px;
  }

  &__subtitle {
    font-size: 18px;
    margin-bottom: 20px;
  }

  &__text {
    font-size: 16px;
    line-height: 1.5;

    & > div {
      margin-bottom: 10px;
    }
  }
}
</style>
