import axios from 'axios'
import { type SubBuilding } from '@/types/ObjectBuilding'

class SubBuildingService {
  baseUrl: string
  token = localStorage.getItem('token')
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async createSubBuilding(id: number, body: SubBuilding) {
    const { data } = await axios.post(
      `${this.baseUrl}/api/v1/buildings/${id}/subbuildings/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + this.token
        }
      }
    )
    return data
  }

  async getSubBuildings(id: string): Promise<SubBuilding[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/buildings/${id}/subbuildings/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data.results
  }

  async getSubBuildingInfo(id: string, subId: string): Promise<SubBuilding> {
    const { data } = await axios.get(
      `${this.baseUrl}/api/v1/buildings/${id}/subbuildings/${subId}/`,
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + this.token
        }
      }
    )
    return data
  }

  async updateSubBuildingInfo(
    id: string,
    subId: string,
    body: Partial<SubBuilding>
  ): Promise<string> {
    await axios.patch(`${this.baseUrl}/api/v1/buildings/${id}/subbuildings/${subId}/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return 'Поля успешно обновлены.'
  }

  async deleteSubBuilding(id: string, subId: string): Promise<SubBuilding> {
    const { data } = await axios.delete(
      `${this.baseUrl}/api/v1/buildings/${id}/subbuildings/${subId}/`,
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + this.token
        }
      }
    )
    return data
  }

  async createSubBuildingAvatar(buildingId: string,subBuildingId :string, body: FormData) {
    const { data } = await axios.postForm
    (`${this.baseUrl}/api/v1/buildings/${buildingId}/subbuildings/${subBuildingId}/sub_building_images/upload/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getSubBuildingAvatar(buildingId: string, subBuildingId :string,) {
    const { data } = await axios.get
    (`${this.baseUrl}/api/v1/buildings/${buildingId}/subbuildings/${subBuildingId}/sub_building_images/list/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async deleteSubBuildingAvatar(buildingId: string,subBuildingId :string, imageId: string) {
    const { data } = await axios.delete
    (`${this.baseUrl}/api/v1/buildings/${buildingId}/subbuildings/${subBuildingId}/sub_building_images/delete/${imageId}/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }
}

export const subBuildingService = new SubBuildingService(import.meta.env.VITE_BACKEND_URL)
