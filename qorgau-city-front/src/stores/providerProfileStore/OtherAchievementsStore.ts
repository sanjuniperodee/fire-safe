import { ref } from 'vue'
import { providerProfile } from '@/services/providerProfile.service'
import type { OtherAchievements } from '@/types/ProviderProfile'
import { defineStore } from 'pinia'

export const useOtherAchievementsStore = defineStore('otherAchievementsStore', () => {
  const otherAchievement = ref<OtherAchievements | null>(null)
  const otherAchievements = ref<OtherAchievements[] | null>(null)
  const isLoading = ref<boolean>(false)

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const handleError = (error: any) => {
    console.error(error)
  }

  const createOtherAchievements = async (formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.createOtherAchievements(formData)
      otherAchievements.value = otherAchievements.value ? [...otherAchievements.value, data] : [data]
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getOtherAchievements = async () => {
    setLoading(true)
    try {
      otherAchievements.value = await providerProfile.getOtherAchievements()
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getOtherAchievement = async (id: number) => {
    setLoading(true)
    try {
      otherAchievement.value = await providerProfile.getOtherAchievement(id)
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const editOtherAchievement = async (id: number, formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.editOtherAchievements(id, formData)
      if (otherAchievements.value) {
        const index = otherAchievements.value.findIndex(item => item.id === id)
        if (index !== -1) {
          otherAchievements.value[index] = data
        }
      }
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const deleteOtherAchievement = async (id: number) => {
    setLoading(true)
    try {
      await providerProfile.deleteOtherAchievements(id)
      if (otherAchievements.value) {
        otherAchievements.value = otherAchievements.value.filter(item => item.id !== id)
      }
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  return {
    otherAchievement,
    otherAchievements,
    isLoading,
    createOtherAchievements,
    getOtherAchievements,
    getOtherAchievement,
    editOtherAchievement,
    deleteOtherAchievement,
  }
})
