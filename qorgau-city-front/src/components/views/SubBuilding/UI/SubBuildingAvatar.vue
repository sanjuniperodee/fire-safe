<template>
  <div class="avatar">
    <v-menu
      location="end"
      style="padding: 0"
      transition="scale-transition"
    >
      <template v-slot:activator="{ props }">
        <label
          v-bind="props"
          for="thumbnail"
        >
          <img
            v-if="image"
            :src="image"
            class="avatar-img"
            alt="Аватар профиля"
          />

          <span v-else>
            <v-icon size="200" class="no-image">mdi-home-city</v-icon>
            <!--            <MediaUpload :title="'Загрузите фото обьекта'" :handle-file-change="uploadAvatar"/>-->
          </span>
        </label>
      </template>
      <v-list style="padding: 0">
        <v-list-item
          @click="uploadAvatar"
          style="color: #5b9271"
          value="upload-avatar"
        >
          <v-list-item-title class="list-item">
            <v-icon> mdi-upload </v-icon>
            <div style="padding-top: 3px">Загрузить фото</div>
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="deleteAvatar"
          style="color: #d20f0d"
          value="delete-avatar"
        >
          <v-list-item-title class="list-item">
            <v-icon> mdi-delete </v-icon>
            <div style="padding-top: 3px">Удалить фото</div>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script setup lang="ts">
import { useSnackbarStore } from '@stores/SnackbarStore'
import { useObjectStore } from '@stores/ObjectStore'
import { useRoute } from 'vue-router'

const snackbarStore = useSnackbarStore()
const objectStore = useObjectStore()

const route = useRoute()
const routeId = Number(route.params.id) as number

const props = defineProps<{
  image: string | null
}>()

console.log(props.image)

const uploadAvatar = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e: any) => {
    try {
      const formData = new FormData()
      formData.append('avatar_url', e.target.files[0])

      console.log("avatar",e.target.files[0])

      await objectStore.createObjectAvatar(routeId, formData)
      snackbarStore.pullSnackbar('Ваше фото успешно загружено.', 2000, '#5b9271')
    } catch (error) {
      snackbarStore.pullSnackbar('Не удалось загрузить ваше фото.', 2000, '#d20f0d')
    }
  }
  input.click()
}

const deleteAvatar = async () => {
  try {
    if (props.image) {
      // Предполагаем, что image содержит URL с imageId
      const imageId = extractImageIdFromUrl(props.image); // Вам нужно реализовать функцию
      await objectStore.deleteObjectAvatar(routeId, imageId);
      snackbarStore.pullSnackbar('Фото успешно удалено.', 2000, '#5b9271');
    } else {
      throw new Error('Изображение не задано');
    }
  } catch (error) {
    snackbarStore.pullSnackbar('Не удалось удалить ваше фото.', 2000, '#d20f0d');
  }
}

// Пример функции извлечения imageId из URL
function extractImageIdFromUrl(imageUrl: string): string {
  // Реализуйте логику для извлечения imageId из URL
  const parts = imageUrl.split('/');
  return parts[parts.length - 1].split('.')[0]; // Например, /images/123.jpg -> 123
}
</script>

<style lang="scss" scoped>
.avatar {
  width: 200px;
  height: 200px;
  position: relative;
  border-radius: 10px;
}

.avatar-img {
  width: 200px;
  height: 200px;
  border-radius: 10px;
  object-fit: cover;
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
</style>
