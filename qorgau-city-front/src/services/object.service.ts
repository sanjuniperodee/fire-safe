import axios from 'axios'
import type {
  ObjectBuilding, CreateObjectValidator, UpdateObjectInfoPayload,
  BuildingCoordinatesValidator, ObjectInfo, Remark, RemarkContent, DocumentRemark, UpdateObject
} from '@/types/ObjectBuilding'
import type { HistoryAction } from '@/types/HistoryAction'
import { th } from 'date-fns/locale'

class ObjectService {
  baseUrl: string
  token = localStorage.getItem('token')
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async getObjects(): Promise<ObjectBuilding[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data.results
  }

  async deleteObject(id: number): Promise<string> {
    await axios.delete(`${this.baseUrl}/api/v1/buildings/${id}/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return 'Ваш Паспорт ПБО был удален из нашей информационной системы.'
  }

  async getObjectInfo(objectId: string): Promise<ObjectInfo> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${objectId}/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async updateObjectInfo(
    objectId: string,
    body: Partial<UpdateObjectInfoPayload>
  ): Promise<string> {
    await axios.patch(`${this.baseUrl}/api/v1/buildings/${objectId}/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return 'Поля успешно обновлены.'
  }

  async updateObject(objectId: number, body: Partial<UpdateObject>) {
    await axios.patch(`${this.baseUrl}/api/v1/buildings/${objectId}/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return 'Поля успешно обновлены.'
  }

  async createObject(body: CreateObjectValidator): Promise<ObjectBuilding> {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/buildings/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    console.log(body)
    return data
  }

  async getHistories(objectId: string): Promise<HistoryAction[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${objectId}/history/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return data.results
  }

  async createCoordinates(body: BuildingCoordinatesValidator): Promise<ObjectBuilding> {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/building/coordinates/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async updateCoordinates(id: number, body: BuildingCoordinatesValidator): Promise<ObjectBuilding> {
    const { data } = await axios.patch(`${this.baseUrl}/api/v1/building/coordinates/${id}/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getMyObjects(): Promise<ObjectBuilding[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/my_objects/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return data.results
  }

  async saveMyObject(objectId: string): Promise<ObjectBuilding> {
    const { data } = await axios.patch(
      `${this.baseUrl}/api/v1/buildings/${objectId}/attach/`,
      {},
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + this.token
        }
      }
    )
    return data
  }

  async deleteMyObject(objectId: string): Promise<ObjectBuilding> {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/buildings/${objectId}/attach/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return data
  }

  async createRemark(id: string, body: RemarkContent) {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/buildings/${id}/remark/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getRemarks(id: string) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${id}/get_remarks/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getRemarkById(buildingId: string, remarkId: string) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${buildingId}/remark/${remarkId}/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async updateRemark(id: string, body: Partial<Remark>) {
    const { data } = await axios.patch(`${this.baseUrl}/api/v1/buildings/${id}/remark/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async deleteRemark(buildingId: string, remarkId: string) {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/buildings/${buildingId}/remark/${remarkId}`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async createObjectAvatar(buildingId: number, body: FormData) {
    const { data } = await axios.postForm(`${this.baseUrl}/api/v1/buildings/${buildingId}/building_images/upload/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getObjectAvatar(buildingId: string) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${buildingId}/building_images/list/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async deleteObjectAvatar(buildingId: number, image_id: string) {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/buildings/${buildingId}/building_images/delete_image/${image_id}/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async uploadedImageLadder(buildingId: number, body: FormData) {
    const { data } = await axios.postForm(`${this.baseUrl}/api/v1/buildings/${buildingId}/escape-ladder/upload/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getImageLadder(buildingId: number) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${buildingId}/escape-ladder/images/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async deleteImageLadder(buildingId: number, image_id: string) {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/buildings/${buildingId}/escape-ladder/delete/${image_id}/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async createSubBuildingImages(buildingId: number, subbuildinId: number, body: FormData) {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/buildings/${buildingId}/subbuildings/${subbuildinId}/sub_building_images/upload/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getSubBuildingImages(buildingId: number, subbuildId: number) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${buildingId}/subbuildings/${subbuildId}/sub_building_images/list/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async deleteSubBuildingImages(buildingId: number, subbuildId: number, imageId: number) {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/buildings/${buildingId}/subbuildings/${subbuildId}/sub_building_images/delete/${imageId}/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async createDocumentRemark(body: DocumentRemark) {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/document/document_remark/`, body, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async createGeneratePdf(id: number) {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/buildings/${id}/generate-pdf/`, {}, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${this.token}`
      }
    }
    )
    return data
  }

  async getPdfDocument(id: number) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${id}/pdf-documents/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }
}

export const objectService = new ObjectService(import.meta.env.VITE_BACKEND_URL)
