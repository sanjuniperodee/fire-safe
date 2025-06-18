<template>
  <v-card
    :loading="isDownloadLoading"
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
        :loading="isDownloadLoading"
        :disabled="isDownloadLoading"
        @click="() => downloadFile()"
        size="x-small"
        color="#5b9271"
        variant="elevated"
        class="text-white action-button"
        icon="mdi-download"
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

const isButtonsVisible = ref<boolean>(false)
const snackbarStore = useSnackbarStore()
const fileStore = useFileStore()
const isDownloadLoading = ref<boolean>(false)

const props = defineProps<{
  name: string
  extension: string
  filebody: FileBody
}>()

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
