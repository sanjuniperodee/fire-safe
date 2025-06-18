export type Provider = {
  id: number
  first_name: string
  last_name: string
  middle_name: string
  email: string
  phone: string
  organization_name: string
  main_organization_type: MainOrganizationTypes
  organization_type: OrganizationTypes
  organization_sub_type: string
  company_name: string
  bin_field: string
  actual_residence_address: string
  residence_address: string
  categories: Category[]
  role: []
}

export type AllProvider = {
  id: number
  first_name: string
  last_name: string
  middle_name: string
  email: string
  phone: string
  main_organization_type: MainOrganizationTypes
  bin_field: string
  categories: Category[]
  avator_url: string
  company_name: string
}

export interface Category {
  id: number
  name: string
  measurement_unit?: string
}

export type ProviderValidator = {
  first_name: string
  last_name: string
  middle_name: string
  email: string
  phone: string
  organization_name: string
  main_organization_type: MainOrganizationTypes
  organization_type: OrganizationTypes
  organization_sub_type: string
  bin_field: string
  categories: number[]
}

export type UpdateProvider = {
  id: number
  first_name: string
  last_name: string
  middle_name: string
  email: string
  phone: string
  organization_name: string
  main_organization_type: MainOrganizationTypes
  organization_type: OrganizationTypes
  organization_sub_type: string
  bin_field: string
  categories: number[]
}

export type MainOrganizationTypes = 'Commercial Organizations' | 'NonCommercial Organizations'

export type MainOrganizationTypesLocal = 'Коммерческие организации' | 'Некоммерческие организации'

export type OrganizationTypes = 'State-owned enterprises(Commercial)' | 'Business partnerships(Commercial)' | 'Joint stock company(Commercial)' | 'Production cooperative(Commercial)' | 'Institutions(NonCommercial)' | 'Public Association(NonCommercial)' | 'Joint stock company(NonCommercial)' | 'Consumer Cooperative(NonCommercial)' | 'Fund(NonCommercial)' | 'Religious associations(NonCommercial)' | 'Associations of individual entrepreneurs and (or) legal entities in the form of an association (union)(NonCommercial)' | 'Other forms provided for by law(NonCommercial)';




