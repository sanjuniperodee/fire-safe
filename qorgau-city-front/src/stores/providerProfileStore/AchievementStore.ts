import { ref } from 'vue'
import { providerProfile } from '@/services/providerProfile.service'
import type { Achievement } from '@/types/ProviderProfile'
import { defineStore } from 'pinia'

export const useAchievementStore = defineStore('achievementStore', () => {
  const achievement = ref<Achievement | null>(null)
  const achievements = ref<Achievement[] | null>(null)
  const isLoading = ref<boolean>(false)

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const handleError = (error: any) => {
    console.error(error)
  }

  const createAchievement = async (formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.createAchievement(formData)
      achievements.value = achievements.value ? [...achievements.value, data] : [data]
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getAchievements = async () => {
    setLoading(true)
    try {
      achievements.value = await providerProfile.getAchievements()
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getAchievement = async (id: number) => {
    setLoading(true)
    try {
      achievement.value = await providerProfile.getAchievement(id)
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const editAchievement = async (id: number, formData: FormData) => {
    setLoading(true)
    try {
      const data = await providerProfile.editAchievement(id, formData)
      if (achievements.value) {
        const index = achievements.value.findIndex(item => item.id === id)
        if (index !== -1) {
          achievements.value[index] = data
        }
      }
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const deleteAchievement = async (id: number) => {
    setLoading(true)
    try {
      await providerProfile.deleteAchievement(id)
      if (achievements.value) {
        achievements.value = achievements.value.filter(item => item.id !== id)
      }
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  return {
    achievement,
    achievements,
    isLoading,
    createAchievement,
    getAchievements,
    getAchievement,
    editAchievement,
    deleteAchievement,
  }
})
