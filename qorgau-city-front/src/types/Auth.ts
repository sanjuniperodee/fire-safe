import type { UserRoles } from '@/types/User'
import type { OrganizationTypes, MainOrganizationTypes } from '@/types/Provider'

export type LoginValidator = {
  phone: string
  password: string
}

export type SendSmsCodePayload = {
  phone: string
}

export type VerifySmsCodePayload = {
  phone: string
  code: string
}

export type RegisterValidator = {
  first_name: string
  middle_name: string
  last_name: string
  email: string
  birthdate: string
  iin: string
  actual_residence_address?: string
  residence_address?: string

  role: UserRoles
  // FOR PROVIDER
  organization_name?: string
  main_organization_type? : MainOrganizationTypes
  organization_type?: OrganizationTypes
  organization_sub_type?: string
  bin_field?: string
  categories?: number[]
  // FOR INSPECTOR
  rank?: string,
  position?: string,
  certificate_number?: string,

  phone: string
  password: string
  password2: string
}

export type ChangePasswordValidator = {
  phone: string
  new_password: string
  old_password: string
  confirm_password: string
}

export type ForgotPasswordPayload = {
  phone: string
  password: string
}
