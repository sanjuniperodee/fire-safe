import axios from 'axios'
import { type Statement } from '@/types/Statement'

class StatementService {
  baseUrl: string
  token = localStorage.getItem('token')
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async createStatement(formData: FormData) {
    await axios.post(`${this.baseUrl}/api/v1/statements/`, formData, {
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  async getAllStatements( limit: number, offset: number ) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/`, {
      params: { limit, offset },
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getAllStatementsFiltered (
    limit: number, offset: number,
    min_price: number, max_price: number,
    seen: boolean,
  ) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/`, {
      params: {
        limit,
        offset,
        min_price,
        max_price,
        seen
      },
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getStatementById(id: number): Promise<Statement> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/${id}`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async noteStatement(id: number) {
    const { data } = await axios.post(
      `${this.baseUrl}/api/v1/statements/response/call/${id}/`,
      {statement: id},
      {
        headers: {
          Authorization: 'Bearer ' + this.token,
          'Content-Type': 'application/json'
        }
      }
    )
    return data
  }

  async getSelectedStatements(limit: number, offset: number) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/response/selected/`, {
      params: {
        limit,
        offset
      },
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'application/json'
      }
    })
    return data
  }

  async getCalledStatements(limit: number, offset: number): Promise<Statement[]> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/response/called/`, {
      params: {
        limit,
        offset
      },
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'application/json'
      }
    })
    return data
  }

  async deleteCalledStatement(id: number): Promise<Statement> {
    const { data } = await axios.delete(
      `${this.baseUrl}/api/v1/statements/response/call/${id}`,
      {
        headers: {
          Authorization: 'Bearer ' + this.token,
          'Content-Type': 'application/json'
        }
      }
    )
    return data
  }

  async getMyStatements(limit: number, offset: number) {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/my_statements/`, {
      params: {
        limit,
        offset
      },
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async getMyStatementById(id: number): Promise<Statement> {
    const { data } = await axios.get(`${this.baseUrl}/api/v1/statements/my_statements/${id}`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.token
      }
    })
    return data
  }

  async editMyStatement(id: number, formData: FormData): Promise<Statement> {
    const { data } = await axios.patch(
      `${this.baseUrl}/api/v1/statements/my_statements/${id}/`,
      formData,
      {
        headers: {
          Authorization: 'Bearer ' + this.token,
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    return data
  }

  async deleteMyStatement(id: number) {
    const { data } = await axios.delete(`${this.baseUrl}/api/v1/statements/${id}`, {
      headers: {
        Authorization: 'Bearer ' + this.token,
        'Content-Type': 'multipart/form-data'
      }
    })

    return data
  }
}

export const statementService = new StatementService(import.meta.env.VITE_BACKEND_URL)
