export const rules = {
  required: (value: any) => !!value || 'Поле обязательно',
  isNumber: (value: any) => !isNaN(value) || 'Должно быть числом'
}
