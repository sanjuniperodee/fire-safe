<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { useProfileStore } from '@/stores/ProfileStore'
import { useObjectStore } from '@/stores/ObjectStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import ObjectsInspector from '@views/Objects/objects-inspector/ObjectsInspector.vue'
import CabinetInspectorLayout from '@/layouts/CabinetInspectorLayout.vue'
import { UserRoleOptions } from '@/types/User'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const snackbarStore = useSnackbarStore()
const objectStore = useObjectStore()
const profileStore = useProfileStore()

const router = useRouter()

onMounted(async () => {
  await userStore.getUser()
  if (!userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)) {
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
  <CabinetInspectorLayout>
    <div class="main">
      <ObjectsInspector />
    </div>
  </CabinetInspectorLayout>
</template>

<style scoped lang="scss">
.main {
  height: calc(100vh - 56px);
  padding: 20px 0;
}

@media only screen and (max-width: 789px) {
  .main {
    left: 0;
    padding: 0 10px;
  }
}
</style>
