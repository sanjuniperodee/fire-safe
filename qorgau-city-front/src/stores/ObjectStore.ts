import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ObjectBuilding, RatingOption, Remark, RemarkContent, DocumentRemark,  RemarkContentInfo, ObjectInfo, Avatar, ImagesLadder, UpdateObjectInfoPayload, UpdateObject, PdfDocuments } from '@/types/ObjectBuilding'
import { objectService } from '@/services/object.service'
import axios from 'axios'

export const useObjectStore = defineStore('objectStore', () => {
  const objects = ref<ObjectBuilding[]>([])
  const myObjects = ref<ObjectBuilding[]>([])

  const remarks = ref<RemarkContentInfo[]>([])
  const remarkById = ref<Remark>()

  const currentStep = ref(1)
  const isKeyDialogOpen = ref(false)

  const objectById = ref<ObjectInfo | null>(null)
  const objectImages = ref<Avatar[] | null>(null)
  const objectEscapeLadderImages = ref<ImagesLadder[] | null>(null)

  const uploadedFiles = ref<{ name: string; url: string }[]>([])
  const uploadedAvatar = ref<{ name: string; url: string }[]>([])
  const uploadedSubbuidingImages = ref<{ name: string; url: string }[]>([])
  const files = ref<FileList | null>(null)
  const avatar = ref<FileList | null>(null)
  const subbuildingImages = ref<FileList | null>(null)

  const pdfDocuments = ref<PdfDocuments[]>([]) 

  const getObjectById = async (objectId: string) => {
    try {
      objectById.value = await objectService.getObjectInfo(objectId)
      return objectById
    } catch (error) {
      throw new Error('Не удалось получить паспорты ПБО.')
    }
  }

  const getObjects = async () => {
    try {
      const fetchedObjects = await objectService.getObjects()
      setObjects(fetchedObjects)
    } catch (error) {
      throw new Error('Не удалось получить паспорты ПБО.')
    }
  }

  const updateRating = async (objectId: string, rating: RatingOption) => {
    try {
      return await objectService.updateObjectInfo(objectId, {
        rating: rating
      })
    } catch (error) {
      console.log('error => ', error)
      throw new Error('Не удалось обновить ваш объект.')
    }
  }

  const updateObject = async(objectId: number, body: UpdateObject) => {
  try {
      return await objectService.updateObject(objectId, body)
    } catch (error) {
      console.log('error => ', error)
      throw new Error('Не удалось обновить ваш объект.')
    }
  }

  const deleteObject = async (objectId: number) => {
    try {
      const message = await objectService.deleteObject(objectId)
      objects.value = objects.value.filter((object) => object.id !== objectId)
      return message
    } catch (error) {
      throw new Error('Не удалось удалить паспорт ПБО.')
    }
  }

  const getMyObjects = async () => {
    try {
      const fetchedObjects = await objectService.getMyObjects()
      setMyObjects(fetchedObjects)
    } catch (error) {
      throw new Error('Не удалось получить паспорты ПБО.')
    }
  }

  const saveMyObjects = async (objectId: string) => {
    try {
      myObjects.value.push(await objectService.saveMyObject(objectId))
      return myObjects.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось добавить ваш объект.')
    }
  }

  const deleteMyObjects = async (objectId: string) => {
    try {
      return await objectService.deleteMyObject(objectId)
    } catch (error) {
      throw new Error('Не удалось удалить ваш объект.')
    }
  }

  const createRemark = async (objectId: string, body: RemarkContent) => {
    try {
      remarks.value.push(await objectService.createRemark(objectId, body))
      return remarks.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось создать примечание.')
    }
  }

  const getRemarks = async ( objectId: string ) => {
    try {
      remarks.value = await objectService.getRemarks(objectId)
      return remarks.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось получить примечания.')
    }
  }

  const getRemarkById = async ( objectId: string, remarkId: string ) => {
    try {
      remarkById.value = await objectService.getRemarkById(objectId, remarkId)
      return remarkById.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось получить примечание.')
    }
  }

  const updateRemark = async (objectId: string, body: Partial<Remark>) => {
    try {
      await objectService.updateRemark(objectId, body)
      return remarks.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось обновить примечание.')
    }
  }

  const deleteRemark = async ( objectId: string, remarkId: string ) => {
    try {
      await objectService.deleteRemark(objectId, remarkId)
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось удалить примечание.')
    }
  }

  const createDocumentRemark = async (body: DocumentRemark) => {
    try {
      await objectService.createDocumentRemark(body)
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось создать примечание.')
    }
  }

  const createObjectAvatar = async (buildingId: number, body: FormData) => {
    try {
      const data = await objectService.createObjectAvatar(buildingId, body)
      objectImages.value?.push(data)
      return objectImages.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось создать примечание.')
    }
  }

  const getObjectAvatars = async (buildingId: string) => {
    try {
      objectImages.value = await objectService.getObjectAvatar(buildingId)
      return objectImages.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось создать примечание.')
    }
  }

  const deleteObjectAvatar = async (buildingId: number, imageId:string) => {
    try {
      await objectService.deleteObjectAvatar(buildingId, imageId)
      objectImages.value = objectImages.value?.filter(image => image.id !== Number(imageId)) || null
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось удалить примечание.')
    }
  }

  // escape ladder
  
  const createEscapeLadder = async (buildingId: number, body: FormData) => {
    try {
      const data = await objectService.uploadedImageLadder(buildingId, body)
      objectEscapeLadderImages.value?.push(data)
      return objectEscapeLadderImages.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось создать примечание.')
    }
  }

  const getObjectEscapeLadder = async (buildingId: number) => {
    try {
      objectEscapeLadderImages.value = await objectService.getImageLadder(buildingId)
      return objectEscapeLadderImages.value
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось создать примечание.')
    }
  }

  const deleteObjectEscapeLadder = async (buildingId: number, imageId:string) => {
    try {
      await objectService.deleteImageLadder(buildingId, imageId)
      objectEscapeLadderImages.value = objectEscapeLadderImages.value?.filter(image => image.id !== Number(imageId)) || null
    } catch (error) {
      console.error('Error => ', error)
      throw new Error('Не удалось удалить примечание.')
    }
  }

  // Object image 

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

const handleAvatarChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    const newFiles = Array.from(target.files).map((file) => ({
      name: file.name,
      url: URL.createObjectURL(file)
    }))
    uploadedAvatar.value = [...uploadedAvatar.value, ...newFiles]
    avatar.value = target.files
  } else {
    uploadedAvatar.value = []  // добавьте это, если хотите очистить, когда файлов нет
  }
}

