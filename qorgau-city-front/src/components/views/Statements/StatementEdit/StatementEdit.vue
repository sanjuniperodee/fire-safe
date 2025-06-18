<script setup lang="ts">
import CabinetProviderLayout from '@/layouts/CabinetProviderLayout.vue'
import { UserRoleOptions } from '@/types/User'
import { useUserStore } from '@/stores/UserStore'
import EditForm from '@views/Statements/StatementEdit/EditForm.vue'

const userStore = useUserStore()
</script>

<template>
  <CabinetProviderLayout v-if="userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER)">
    <EditForm />
  </CabinetProviderLayout>

  <div
    v-else
    class="wrapper"
  >
    <EditForm />
  </div>
</template>

<style scoped lang="scss">
.wrapper {
  height: calc(100vh - 56px);
  overflow-y: scroll;
}
</style>
