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
            v-if="userStore.user?.avatar_url"
            :src="userStore.user?.avatar_url"
            alt="Аватар профиля"
          />
          <img
            v-else
            src="/user.png"
            alt="Аватар профиля"
          />
        </label>
      </template>
      <v-list style="padding: 0">
        <v-list-item
          @click="() => uploadAvatar()"
          style="color: #5b9271"
          value="upload-avatar"
        >
          <v-list-item-title class="list-item">
            <v-icon> mdi-upload </v-icon>
            <div style="padding-top: 3px">Загрузить фото</div>
          </v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="() => deleteAvatar()"
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
import { userService } from '@/services/user.service'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { useUserStore } from '@/stores/UserStore'

const userStore = useUserStore()
const snackbarStore = useSnackbarStore()

const uploadAvatar = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e: any) => {
    try {
      const formData = new FormData()
      formData.append('avatar_url', e.target.files[0])
      userStore.user!.avatar_url = await userService.uploadAvatar(userStore.user!.id, formData)
      snackbarStore.pullSnackbar('Ваше фото успешно загружено.', 2000, '#5b9271')
    } catch (error) {
      snackbarStore.pullSnackbar('Не удалось загрузить ваше фото.', 2000, '#d20f0d')
    }
  }
  input.click()
}

const deleteAvatar = async () => {
  try {
    const message = await userService.deleteAvatar(userStore.user!.id)
    userStore.user!.avatar_url = ''
    snackbarStore.pullSnackbar(message, 2000, '#5b9271')
  } catch (error) {
    snackbarStore.pullSnackbar('Не удалось удалить ваше фото.', 2000, '#d20f0d')
  }
}
</script>

<style lang="scss" scoped>
.avatar {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  position: relative;

  & img {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    object-fit: cover;
  }

  background-color: #ccc;
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
