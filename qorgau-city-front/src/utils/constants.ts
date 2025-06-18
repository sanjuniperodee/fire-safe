// FOR PAGINATION
export const itemsPerPage = 10
export const getTotalPages = (count: number) => {
  return Math.ceil(count / itemsPerPage)
}

//OBJECT RATING
import type { RatingOption } from '@/types/ObjectBuilding'

export const calculateRating = (progress: number) => {
  if (progress >= 70) {
    return '1'
  } else if (progress >= 40) {
    return '2'
  } else {
    return '3'
  }
}

export function getMarkerIcon(rating: RatingOption) {
  return `/marks/rating-${rating}.png`
}

export function getMarkerTitle(rating: RatingOption) {
  switch (rating) {
    case '1':
      return 'Safe'
    case '2':
      return 'Normal'
    case '3':
      return 'Danger'
  }
}