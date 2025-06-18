import { ref } from 'vue'
import { providerProfile } from '@/services/providerProfile.service'
import type { Experience } from '@/types/ProviderProfile'
import { defineStore } from 'pinia'

export const useExperienceStore = defineStore('experienceStore', () => {
  const experience = ref<Experience | null>(null)
  const experiences = ref<Experience[] | null>(null)
  const isLoading = ref<boolean>(false)

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const handleError = (error: any) => {
    console.error(error)
  }

  const createExperience = async (formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.createExperience(formData)
      experiences.value = experiences.value ? [...experiences.value, data] : [data]
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getExperiences = async () => {
    setLoading(true)
    try {
      experiences.value = await providerProfile.getExperiences()
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getExperience = async (id: number) => {
    setLoading(true)
    try {
      experience.value = await providerProfile.getExperience(id)
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const editExperience = async (id: number, formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.editExperience(id, formData)
      if (experiences.value) {
        const index = experiences.value.findIndex(item => item.id === id)
        if (index !== -1) {
          experiences.value[index] = data
        }
      }
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const deleteExperience = async (id: number) => {
    setLoading(true)
    try {
      await providerProfile.deleteExperience(id)
      if (experiences.value) {
        experiences.value = experiences.value.filter(item => item.id !== id)
      }
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  return {
    experience,
    experiences,
    isLoading,
    createExperience,
    getExperiences,
    getExperience,
    editExperience,
    deleteExperience,
  }
})
