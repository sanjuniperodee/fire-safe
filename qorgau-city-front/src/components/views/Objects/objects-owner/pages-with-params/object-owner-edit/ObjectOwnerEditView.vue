<template>
  <div class="edit-parent">
    <div v-if="!(objectStore.currentStep === 2)">
      <ObjectDownloadZip :organizationName="organizationName" />
      <ObjectOwnerSaveButton />
    </div>
    <ObjectOwnerToolbar />
    <div class="edit">
      <LoaderSpinner v-if="objectInfoStore.isObjectInfoLoading" />
      <ObjectOwnerTimeline v-if="!objectInfoStore.isObjectInfoLoading" />
      <ObjectPassport  v-if="!objectInfoStore.isObjectInfoLoading"/>
      <ObjectOwnerEditForms v-if="!objectInfoStore.isObjectInfoLoading" />
    </div>
  </div>
</template>

<script setup lang="ts">
import ObjectOwnerToolbar from '../UI/object-owner-toolbar/ObjectOwnerToolbar.vue'
import ObjectOwnerTimeline from '../UI/object-owner-timeline/ObjectOwnerTimeline.vue'
import ObjectOwnerEditForms from './forms/ObjectOwnerEditForms.vue'
import ObjectOwnerSaveButton from './UI/ObjectOwnerSaveButton.vue'
import ObjectDownloadZip from './UI/ObjectDownloadZip.vue'
import ObjectPassport from './UI/ObjectPassport.vue'
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { useRoute, useRouter } from 'vue-router'
import { useObjectStore } from '@/stores/ObjectStore'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'
import { UserRoleOptions } from '@/types/User'

const router = useRouter()
const route = useRoute()

const userStore = useUserStore()
const objectStore = useObjectStore()
const objectInfoStore = useObjectInfoStore()

const organizationName = 'ТОО АЗКО'

onMounted(async () => {
  await userStore.getUser()

  if (userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)) {
    await router.push('/objects')
    return
  }
  if (!userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER)) {
    await router.push('/map')
    return
  }
  await objectStore.getObjects()
  await objectInfoStore.getObjectInfo(route.params.id as string)
  await objectStore.getObjectAvatars(route.params.id as string)
  await objectStore.getObjectEscapeLadder(Number(route.params.id) as number)
})
</script>

<style lang="scss" scoped>
.edit {
  padding: 2em 0;
  font-family: 'Overpass', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2em;
  overflow-x: hidden;
  height: 100%;
  overflow-y: scroll;
}

.edit-parent {
  height: calc(100vh - 120px);
}
</style>
