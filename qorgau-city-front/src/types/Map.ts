import type { ObjectBuilding } from './ObjectBuilding'

export type Coordinates = {
  lat: number
  lng: number
}

export type ObjectCoordinatesType = {
  id: number
  lat: number
  lng: number
  building: ObjectBuilding
}

export const ratingTypes = {
  Safe: 1,
  Normal: 2,
  Danger: 3
}

export const ratingDescriptionMap = {
  1: 'Безопасен',
  2: 'Средней безопасности',
  3: 'Не безопасен'
}

export const ratingPercentages = {
  1: 'больше 70%',
  2: 'больше 40%',
  3: 'меньше 40%'
}

export const ratingColors = {
  1: '#5b9271',
  2: '#f6c640',
  3: '#d20f0d'
}

export const getColor = (rating: string) => {
  switch (rating) {
    case '1':
      return '#5b9271'
    case '2':
      return '#f6c640'
    case '3':
      return '#d20f0d'
  }
}

export type MarkerType = Coordinates & ObjectBuilding
