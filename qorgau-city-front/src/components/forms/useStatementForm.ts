import { ref, computed, watch } from 'vue'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { statementService } from '@/services/statement.service'
import type { StatementValidator } from '@/types/Statement'

export function useStatementForm() {
  const snackbarStore = useSnackbarStore()
  const isUploadLoading = ref<boolean>(false)
  const selectedCategories = ref<number[]>([])
  const files = ref<FileList | null>(null)
  const uploadedFiles = ref<{ name: string; url: string }[]>([])

  const statement = ref<StatementValidator>({
    categories: [],
    text: '',
    service_time: '',
    location: '',
    min_price: 0,
    max_price: 0,
    uploaded_media: [],
  })

  const day = ref<string>('')
  const hour = ref<string>('')

  const serviceTime = computed(() => {
    if (day.value && hour.value) {
      return `${day.value}T${hour.value}`
    }
    return ''
  })

  watch(serviceTime, (newVal) => {
    statement.value.service_time = newVal
  })

  watch(selectedCategories, (newSelectedCategories) => {
    statement.value.categories = newSelectedCategories.map((id) => id)
  })

  const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files) {
      const newFiles = Array.from(target.files).map((file) => ({
        name: file.name,
        url: URL.createObjectURL(file)
      }))
      uploadedFiles.value = [...uploadedFiles.value, ...newFiles]
      files.value = target.files
    }
  }

  const removeFile = (fileName: string) => {
    uploadedFiles.value = uploadedFiles.value.filter((file) => file.name !== fileName)
  }

  const resetForm = () => {
    selectedCategories.value = []
    files.value = null
    uploadedFiles.value = []
    statement.value = {
      categories: [],
      text: '',
      service_time: '',
      location: '',
      min_price: 0,
      max_price: 0,
      uploaded_media: []
    }
    day.value = ''
    hour.value = ''
  }

  const validateForm = () => {
    const errors: string[] = []

    if (selectedCategories.value.length === 0) errors.push('Выберите хотя бы одну категорию.')
    if (!statement.value.text) errors.push('Поле "Текст" обязательно для заполнения.')
    if (!statement.value.location) errors.push('Поле "Место услуги" обязательно для заполнения.')
    if (
      !statement.value.min_price ||
      isNaN(statement.value.min_price) ||
      statement.value.min_price <= 0
    )
      errors.push('Поле "Минимальная цена" должно быть числом больше нуля.')
    if (
      !statement.value.max_price ||
      isNaN(statement.value.max_price) ||
      statement.value.max_price <= 0
    )
      errors.push('Поле "Максимальная цена" должно быть числом больше нуля.')

    return errors[0]
  }

  const submitForm = async (toggleModal: () => void) => {
    const validationErrors = validateForm()

    if (validationErrors) {
      snackbarStore.pullSnackbar(validationErrors, 3000, '#d20f0d')
      return
    } else if (files.value === null) {
      snackbarStore.pullSnackbar('Вы должны загрузить хотя бы одно "Фото/Видео"', 3000, '#d20f0d')
      return
    }

    const formData = new FormData()
    formData.append('text', statement.value.text)
    formData.append('service_time', statement.value.service_time)
    formData.append('location', statement.value.location)
    formData.append('min_price', statement.value.min_price.toString())
    formData.append('max_price', statement.value.max_price.toString())
    formData.append('categories', statement.value.categories.toString())

    if (files.value) {
      for (let i = 0; i < files.value.length; i++) {
        formData.append('uploaded_media', files.value[i])
      }
    }

    try {
      isUploadLoading.value = true
      await statementService.createStatement(formData)
      snackbarStore.pullSnackbar('Объявление успешно создано.', 3000, '#5b9271')
      isUploadLoading.value = false
      resetForm()
      toggleModal()
    } catch (error) {
      console.error('Ошибка при отправке данных:', error)
      snackbarStore.pullSnackbar('Не удалось создать объявление.', 3000, '#d20f0d')
    }
  }

  return {
    isUploadLoading,
    selectedCategories,
    files,
    uploadedFiles,
    statement,
    day,
    hour,
    serviceTime,
    handleFileChange,
    removeFile,
    resetForm,
    validateForm,
    submitForm
  }
}
