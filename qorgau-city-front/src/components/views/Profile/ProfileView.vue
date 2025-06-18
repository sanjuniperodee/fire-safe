<template>
  <div class="profile-parent">
    <ProfileBanner />
    <div class="profile">
      <ProfileInfo />
    </div>
  </div>
</template>

<script setup lang="ts">
import ProfileBanner from './profile-banner/ProfileBanner.vue'
import ProfileInfo from './profile-info/ProfileInfo.vue'
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { useProfileStore } from '@/stores/ProfileStore'
import { useObjectStore } from '@/stores/ObjectStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'

const userStore = useUserStore()
const snackbarStore = useSnackbarStore()
const objectStore = useObjectStore()
const profileStore = useProfileStore()

onMounted(async () => {
  await userStore.getUser()
  try {
    await objectStore.getObjects()
    profileStore.fillItemsValues(userStore.user!)
  } catch (error) {
    snackbarStore.pullSnackbar(
      'Не удалось получить ваши паспорты ПБО. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
  }
})
</script>

<style lang="scss" scoped>
.profile-parent {
  height: calc(100vh - 56px);
  overflow-y: scroll;
  background-color: #f5f5f5;
}

.profile {
  height: 100vh;
  font-family: 'Overpass', sans-serif;
  display: flex;
  flex-direction: column;
}
</style>
