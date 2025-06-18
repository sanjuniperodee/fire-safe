<template>
  <div class="inspect-parent">
    <ObjectOwnerEditButton v-if="!userStore.isInspector" />
    <ObjectOwnerToolbar />
    <div class="inspect">
      <LoaderSpinner v-if="objectInfoStore.isObjectInfoLoading" />
      <ObjectOwnerTimeline v-if="!objectInfoStore.isObjectInfoLoading" />
      <ObjectOwnerInspectForms v-if="!objectInfoStore.isObjectInfoLoading" />
    </div>
  </div>
</template>

<script setup lang="ts">
import ObjectOwnerToolbar from '../UI/object-owner-toolbar/ObjectOwnerToolbar.vue'
import ObjectOwnerTimeline from '../UI/object-owner-timeline/ObjectOwnerTimeline.vue'
import ObjectOwnerInspectForms from './forms/ObjectOwnerInspectForms.vue'
import ObjectOwnerEditButton from './UI/ObjectOwnerEditButton.vue'
import { useUserStore } from '@/stores/UserStore'
import { onMounted } from 'vue'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'
import { useRoute } from 'vue-router'
import { UserRoleOptions } from '@/types/User'
import router from '@/router'

const userStore = useUserStore()
const route = useRoute()

const objectInfoStore = useObjectInfoStore()

onMounted(async () => {
  await userStore.getUser()
  if (
    !userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER) &&
    !userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)
  ) {
    await router.push('/map')
    return
  }
  await objectInfoStore.getObjectInfo(route.params.id as string)
})
</script>

<style lang="scss" scoped>
.inspect {
  padding: 2em 0;
  font-family: 'Overpass', sans-serif;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: scroll;
  overflow-x: hidden;
  align-items: center;
}

.inspect-parent {
  height: calc(100vh - 120px);
}
</style>
