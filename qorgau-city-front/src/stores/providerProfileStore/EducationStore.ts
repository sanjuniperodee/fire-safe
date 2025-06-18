import { ref } from 'vue'
import { providerProfile } from '@/services/providerProfile.service'
import type { Education } from '@/types/ProviderProfile'
import { defineStore } from 'pinia'

export const useEducationStore = defineStore('educationStore', ()=> {
  const education = ref<Education | null>(null)
  const educations = ref<Education[] | null>(null)
  const isLoading = ref<boolean>(false)

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }
  const handleError = (error: any) => {
    console.error(error)
  }

  const createEducation = async (formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.createEducation(formData)
      educations.value = educations.value ? [...educations.value, data] : [data]
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getEducations = async () => {
    setLoading(true)
    try {
      educations.value = await providerProfile.getEducations()
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getEducation = async (id: number) => {
    setLoading(true)
    try {
      education.value = await providerProfile.getEducation(id)
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const editEducation = async (id: number, formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.editEducation(id, formData)
      if (educations.value) {
        const index = educations.value.findIndex(item => item.id === id)
        if (index !== -1) {
          educations.value[index] = data
        }
      }
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const deleteEducation = async (id: number) => {
    setLoading(true)
    try {
      await providerProfile.deleteEducation(id)
      if (educations.value) {
        educations.value = educations.value.filter(item => item.id !== id)
      }
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  return {
    education,
    educations,
    isLoading,
    createEducation,
    getEducations,
    getEducation,
    editEducation,
    deleteEducation,
  }
})
