import axios from 'axios'
import { type Advertisement } from '@/types/Advertisements'

class AdvertisementService {
  baseUrl: string
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async createAdvertisements(body: Advertisement): Promise<Advertisement> {
    const token = localStorage.getItem('token')!
    const { data } = await axios.post(`${this.baseUrl}/api/v1/advertisements/`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
      }
    })

    return data
  }

  async getAdvertisements(): Promise<Advertisement[]> {
    const token = localStorage.getItem('token')!
    const { data } = await axios.get(`${this.baseUrl}/api/v1/advertisements/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
      }
    })
    return data.results
  }

  async getAdvertisementById(id: number): Promise<Advertisement[]> {
    const token = localStorage.getItem('token')!
    const { data } = await axios.get(`${this.baseUrl}/api/v1/advertisements/${id}`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
      }
    })
    return data.results
  }
}

export const advertisementService = new AdvertisementService(import.meta.env.VITE_BACKEND_URL)
