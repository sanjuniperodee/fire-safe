import { ref } from 'vue'

export const fullNameRules = ref([
  (v: any) => !!v || 'ФИО обязательно',
  (v: any) => v.split(' ').length >= 2 || 'Введите ФИО полностью (Фамилия Имя)'
])

export const roleRules = ref([(v: any) => !!v || 'Роль пользователя обязателена'])
export const IINRules = ref([
  (v: any) => !!v || 'ИИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
])

export const phoneRules = ref([
  (v: any) => !!v || 'Номер телефона обязателен',
  (v: any) => {
    const phoneNumberPattern = /^\+77\d{9}$/ // Match the pattern for +77 followed by 9 digits
    return v.match(phoneNumberPattern) ? true : 'Некорректный формат телефона (+77...)'
  }
])

export const emailRules = ref([
  (v: any) => !!v || 'Почта обязателена',
  (v: any) => {
    const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
    return v.match(emailPattern) ? true : 'Некорректный формат почты'
  }
])

export const passwordRules = ref([
  (v: any) => !!v || 'Пароль обязателен',
  (v: any) => (v && v.length >= 8) || 'Пароль должен быть более чем 8 символов',
  (v: any) => (v && v.length <= 20) || 'Пароль должен быть менее чем 20 символов'
])
