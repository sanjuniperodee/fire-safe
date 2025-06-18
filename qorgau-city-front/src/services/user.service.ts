import type { User, UpdateUserValidator } from '@/types/User'
import { type Provider, type AllProvider, type UpdateProvider } from '@/types/Provider'
import axios from 'axios'

class UserService {
  baseUrl: string
  token = localStorage.getItem('token')
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async getUserById(userId: number): Promise<User> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/users/${userId}`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })

    return data
  }

  async getAllUser(): Promise<User[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/users/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })

    return data
  }

  async getAllInspProviders(): Promise<AllProvider[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/users/provider_list/`, {
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'application/json'
      }
      })

      return data.results
  }

  async getAllProviders(): Promise<Provider[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/providers/`, {
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'application/json'
      }
    })

    return data.results
  }

  async getProvider(userId: number): Promise<Provider> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/users/${userId}/provider_detail/`, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })

    return data
  }

  async updateUser(userId: number, body: Partial<UpdateUserValidator> | FormData): Promise<string> {
    await axios.patchForm(`${this.baseUrl}/api/v1/users/${userId}/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })

    return 'Пользователь был обновлен.'
  }

  async updateUserRole(body: Partial<UpdateUserValidator>): Promise<string> {
    await axios.patch(`${this.baseUrl}/api/v1/users/user_roles/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'application/json'
      }
    })

    return 'Пользователь был обновлен.'
  }

  async deleteUserRole(body: Partial<UpdateUserValidator>): Promise<string> {
    await axios.request({
      method: 'delete',
      url: `${this.baseUrl}/api/v1/users/user_roles/`,
      data: body,
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'application/json'
      }
    })

    return 'Пользователь был обновлен.'
  }

  async uploadAvatar(userId: number, formData: FormData): Promise<string> {
    const { data } = await axios.postForm(
      `${this.baseUrl}/api/v1/user/avatar/${userId}/upload/`,
      formData,
      {
        headers: {
          Authorization: 'Bearer ' + this.token
        }
      }
    )
    return data.avatar_url
  }
  async deleteAvatar(userId: number): Promise<string> {
    await axios.delete(`${this.baseUrl}/api/v1/user/avatar/${userId}/delete/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return 'Фото профиля было успешно удалено.'
  }
}

export const userService = new UserService(import.meta.env.VITE_BACKEND_URL)
