import axios from 'axios'
import type { Education, Experience, Achievement, OtherAchievements } from '@/types/ProviderProfile'

enum ProfileEndpoint {
  Education = 'education',
  Experience = 'experience',
  Achievement = 'achievement',
  OtherAchievement = 'other_achievement',
}

class ProviderProfileService {
  baseUrl: string
  token = localStorage.getItem('token')
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async createProfileInfo<T>(endpoint: string, formData: FormData): Promise<T> {
    const { data } = await axios.postForm(`${this.baseUrl}/api/v1/provider_profile/${endpoint}/`, formData, {
      headers: {
        Authorization: 'Bearer ' + this.token,
      }
    })

    return data
  }

  private async getProfileInfos<T>(endpoint: string): Promise<T> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/provider_profile/${endpoint}/`, {
      headers: {
        Authorization: 'Bearer ' + this.token,
      }
    })

    return data
  }

  private async getProfileInfoById<T>(endpoint: string, id: number): Promise<T> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/provider_profile/${endpoint}/${id}`, {
      headers: {
        Authorization: 'Bearer ' + this.token,
      }
    })

    return data
  }

  private async editProfileInfo<T>(endpoint: string, id: number, formData: FormData): Promise<T> {
    const { data } = await axios.patchForm(`${this.baseUrl}/api/v1/provider_profile/${endpoint}/${id}/`, formData, {
      headers: {
        Authorization: 'Bearer ' + this.token,
      }
    })

    return data
  }

  private async deleteProfileInfo(endpoint: string, id: number,) {
    await axios.delete(`${this.baseUrl}/api/v1/provider_profile/${endpoint}/${id}/`, {
      headers: {
        Authorization: 'Bearer ' + this.token,
      }
    })
  }

  // CREATE
  async createEducation(formData: FormData): Promise<Education> {
    return await this.createProfileInfo( ProfileEndpoint.Education, formData)
  }
  async createExperience(formData: FormData): Promise<Experience> {
    return await this.createProfileInfo(ProfileEndpoint.Experience, formData)
  }
  async createAchievement(formData: FormData): Promise<Achievement> {
    return await this.createProfileInfo(ProfileEndpoint.Achievement, formData)
  }
  async createOtherAchievements(formData: FormData): Promise<OtherAchievements> {
    return await this.createProfileInfo(ProfileEndpoint.OtherAchievement, formData)
  }
  // GET
  async getEducations(): Promise<Education[]> {
    return await this.getProfileInfos(ProfileEndpoint.Education)
  }
  async getExperiences(): Promise<Experience[]> {
    return await this.getProfileInfos(ProfileEndpoint.Experience)
  }
  async getAchievements(): Promise<Achievement[]> {
    return await this.getProfileInfos(ProfileEndpoint.Achievement)
  }
  async getOtherAchievements(): Promise<OtherAchievements[]> {
    return await this.getProfileInfos(ProfileEndpoint.OtherAchievement)
  }
  // GET BY ID
  async getEducation(id: number): Promise<Education> {
    return await this.getProfileInfoById(ProfileEndpoint.Education, id)
  }
  async getExperience(id: number): Promise<Experience> {
    return await this.getProfileInfoById(ProfileEndpoint.Experience, id)
  }
  async getAchievement(id: number): Promise<Achievement> {
    return await this.getProfileInfoById(ProfileEndpoint.Achievement, id)
  }
  async getOtherAchievement(id: number): Promise<OtherAchievements> {
    return await this.getProfileInfoById(ProfileEndpoint.OtherAchievement, id)
  }
  // EDITS
  async editEducation( id: number, formData: FormData): Promise<Education> {
    return await this.editProfileInfo(ProfileEndpoint.Education, id, formData)
  }
  async editExperience( id: number, formData: FormData): Promise<Experience> {
    return await this.editProfileInfo(ProfileEndpoint.Experience, id, formData)
  }
  async editAchievement( id: number, formData: FormData): Promise<Achievement> {
    return await this.editProfileInfo(ProfileEndpoint.Achievement, id, formData)
  }
  async editOtherAchievements( id: number, formData: FormData): Promise<OtherAchievements> {
    return await this.editProfileInfo(ProfileEndpoint.OtherAchievement, id, formData)
  }
  // DELETE
  async deleteEducation(id: number) {
    await this.deleteProfileInfo(ProfileEndpoint.Education, id)
  }
  async deleteExperience(id: number) {
    await this.deleteProfileInfo(ProfileEndpoint.Experience, id)
  }
  async deleteAchievement(id: number) {
    await this.deleteProfileInfo(ProfileEndpoint.Achievement, id)
  }
  async deleteOtherAchievements(id: number) {
    await this.deleteProfileInfo(ProfileEndpoint.OtherAchievement, id)
  }
}

export const providerProfile = new ProviderProfileService(import.meta.env.VITE_BACKEND_URL)
