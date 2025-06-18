<template>
  <LoaderSpinner v-if="loading"/>

  <v-container>
    COMPLAINT
  </v-container>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'

const userStore = useUserStore()
const userId = userStore.user?.id
const loading = false

// const uploadFile = (e: Event) => {
//   const target = e.target as HTMLInputElement
//   const files = target.files
//   if (files && files.length > 0) {
//     const selectedFile: File = files[0]
//     const fileBody = {
//       id: Date.now(),
//       message: selectedFile.name
//     }
//     const reader = new FileReader()
//
//     reader.onloadend = () => {
//       // @ts-ignore
//       chatMessages.value.push(fileBody)
//     }
//     reader.readAsDataURL(selectedFile)
//   }
// }

</script>

<style scoped>
.custom-file-upload input[type='file'] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  cursor: pointer;
}

</style>
