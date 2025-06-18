<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { useProfileStore } from '@/stores/ProfileStore'
import { useObjectStore } from '@/stores/ObjectStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { UserRoleOptions } from '@/types/User'
import { useRouter } from 'vue-router'
import StatementsView from '@views/Statements/StatementsView.vue'
import CabinetProviderLayout from '@/layouts/CabinetProviderLayout.vue'

const userStore = useUserStore()
const snackbarStore = useSnackbarStore()
const objectStore = useObjectStore()
const profileStore = useProfileStore()

const router = useRouter()

onMounted(async () => {
  await userStore.getUser()

  if (!userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER)) {
    await router.push('/profile')
    return
  }
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

<template>
  <div class="main">
    <CabinetProviderLayout>

    </CabinetProviderLayout>
  </div>
</template>

<style scoped lang="scss">
.main {
  height: calc(100vh - 56px);
  padding: 20px 0;
  flex-grow: 1;
}

@media only screen and (max-width: 789px) {
  .main {
    left: 0;
    padding: 0 10px;
  }
}
</style>
