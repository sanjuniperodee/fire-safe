import axios from 'axios'
import type { CreateComplaint, Complaint } from '@/types/Complaint'


class ComplaintService {
  baseUrl: string
  token = localStorage.getItem('token')
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async createComplaint(body: CreateComplaint) {
    await axios.post(`${this.baseUrl}/api/v1/complaint/`, body, {
      headers: {
        Authorization: 'Bearer ' + this.token
      }
    })
  }

  async getComplaints(status: string): Promise<Complaint[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/complaint/?status=${status}`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })

    return data.results
  }

  async getComplaintsById(id: number) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/complaint/${id}/`, {
      headers: {
        Authorization: `Bearer ${this.token}`
      }
    });
    return data;
  }

  async removeComplaint(id: number) {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/complaint/${id}/`, {
      headers: {
        Authorization: `Bearer ${this.token}`
      }
    });
    return data;
  }
  async createMarkAsAnswered(id: number | null) {
    try {
      await axios.post(
        `${this.baseUrl}/api/v1/complaint/${id}/mark_as_answered/`, 
        {}, // пустой объект данных, если нет тела запроса
        {
          headers: {         
            Authorization: `Bearer ${this.token}`       
          }
        }
      )
    } catch (error) {
      console.error('Ошибка приmarks as answered:', error)
      // Обработка ошибки
    }
  }

  async updateChangeStatementStatus(id: number | null, status: string) {
    try {
      await axios.patch(
        `${this.baseUrl}/api/v1/statements/${id}/change_statement_provider_status/`, 
        { status },
        {
          headers: {
            Authorization: `Bearer ${this.token}`,
            'Content-Type': 'multipart/form-data'
          },
        }
      );
    } catch (error) {
      console.error('Ошибка обновления статуса:', error);
    }
}
  
}

export const complaintService = new ComplaintService(import.meta.env.VITE_BACKEND_URL)
