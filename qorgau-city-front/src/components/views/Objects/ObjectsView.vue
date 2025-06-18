<script lang="ts" setup>
import { onMounted } from 'vue'
import { useUserStore } from '@stores/UserStore'
import ObjectsOwner from './objects-owner/ObjectsOwner.vue'
import ObjectsInspector from './objects-inspector/ObjectsInspector.vue'
import { useRouter } from 'vue-router'
import { UserRoleOptions } from '@/types/User'

const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  await userStore.getUser()
  if (!userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER)) {
    await router.push('/map')
    return
  }
})
</script>

<template>
  <div class="object-parent">
    <div
      v-if="userStore.isInspector"
      class="h-100"
    >
      <ObjectsInspector />
    </div>
    <div
      class="h-100"
      v-if="!userStore.isInspector"
    >
      <ObjectsOwner />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.object-parent {
  height: calc(100vh - 56px);
}
</style>
