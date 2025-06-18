import axios from 'axios'

class FileService {
  baseUrl: string
  token = localStorage.getItem('token')

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async uploadFile(formData: FormData): Promise<void> {
    await axios.post(`${this.baseUrl}/api/v1/document/upload/file/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: 'Bearer ' + this.token
      }
    })
  }

  async deleteFile(fileId: number): Promise<void> {
    await axios.delete(`${this.baseUrl}/api/v1/document/${fileId}/delete/file/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
  }

  async downloadFile(fileId: number): Promise<string> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/document/${fileId}/download/file/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    const byteCharacters = atob(data) // Assuming base64Data contains the base64 prefix (data:image/png;base64,)
    const byteArrays = []

    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512)
      const byteNumbers = new Array(slice.length)
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      byteArrays.push(byteArray)
    }

    const blob = new Blob(byteArrays, { type: 'application/octet-stream' })
    return URL.createObjectURL(blob)
  }
}

export const fileService = new FileService(import.meta.env.VITE_BACKEND_URL)
