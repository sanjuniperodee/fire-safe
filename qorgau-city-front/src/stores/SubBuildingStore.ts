import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { SubBuilding } from '@/types/ObjectBuilding'
import { subBuildingService } from '@/services/subBuilding.service'

export const useSubBuildingStore = defineStore('subBuildingStore', () => {
  const subBuildings = ref<SubBuilding[]>([])
  const currentSubBuilding = ref<SubBuilding | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const editingFields = ref<Record<keyof SubBuilding, boolean>>(
    {} as Record<keyof SubBuilding, boolean>
  )

  const getSubBuildings = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      subBuildings.value = await subBuildingService.getSubBuildings(id)
    } catch (err) {
      error.value = 'Ошибка при загрузке подзданий.'
    } finally {
      loading.value = false
    }
  }

  const getSubBuildingInfo = async (id: string, subId: string) => {
    try {
      loading.value = true
      error.value = null
      currentSubBuilding.value = await subBuildingService.getSubBuildingInfo(id, subId)
      initEditingFields()
      loading.value = false
    } catch (error) {
      console.error('Failed to fetch sub-building info:', error)
    }
  }
  // EDIT START
  const initEditingFields = () => {
    if (currentSubBuilding.value) {
      Object.keys(currentSubBuilding.value).forEach((key) => {
        editingFields.value[key as keyof SubBuilding] = false
      })
    }
  }

  const toggleEditing = async (field: keyof SubBuilding) => {
    editingFields.value[field] = !editingFields.value[field]
  }

  const updateSubBuildingInfo = async (
    field: keyof SubBuilding,
    objectId: string,
    subBuildingId: string
  ) => {
    if (currentSubBuilding.value) {
      try {
        await subBuildingService.updateSubBuildingInfo(objectId, subBuildingId, {
          [field]: currentSubBuilding.value[field]
        })
        // Закрываем поле редактирования только после успешного обновления данных
        editingFields.value[field] = false
      } catch (error) {
        console.error(`Failed to update ${field}:`, error)
      }
    }
  }
  // EDIT END

  const createSubBuilding = async (id: number, body: SubBuilding) => {
    loading.value = true
    error.value = null
    try {
      const newSubBuilding = await subBuildingService.createSubBuilding(id, body)
      subBuildings.value.push(newSubBuilding)
      return newSubBuilding
    } catch (err) {
      error.value = 'Ошибка при создании подздания.'
    } finally {
      loading.value = false
    }
  }

  const deleteSubBuilding = async (id: string, subId: string) => {
    loading.value = true
    error.value = null
    try {
      await subBuildingService.deleteSubBuilding(id, subId)
    } catch (err) {
      error.value = 'Ошибка при удалении подздания.'
    } finally {
      loading.value = false
    }
  }

  return {
    subBuildings,
    currentSubBuilding,
    loading,
    error,
    editingFields,
    getSubBuildingInfo,
    toggleEditing,
    getSubBuildings,
    createSubBuilding,
    updateSubBuildingInfo,
    deleteSubBuilding
  }
})
