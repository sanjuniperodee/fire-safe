export const formatBirthdate = (date: Date) => {
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear()

  return `${day < 10 ? '0' : ''}${day}.` + `${month < 10 ? '0' : ''}${month}.` + `${year} `
}

export const formatDate = (date: Date) => {
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear() % 100
  const hours = date.getHours()
  const minutes = date.getMinutes()
  const seconds = date.getSeconds()

  const formattedDate =
    `${day < 10 ? '0' : ''}${day}.` +
    `${month < 10 ? '0' : ''}${month}.` +
    `${year < 10 ? '0' : ''}${year} ` +
    `${hours}:${minutes}:${seconds}`

  return formattedDate
}

export const formatDateForChat = (inputDate: Date | string | null | undefined) => {
  if (inputDate == null) {
    return 'Дата недоступна'; // Возвращаем сообщение о недоступной дате
  }

  const date = typeof inputDate === 'string' ? new Date(inputDate) : inputDate;

  if (isNaN(date.getTime())) {
    throw new TypeError('Invalid date object');
  }

  const month = date.toLocaleString('ru-RU', { month: 'long' });
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes().toString().padStart(2, '0');

  return `${day} ${month}, ${hours}:${minutes}`;
}


export const formatStatementInfoDate = (date: string) => {
  const dateWrapper = new Date(date)

  const year = dateWrapper.getFullYear()
  const month = String(dateWrapper.getMonth() + 1).padStart(2, '0')
  const day = String(dateWrapper.getDate()).padStart(2, '0')
  const hours = String(dateWrapper.getHours()).padStart(2, '0')
  const minutes = String(dateWrapper.getMinutes()).padStart(2, '0')

  return `${year}-${month}-${day}(${hours}:${minutes})`
}

export const formatDateWithoutTime = (date: Date) => {
  const day = date.getDate()
  const month = date.getMonth() + 1
  const year = date.getFullYear() % 100

  const formattedDate =
    `${day < 10 ? '0' : ''}${day}.` +
    `${month < 10 ? '0' : ''}${month}.` +
    `${year < 10 ? '0' : ''}${year} `
  return formattedDate
}

export const formatDateForValidation = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}
