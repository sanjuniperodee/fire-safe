<template>
  <div v-if="computedImages?.length! > 0" class="block">
    <div v-for="image in computedImages" :key="image.id" class="avatar-img-wrapper">
      <img
        :src="image.image"
        :alt="image.image"
        class="avatar-img"
      />
      <button @click="deleteAvatar(image.id!)" class="remove-file-btn" v-html="close"></button>
    </div>
  </div>
  <span v-else>
    <v-icon size="300" class="no-image">mdi-home-city</v-icon>
  </span>
</template>

<script setup lang="ts">
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { useObjectStore } from '@stores/ObjectStore'
import { useRoute } from 'vue-router'
import type { Avatar } from '@/types/ObjectBuilding'
import { close } from '@/assets/svg'
import { computed } from 'vue'

const snackbarStore = useSnackbarStore()
const objectStore = useObjectStore()

const route = useRoute()
const routeId = Number(route.params.id) as number

const props = defineProps<{
  images: Avatar[] | null
}>()

const computedImages = computed(() => props.images)

const deleteAvatar = async (id: number) => {
  try {
    await objectStore.deleteObjectAvatar(routeId, id.toString()) // Передаем ID для удаления
    snackbarStore.pullSnackbar('Фото успешно удалено.', 2000, '#5b9271')
  } catch (error) {
    snackbarStore.pullSnackbar('Не удалось удалить ваше фото.', 2000, '#d20f0d')
  }
}
</script>

<style lang="scss" scoped>
.block{
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 30px;

  & .avatar-img-wrapper{
    position: relative;

    & .avatar-img {
      max-width: 500px;
      width: 1/3;
      max-height: 300px;
      border-radius: 10px;
      object-fit: cover;
    }
  }
}

.no-image{
  color: #68696EFF;
  cursor: pointer;
}

.icon {
  transform: translateY(150px);
  opacity: 0;
  transition: 0.2s;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 4px;
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
</style>