const uploadAvatar = async (buildingId: number) => {
  if (!avatar.value) return

  for (const file of Array.from(avatar.value)) {
    const formData = new FormData()
    formData.append("images", file)

    try {
      console.log(formData)
      const response =  await objectService.createObjectAvatar(buildingId, formData)
      console.log("Файл успешно загружен:", response)
    } catch (error) {
      console.error("Ошибка загрузки файла:", error)
    }
  }
}

// Функция для загрузки каждого файла
const uploadFiles = async (buildingId: number) => {
  if (!files.value) return

  for (const file of Array.from(files.value)) {
    const formData = new FormData()
    formData.append("images", file)

    try {
      console.log(formData)
      const response = await objectService.uploadedImageLadder(buildingId, formData)
      console.log("Файл успешно загружен:", response)
    } catch (error) {
      console.error("Ошибка загрузки файла:", error)
    }
  }
}

const handleSubbuildingImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    const newFiles = Array.from(target.files).map((file) => ({
      name: file.name,
      url: URL.createObjectURL(file)
    }))
    uploadedSubbuidingImages.value = [...uploadedAvatar.value, ...newFiles]
    subbuildingImages.value = target.files
  } else {
    uploadedSubbuidingImages.value = []  // добавьте это, если хотите очистить, когда файлов нет
  }
}

const uploadSubbuidingImages = async (buildingId: number, subbuildId: number) => {
  if (!subbuildingImages.value) return

  for (const file of Array.from(subbuildingImages.value)) {
    const formData = new FormData()
    formData.append("images", file)

    try {
      console.log(formData)
      const response = await objectService.createSubBuildingImages(buildingId, subbuildId, formData)
      console.log("Файл успешно загружен:", response)
    } catch (error) {
      console.error("Ошибка загрузки файла:", error)
    }
  }
}

const createGeneratePdf = async (id: number) => {
  try {
    await objectService.createGeneratePdf(id)
  } catch (error) {
    console.error(error)
  }
}

const getPdfDocument = async (id: number) => {
  try {
    pdfDocuments.value = await objectService.getPdfDocument(id)
  } catch (error) {
    console.error(error)
  }
}

const removeFile = (fileName: string) => {
    uploadedFiles.value = uploadedFiles.value.filter((file) => file.name !== fileName)
}

const removeAvatar = (fileName: string) => {
    uploadedAvatar.value = uploadedAvatar.value.filter((file) => file.name !== fileName)
}

const removeSubbuildingImage = (fileName: string) => {
    uploadedSubbuidingImages.value = uploadedSubbuidingImages.value.filter((file) => file.name !== fileName)
}

  // 

  const setCurrentStep = (step: number) => {
    currentStep.value = step
  }

  const setObjects = (newObjects: ObjectBuilding[]) => {
    objects.value = newObjects
  }

  const setMyObjects = (newObjects: ObjectBuilding[]) => {
    myObjects.value = newObjects
  }

  const addObject = (newObject: ObjectBuilding) => {
    objects.value.push(newObject)
  }



  return {
    objects,
    myObjects,
    currentStep,
    isKeyDialogOpen,
    remarks,
    remarkById,
    objectById,
    objectImages,
    objectEscapeLadderImages,
    getObjectById,
    setObjects,
    addObject,
    deleteObject,
    getObjects,
    getMyObjects,
    setCurrentStep,
    updateRating,
    saveMyObjects,
    deleteMyObjects,
    createRemark,
    getRemarks,
    getRemarkById,
    updateRemark,
    deleteRemark,
    createObjectAvatar,
    createEscapeLadder,
    getObjectAvatars,
    deleteObjectAvatar,
    handleFileChange,
    handleAvatarChange,
    handleSubbuildingImageChange,
    uploadAvatar,
    uploadFiles,
    uploadSubbuidingImages,
    removeFile,
    removeAvatar,
    removeSubbuildingImage,
    getObjectEscapeLadder,
    deleteObjectEscapeLadder,
    uploadedFiles,
    uploadedAvatar,
    uploadedSubbuidingImages,
    files,
    avatar,
    subbuildingImages,
    updateObject,
    createDocumentRemark,
    createGeneratePdf,
    getPdfDocument,
    pdfDocuments,
  }
})
