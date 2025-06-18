import { ref } from 'vue'
import { defineStore } from 'pinia'
import { generalObjectInfo, subBuildingInfo } from '@/utils/LongFormsStorage'
import { useSnackbarStore } from './SnackbarStore'
import { objectService } from '@/services/object.service'
import { type UpdateObjectInfoPayload } from '@/types/ObjectBuilding'
import router from '@/router'
import { snakeCaseObjectInfoMap, type ObjectInfo } from '@/types/ObjectBuilding'

export const useObjectInfoStore = defineStore('objectInfoStore', () => {
  const isObjectInfoLoading = ref<boolean>(false)
  const isSaveLoading = ref<boolean>(false)
  const snackbarStore = useSnackbarStore()
  const progressPercentage = ref<number[]>([])
  const objectDocumentsInfo = ref<any[]>([])

  const updateComment = (comment: string, titleKey: string) => {
    objectDocumentsInfo.value.forEach((topic) => {
      if (topic.subParagraphs) {
        for (const sub of topic.subParagraphs) {
          for (const key of sub.keys) {
            if (key.title === titleKey) {
              key.comment = comment
            }
          }
        }
        return
      }
      for (const key of topic.keys) {
        if (key.title === titleKey) {
          key.comment = comment
        }
      }
    })
  }

  const getObjectInfo = async (objectId: string) => {
    try {
      isObjectInfoLoading.value = true
      const data = await objectService.getObjectInfo(objectId)
      fillObjectInfo({ ...data })
      isObjectInfoLoading.value = false
      return data
    } catch (error) {
      isObjectInfoLoading.value = false
      await router.push('/objects')
      snackbarStore.pullSnackbar(
        'Не удалось получить доступ к этому паспорту ПБО.',
        3000,
        '#d20f0d'
      )
    }
  }

  const fillObjectInfo = (objectValues: ObjectInfo) => {
    generalObjectInfo.value.forEach((object) => {
      if (Object.prototype.hasOwnProperty.call(objectValues, object.key)) {
        if (object.key === 'owner') {
          const owner = objectValues[object.key]
          object.value = `${owner?.last_name} ${owner?.first_name} ${owner?.middle_name}`
        } else {
          object.value = objectValues[object.key as keyof ObjectInfo]
        }
      }
    })

    subBuildingInfo.value.forEach((object) => {
      if (Object.prototype.hasOwnProperty.call(objectValues, object.key)) {
        object.value = objectValues[object.key as keyof ObjectInfo]
      }
    })

    objectDocumentsInfo.value = objectValues.documents
    calculateProgressForEachTopic()
  }

  const saveObjectInfo = async (objectId: string) => {
    try {
      isSaveLoading.value = true
      const payload = generateSavePayload()
      const message = await objectService.updateObjectInfo(objectId, payload)
      snackbarStore.pullSnackbar(message, 2000, '#5b9271')
      isSaveLoading.value = false
    } catch (error) {
      isSaveLoading.value = false
      snackbarStore.pullSnackbar('Не удалось сохранить измененные поля.', 3000, '#d20f0d')
    }
  }

  const generateSavePayload = () => {
    const combinedObject: UpdateObjectInfoPayload = {
      address: '',
      organization_type: '',
      organization_sub_type: '',
      organization_characteristics: '',
      organization_name: '',
      iin: '',
      rating: '3',
      escape_ladder: false
    }

    generalObjectInfo.value.forEach((item) => {
      combinedObject[
        snakeCaseObjectInfoMap[
          item.key as keyof typeof snakeCaseObjectInfoMap
        ] as keyof typeof combinedObject
      ] = item.value as never
    })

    subBuildingInfo.value.forEach((item) => {
      combinedObject[
        snakeCaseObjectInfoMap[
          item.key as keyof typeof snakeCaseObjectInfoMap
        ] as keyof typeof combinedObject
      ] = item.value as never
    })

    return combinedObject
  }

  const calculateProgressForTopic = (topic: any) => {
    let totalKeys = 0
    let filledKeys = 0

    if (topic.subParagraphs) {
      topic.subParagraphs.forEach((subPara: any) => {
        totalKeys += subPara.keys.length
        filledKeys += subPara.keys.filter((key: any) => key.files.length > 0).length
      })
    } else {
      totalKeys += topic.keys.length
      filledKeys += topic.keys.filter((key: any) => key.files.length > 0).length
    }

    if (totalKeys === 0) {
      return 0
    }

    return Math.floor((filledKeys / totalKeys) * 100)
  }

  const calculateProgressForEachTopic = () => {
    progressPercentage.value = objectDocumentsInfo.value.map((topic) =>
      calculateProgressForTopic(topic)
    )
  }

  const calculateGeneralProgress = (): number => {
    if (!objectDocumentsInfo.value || objectDocumentsInfo.value.length === 0) {
      return 0
    }

    let totalKeys = 0
    let filledKeys = 0

    objectDocumentsInfo.value.forEach((topic) => {
      if (topic.subParagraphs) {
        topic.subParagraphs.forEach((subPara: any) => {
          totalKeys += subPara.keys.length
          filledKeys += subPara.keys.filter((key: any) => key.files.length > 0).length
        })
      } else {
        totalKeys += topic.keys.length
        filledKeys += topic.keys.filter((key: any) => key.files.length > 0).length
      }
    })

    if (totalKeys === 0) {
      return 0
    }

    return Math.floor((filledKeys / totalKeys) * 100)
  }

  return {
    generalObjectInfo,
    subBuildingInfo,
    objectDocumentsInfo,
    isObjectInfoLoading,
    getObjectInfo,
    saveObjectInfo,
    isSaveLoading,
    updateComment,
    progressPercentage,
    calculateGeneralProgress,
    calculateProgressForEachTopic
  }
})
