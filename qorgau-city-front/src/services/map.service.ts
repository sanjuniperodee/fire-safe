import axios from 'axios'
import type { ObjectCoordinatesType } from '@/types/Map'

class MapService {
  baseUrl: string
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private getAuthHeader() {
    const token = localStorage.getItem('token')
    if (!token) {
      throw new Error('Authentication required')
    }
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    }
  }

  private async handleRequest<T>(request: () => Promise<T>): Promise<T> {
    try {
      return await request()
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          // Handle unauthorized error - you might want to redirect to login
          localStorage.removeItem('token')
          window.location.href = '/login'
        }
        throw new Error(error.response?.data?.message || 'An error occurred')
      }
      throw error
    }
  }

  async getMarkers(): Promise<ObjectCoordinatesType[]> {
    return this.handleRequest(async () => {
      const { data } = await axios.get(`${this.baseUrl}/api/v1/building/coordinates/`, {
        headers: this.getAuthHeader()
      })
      return data
    })
  }

  async getMarkersId(id: number): Promise<ObjectCoordinatesType[]> {
    return this.handleRequest(async () => {
      const { data } = await axios.get(`${this.baseUrl}/api/v1/building/coordinates/${id}/`, {
        headers: this.getAuthHeader()
      })
      return data
    })
  }

  async getMarkersByBuildingId(buildingId: number): Promise<ObjectCoordinatesType[]> {
    return this.handleRequest(async () => {
      const { data } = await axios.get(`${this.baseUrl}/api/v1/building/coordinates/`, {
        headers: this.getAuthHeader()
      })
      return data.filter((marker: ObjectCoordinatesType) => Number(marker.building.id) === buildingId)
    })
  }
}

export const mapService = new MapService(import.meta.env.VITE_BACKEND_URL)
