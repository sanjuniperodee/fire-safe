import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { FileBody } from '@/types/FileBody'
import { useSnackbarStore } from './SnackbarStore'
import { fileService } from '@/services/file.service'

export const useFileStore = defineStore('fileStore', {
  state: () => {
    const snackbarStore = useSnackbarStore()

    const files = ref<FileBody[]>([])
    const newFiles = ref<(FileBody & { file: File })[]>([])
    const isFilesLoading = ref<boolean>(false)

    const getFiles = async (filesData: FileBody[]) => {
      try {
        isFilesLoading.value = true
        // on success
        files.value = filesData
        newFiles.value = []
        isFilesLoading.value = false
      } catch (error) {
        isFilesLoading.value = false
        snackbarStore.pullSnackbar(
          'Не удалось загрузить ваши файлы. Попробуйте позже.',
          3000,
          '#d20f0d'
        )
      }
    }

    return {
      getFiles,
      files,
      newFiles,
      isFilesLoading
    }
  }
})
