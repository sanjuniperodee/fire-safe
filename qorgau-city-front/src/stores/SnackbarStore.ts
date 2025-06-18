import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useSnackbarStore = defineStore('snackbarStore', {
  state: () => {
    const isOpen = ref(false)

    const text = ref('')
    const timeout = ref(0)
    const color = ref('')

    const pullSnackbar = (newText: string, newTimeout: number, newColor: string) => {
      text.value = newText
      timeout.value = newTimeout
      color.value = newColor
      isOpen.value = true
    }

    const changeIsOpen = () => {
      isOpen.value = !isOpen.value
    }
    return {
      isOpen,
      changeIsOpen,
      text,
      timeout,
      color,

      pullSnackbar
    }
  }
})
