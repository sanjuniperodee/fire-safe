<template>
  <v-card
    :loading="isDeleteLoading || isDownloadLoading"
    class="card"
    @mouseover="() => (isButtonsVisible = true)"
    @mouseleave="() => (isButtonsVisible = false)"
    elevation="0"
  >
    <v-icon
      color="#a1a1aa"
      style="font-size: 100px"
      >{{ `mdi-file-document` }}</v-icon
    >
    <v-card-text
      style=""
      :title="name"
      class="file-name"
      >{{ name }}</v-card-text
    >
    <transition name="download-button">
      <v-btn
        v-show="isButtonsVisible"
        :loading="isDeleteLoading || isDownloadLoading"
        :disabled="isDeleteLoading || isDownloadLoading"
        @click="() => downloadFile()"
        size="x-small"
        color="#5b9271"
        variant="elevated"
        class="text-white action-button"
        icon="mdi-download"
      ></v-btn>
    </transition>
    <transition name="delete-button">
      <v-btn
        v-show="isButtonsVisible"
        :loading="isDeleteLoading || isDownloadLoading"
        :disabled="isDeleteLoading || isDownloadLoading"
        @click="() => deleteFile()"
        color="#d20f0d"
        variant="elevated"
        class="text-white action-button"
        size="x-small"
        icon="mdi-delete"
        style="right: 35px"
      ></v-btn>
    </transition>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import type { FileBody } from '@/types/FileBody'
import { useFileStore } from '@/stores/FileStore'
import { fileService } from '@/services/file.service'
import { useRoute, useRouter } from 'vue-router'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { useObjectStore } from '@/stores/ObjectStore'

const isButtonsVisible = ref<boolean>(false)
const snackbarStore = useSnackbarStore()
const isDeleteLoading = ref<boolean>(false)
const fileStore = useFileStore()
const isDownloadLoading = ref<boolean>(false)
const router = useRouter()
const route = useRoute()
const objectInfoStore = useObjectInfoStore()
const objectStore = useObjectStore()

const props = defineProps<{
  name: string
  extension: string
  filebody: FileBody
}>()

const closeModal = () => {
  objectStore.isKeyDialogOpen = false
  fileStore.newFiles = []
  fileStore.files = []
}

const deleteFile = async () => {
  isDeleteLoading.value = true
  const deletingNewFile = fileStore.newFiles.find((file) => file.id === props.filebody.id)
  if (deletingNewFile) {
    fileStore.newFiles = fileStore.newFiles.filter((file) => file.id !== deletingNewFile.id)
    fileStore.files = fileStore.files.filter((file) => file.id !== deletingNewFile.id)
    isDeleteLoading.value = false
    snackbarStore.pullSnackbar('Документ успешно удален.', 2000, '#5b9271')
    return
  }

  try {
    await fileService.deleteFile(props.filebody.id)
    // on success
    isDeleteLoading.value = false
    await objectInfoStore.getObjectInfo(route.params.id as string)
    objectInfoStore.calculateProgressForEachTopic()
    closeModal()
    snackbarStore.pullSnackbar('Документ успешно удален.', 2000, '#5b9271')
    fileStore.files = fileStore.files.filter((file) => file.id !== props.filebody.id)
  } catch (error) {
    isDeleteLoading.value = false
    snackbarStore.pullSnackbar(
      'Не удалось удалить этот документ. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
  }
}

const downloadURL = (link: string, filename: string) => {
  const downloadLink = document.createElement('a')
  downloadLink.href = link
  downloadLink.download = filename
  document.body.appendChild(downloadLink)
  downloadLink.click()
  document.body.removeChild(downloadLink)
}

const downloadFile = async () => {
  isDownloadLoading.value = true
  const downloadingNewFile = fileStore.newFiles.find((file) => file.id === props.filebody.id)
  if (downloadingNewFile) {
    const link = URL.createObjectURL(downloadingNewFile.file as Blob)
    downloadURL(link, props.filebody.name)
    isDownloadLoading.value = false
    snackbarStore.pullSnackbar('Документ успешно скачан.', 2000, '#5b9271')
    return
  }

  try {
    const link = await fileService.downloadFile(props.filebody.id)
    // on success
    downloadURL(link, props.filebody.name)
    isDownloadLoading.value = false
    snackbarStore.pullSnackbar('Документ успешно скачан.', 2000, '#5b9271')
  } catch (error) {
    console.error(error)
    isDownloadLoading.value = false
    snackbarStore.pullSnackbar(
      'Не удалось скачать этот документ. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
  }
}
</script>

<style lang="scss" scoped>
.card {
  align-items: center;
  transition: 0.2s;
  width: 144px;
  height: 144px;
  font-size: 14px;
  display: flex;
  flex-direction: column;
}

.card:hover {
  background-color: #f4f4f5;
  transition: 0.2s;
}

.file-name {
  width: 144px;
  font-size: 12px;
  text-overflow: ellipsis !important;
  word-break: normal;
  word-wrap: break-word;
  white-space: nowrap;
  overflow: hidden;
}

.action-button {
  position: absolute;
  top: 0;
  right: 0;
  transition: 0.2s;
}

.download-button {
  &-enter-active,
  &-leave-active {
    transition: 0.2s;
  }

  &-enter-from,
  &-leave-to {
    opacity: 0;
  }
}

.delete-button {
  &-enter-active,
  &-leave-active {
    transition: 0.2s;
  }

  &-enter-from,
  &-leave-to {
    opacity: 0;
  }
}
</style>
