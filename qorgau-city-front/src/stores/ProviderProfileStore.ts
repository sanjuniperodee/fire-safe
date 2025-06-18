import { defineStore } from 'pinia'
import { type Ref, ref } from 'vue'
import { providerProfile } from '@/services/providerProfile.service'
import type { Education, Experience, Achievement, OtherAchievements } from '@/types/ProviderProfile'
import { statementService } from '@/services/statement.service'

type ProfileItem = Education | Experience | Achievement | OtherAchievements

export const useProviderProfileStore = defineStore('providerProfile', () => {
  const education = ref<Education | null>(null)
  const educations = ref<Education[] | null>(null)
  const experience = ref<Experience | null>(null)
  const experiences = ref<Experience[] | null>(null)
  const achievement = ref<Achievement | null>(null)
  const achievements = ref<Achievement[] | null>(null)
  const otherAchievement = ref<OtherAchievements | null>(null)
  const otherAchievements = ref<OtherAchievements[] | null>(null)

  const isLoading = ref<boolean>(false)

  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  const handleError = (error: any) => {
    console.error(error)
    // You might want to add more error handling logic here
  }

  const createItem = async <T extends ProfileItem>(
    createFunction: (formData: FormData) => Promise<T>,
    itemsRef: Ref<T[] | null>,
    formData: FormData
  ) => {
    setLoading(true)
    try {
      const data = await createFunction(formData)
      itemsRef.value = itemsRef.value ? [...itemsRef.value, data] : [data]
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getItems = async <T extends ProfileItem>(
    getFunction: () => Promise<T[]>,
    itemsRef: Ref<T[] | null>
  ) => {
    setLoading(true)
    try {
      itemsRef.value = await getFunction()
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const getItem = async <T extends ProfileItem>(
    getFunction: (id: number) => Promise<T>,
    itemRef: Ref<T | null>,
    id: number
  ) => {
    setLoading(true)
    try {
      itemRef.value = await getFunction(id)
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const editItem = async <T extends ProfileItem>(
    editFunction: (id: number, formData: FormData) => Promise<T>,
    itemsRef: Ref<T[] | null>,
    id: number,
    formData: FormData
  ) => {
    setLoading(true)
    try {
      const data = await editFunction(id, formData)
      if (itemsRef.value) {
        const index = itemsRef.value.findIndex(item => (item as any).id === id)
        if (index !== -1) {
          itemsRef.value[index] = data
        }
      }
      return data
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  const deleteItem = async <T extends ProfileItem>(
    deleteFunction: (id: number) => Promise<void>,
    itemsRef: Ref<T[] | null>,
    id: number
  ) => {
    setLoading(true)
    try {
      await deleteFunction(id)
      if (itemsRef.value) {
        itemsRef.value = itemsRef.value.filter(item => (item as any).id !== id)
      }
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
    }
  }

  // Education
  const createEducation = (formData: FormData) => createItem(providerProfile.createEducation, educations, formData)

  const getEducations = async() => {
    setLoading(true)
    try {
      educations.value = await providerProfile.getEducations()
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }
  const getEducation = async(id: number) => {
    setLoading(true)
    try {
      education.value = await providerProfile.getEducation(id)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }
  const editEducation = (id: number, formData: FormData) => editItem(providerProfile.editEducation, educations, id, formData)
  const deleteEducation = (id: number) => deleteItem(providerProfile.deleteEducation, educations, id)

  // Experience
  const createExperience = (formData: FormData) => createItem(providerProfile.createExperience, experiences, formData)
  const getExperiences = async() => {
    setLoading(true)
    try {
      experiences.value = await providerProfile.getExperiences()
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }
  const getExperience = (id: number) => getItem(providerProfile.getExperience, experience, id)
  const editExperience = (id: number, formData: FormData) => editItem(providerProfile.editExperience, experiences, id, formData)
  const deleteExperience = (id: number) => deleteItem(providerProfile.deleteExperience, experiences, id)

  // Achievement
  const createAchievement = (formData: FormData) => createItem(providerProfile.createAchievement, achievements, formData)
  const getAchievements = async() => {
    setLoading(true)
    try {
      achievements.value = await providerProfile.getAchievements()
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getAchievement = (id: number) => getItem(providerProfile.getAchievement, achievement, id)
  const editAchievement = (id: number, formData: FormData) => editItem(providerProfile.editAchievement, achievements, id, formData)
  const deleteAchievement = (id: number) => deleteItem(providerProfile.deleteAchievement, achievements, id)

  // OtherAchievements
  const createOtherAchievements = (formData: FormData) => createItem(providerProfile.createOtherAchievements, otherAchievements, formData)

  const getOtherAchievements = async() => {
    setLoading(true)
    try {
      otherAchievements.value = await providerProfile.getOtherAchievements()
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }
  const getOtherAchievement = (id: number) => getItem(providerProfile.getOtherAchievement, otherAchievement, id)
  const editOtherAchievement = (id: number, formData: FormData) => editItem(providerProfile.editOtherAchievements, otherAchievements, id, formData)
  const deleteOtherAchievement = (id: number) => deleteItem(providerProfile.deleteOtherAchievements, otherAchievements, id)

  return {
    education,
    educations,
    experience,
    experiences,
    achievement,
    achievements,
    otherAchievement,
    otherAchievements,
    isLoading,
    createEducation,
    getEducations,
    getEducation,
    editEducation,
    deleteEducation,
    createExperience,
    getExperiences,
    getExperience,
    editExperience,
    deleteExperience,
    createAchievement,
    getAchievements,
    getAchievement,
    editAchievement,
    deleteAchievement,
    createOtherAchievements,
    getOtherAchievements,
    getOtherAchievement,
    editOtherAchievement,
    deleteOtherAchievement,
  }
})