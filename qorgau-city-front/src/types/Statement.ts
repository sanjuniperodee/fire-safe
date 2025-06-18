export type Statement = {
  id: number
  categories: Category[]
  text: string
  service_time: string
  location: string
  min_price: number
  max_price: number
  is_active: boolean
  is_seen: boolean
  is_called: boolean
  uploaded_media: Media[]
}

export type StatementValidator = {
  categories: number[]
  text: string
  service_time: string
  location: string
  min_price: number
  max_price: number
  uploaded_media: Media[]
}

export interface Media {
  id?: number
  file: string
  file_type: string
  file_name?: string
}

export interface Category {
  id: number
  name: string
  measurement_unit?: string
}
