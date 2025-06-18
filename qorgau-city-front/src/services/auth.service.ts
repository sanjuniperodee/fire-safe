import type { User } from '@/types/User'
import axios from 'axios'
import type {
  LoginValidator,
  RegisterValidator,
  ChangePasswordValidator,
  SendSmsCodePayload,
  VerifySmsCodePayload,
  ForgotPasswordPayload
} from '@/types/Auth'

class AuthService {
  baseUrl: string
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async login(body: LoginValidator): Promise<string> {
    const { data } = await axios.post(`${this.baseUrl}/api/v1/login/`, body, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    localStorage.setItem('token', data.access)
    return 'Авторизация прошла успешно.'
  }

  async register(body: RegisterValidator) {
    try {
      const response = await axios.post(`${this.baseUrl}/api/v1/register/`, body, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error: any) {
      if (error.response) {
        console.error('Ошибка регистрации:', error.response.data);
        throw new Error(JSON.stringify(error.response.data)); // Throw the error so it can be caught in `submitForm`
      } else {
        console.error('Ошибка сети или сервера:', error.message);
        throw new Error('Ошибка сети или сервера.');
      }
    }
  }

  async logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('chat_token')
  }

  async changePassword(body: ChangePasswordValidator): Promise<string> {
    const token = localStorage.getItem('token')!
    await axios.post(`${this.baseUrl}/api/v1/users/reset-password`, body, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
      }
    })
    return 'Пароль успешно изменен.'
  }

  async activateUser(query: string): Promise<string> {
    const resultQuery = `${this.baseUrl}/api/v1/users/activate?${query}`
    await axios.get(resultQuery, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    return 'Мы успешно активировали ваш аккаунт. Просим войти в нашу систему.'
  }

  async getUser(): Promise<User> {
    const token = localStorage.getItem('token')!
    const { data } = await axios.get(`${this.baseUrl}/api/v1/user/me/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token
      }
    })

    return data
  }

  async sendSmsCode(body: SendSmsCodePayload): Promise<string> {
    await axios.post(`${this.baseUrl}/api/v1/users/send-sms-code`, body, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return 'SMS код был отправлен на ваш номер.'
  }

  async verifySmsCode(body: VerifySmsCodePayload): Promise<string> {
    await axios.post(`${this.baseUrl}/api/v1/users/verify-sms-code`, body, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return 'SMS код был подтвержден. Введите пароль.'
  }

  async forgotPassword(body: ForgotPasswordPayload): Promise<string> {
    await axios.post(`${this.baseUrl}/api/v1/users/forgot-password`, body, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return 'Пароль успешно изменен. Переводим вас на страницу авторизации.'
  }

  async resendCode(phone: string): Promise<string> {
    await axios.get(`${this.baseUrl}/api/v1/users/resend-activate?phone=${phone}`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return 'Мы отправили код на ваш номер телефона.'
  }
}

export const authService = new AuthService(import.meta.env.VITE_BACKEND_URL)
