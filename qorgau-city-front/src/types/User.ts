import { computed } from 'vue'
import type { OrganizationTypes, MainOrganizationTypes } from '@/types/Provider'
import type { Education, Experience, Achievement, OtherAchievements } from '@/types/ProviderProfile'


export type User = {
  id: number
  first_name: string
  last_name: string
  middle_name: string
  role: UserRole[]
  iin: string
  email: string
  phone: string
  avatar_url: string
  birthdate: string // YYYY-MM-DD
  about_myself: string
  actual_residence_address?: string
  residence_address?: string
  // for inspector
  rank?: rank
  position?: position
  certificate_number?: string
  inspector_jurisdiction_city?: string
  inspector_jurisdiction_district?: string
  // for provider
  main_organization_type?: MainOrganizationTypes,
  organization_type?: OrganizationTypes,
  organization_sub_type?: string
  organization_name?: string,
  bin_field?: string,
  categories?: number[],
  // provider special infos
  education_info?: Education[],
  experience_info?: Experience[],
  achievement_info?: Achievement[],
  other_achievements_info?: OtherAchievements[],
}

export type Author = {
  id?: number
  email: string
  first_name: string
  iin: string
  last_name: string
  middle_name: string
  phone: string
}

export type UserRole = {
  role: UserRoles
  status: 'ACCEPTED' | 'NOT_ACCEPTED'
}

export type UserRoles = (typeof UserRoleOptions)[keyof typeof UserRoleOptions]

export type UpdateUserValidator = {
  id: number
  first_name: string
  last_name: string
  middle_name: string
  role: UserRoles
  iin: string
  email: string
  phone: string
  birthdate: string
  actual_residence_address?: string
  residence_address?: string
  // for inspector
  rank?: string
  position?: string
  certificate_number?: string
  inspector_jurisdiction_city?: string
  inspector_jurisdiction_district?: string
  // for provider
  main_organization_type?: MainOrganizationTypes,
  organization_type?: OrganizationTypes,
  organization_sub_type?: string
  organization_name?: string,
  bin_field?: string,
  categories?: number[],
}

export const RoleMap = {
  OBJECT_OWNER: 'Владелец объекта',
  PROVIDER: 'Поставщик',
  CITIZEN: 'Гражданин',
  INSPECTOR: 'Инспектор',
  ADMIN: 'Админ'
} as const

export const UserRoleOptions = {
  OBJECT_OWNER: 'OBJECT_OWNER',
  PROVIDER: 'PROVIDER',
  CITIZEN: 'CITIZEN',
  INSPECTOR: 'INSPECTOR',
  ADMIN: 'ADMIN'
}

export const roleMapReverse = Object.keys(RoleMap).reduce((res, key) => {
  res[RoleMap[key as keyof typeof RoleMap]] = UserRoleOptions[key as keyof typeof UserRoleOptions]
  return res
}, {} as Record<string, string>)

export const roleReverseToRussian = Object.keys(UserRoleOptions).reduce((res, key) => {
  res[UserRoleOptions[key as keyof typeof UserRoleOptions]] = RoleMap[key as keyof typeof RoleMap]
  return res
}, {} as Record<string, string>)

export const russianRoles = computed(() => Object.values(RoleMap))

export type roles = 'OBJECT_OWNER' | 'PROVIDER' | 'CITIZEN' | 'INSPECTOR' | 'ADMIN'

export type rolesRussian = 'Владелец объекта' | 'Поставщик' | 'Гражданин' | 'Инспектор' | 'Админ'

export const roleTypesMapping = {
  'OBJECT_OWNER': 'Владелец объекта',
  'PROVIDER': 'Поставщик',
  'CITIZEN': 'Гражданин',
  'INSPECTOR': 'Инспектор',
  'ADMIN': 'Админ',
}

export const reversedRoleTypesMapping = Object.fromEntries(
  Object.entries(roleTypesMapping).map(([key, value]) => [value, key])
);

//RANK

export const RankMap = {
  PrivateCivilProtection: 'Рядовой гражданской защиты',
  JuniorSergeantOfCivilProtection: 'Младший сержант гражданской защиты',
  CivilProtectionSergeant: 'Сержант гражданской защиты',
  SeniorSergeantOfCivilProtection: 'Старший сержант гражданской защиты',
  CivilProtectionForeman: 'Старшина гражданской защиты',
  SecondLieutenantOfCivilProtection: 'Младший лейтенант гражданской защиты',
  LieutenantOfCivilProtection: 'Лейтенант гражданской защиты',
  SeniorLieutenantOfCivilProtection: 'Старший лейтенант гражданской защиты',
  CaptainOfCivilProtection: 'Капитан гражданской защиты',
  MajorOfCivilProtection: 'Майор гражданской защиты',
  LieutenantColonelOfCivilProtection: 'Подполковник гражданской защиты',
  ColonelOfCivilProtection: 'Полковник гражданской защиты',
  MajorGeneralOfCivilProtection: 'Генерал-майор гражданской защиты',   
  LieutenantGeneralOfCivilProtection: 'Генерал-лейтенант гражданской защиты',
  ColonelGeneralOfCivilProtection: 'Генерал-полковник гражданской защиты',
} as const

export const UserRankOptions = {
  PrivateCivilProtection: 'PrivateCivilProtection',
  JuniorSergeantOfCivilProtection: 'JuniorSergeantOfCivilProtection',
  CivilProtectionSergeant: 'CivilProtectionSergeant',
  SeniorSergeantOfCivilProtection: 'SeniorSergeantOfCivilProtection',
  CivilProtectionForeman: 'CivilProtectionForeman',
  SecondLieutenantOfCivilProtection: 'SecondLieutenantOfCivilProtection',
  LieutenantOfCivilProtection: 'LieutenantOfCivilProtection',
  SeniorLieutenantOfCivilProtection: 'SeniorLieutenantOfCivilProtection',
  CaptainOfCivilProtection: 'CaptainOfCivilProtection',
  MajorOfCivilProtection: 'MajorOfCivilProtection',
  LieutenantColonelOfCivilProtection: 'LieutenantColonelOfCivilProtection',
  ColonelOfCivilProtection: 'ColonelOfCivilProtection',
  MajorGeneralOfCivilProtection: 'MajorGeneralOfCivilProtection',   
  LieutenantGeneralOfCivilProtection: 'LieutenantGeneralOfCivilProtection',
  ColonelGeneralOfCivilProtection: 'ColonelGeneralOfCivilProtection',
};

export const rankMapReverse = Object.keys(RankMap).reduce((res, key) => {
  res[RankMap[key as keyof typeof RankMap]] = UserRankOptions[key as keyof typeof UserRankOptions]
  return res
}, {} as Record<string, string>)

export const rankReverseToRussian = Object.keys(UserRankOptions).reduce((res, key) => {
  res[UserRankOptions[key as keyof typeof UserRankOptions]] = RankMap[key as keyof typeof RankMap]
  return res
}, {} as Record<string, string>)

export const russianRank = computed(() => Object.values(RankMap))

export type rank = 'Private civil protection' | 'Junior Sergeant of Civil Protection' | 'Civil Protection Sergeant' | 'Senior Sergeant of Civil Protection' | 'Civil Protection Foreman' | 'Second Lieutenant of Civil Protection' | 'Lieutenant of Civil Protection' | 'Senior Lieutenant of Civil Protection' | 'Captain of Civil Protection' | 'Major of Civil Protection' | 'Lieutenant Colonel of Civil Protection' | 'Colonel of Civil Protection' | 'Major General of Civil Protection' | 'Lieutenant General of Civil Protection' | 'Colonel-General of Civil Protection'

export type rankRussian = 'Рядовой гражданской защиты' | 'Младший сержант гражданской защиты' | 'Сержант гражданской защиты' | 'Старший сержант гражданской защиты' | 'Старшина гражданской защиты' | 'Младший лейтенант гражданской защиты' | 'Лейтенант гражданской защиты' | 'Старший лейтенант гражданской защиты' | 'Капитан гражданской защиты' | 'Майор гражданской защиты' | 'Подполковник гражданской защиты' | 'Полковник гражданской защиты' | 'Генерал-майор гражданской защиты' | 'Генерал-лейтенант гражданской защиты' | 'Генерал-полковник гражданской защиты'

export const rankTypesMapping = {
  'Private civil protection': 'Рядовой гражданской защиты',
  'Junior Sergeant of Civil Protection': 'Младший сержант гражданской защиты',
  'Civil Protection Sergeant': 'Сержант гражданской защиты',
  'Senior Sergeant of Civil Protection': 'Старший сержант гражданской защиты',
  'Civil Protection Foreman': 'Старшина гражданской защиты',
  'Second Lieutenant of Civil Protection': 'Младший лейтенант гражданской защиты',
  'Lieutenant of Civil Protection': 'Лейтенант гражданской защиты',
  'Senior Lieutenant of Civil Protection': 'Старший лейтенант гражданской защиты',
  'Captain of Civil Protection': 'Капитан гражданской защиты',
  'Major of Civil Protection': 'Майор гражданской защиты',
  'Lieutenant Colonel of Civil Protection': 'Подполковник гражданской защиты',
  'Colonel of Civil Protection': 'Полковник гражданской защиты',
  'Major General of Civil Protection': 'Генерал-майор гражданской защиты',   
  'Lieutenant General of Civil Protection': 'Генерал-лейтенант гражданской защиты',
   'Colonel-General of Civil Protection':  'Генерал-полковник гражданской защиты',
}

export const reversedRankTypesMapping = Object.fromEntries(
  Object.entries(rankTypesMapping).map(([key, value]) => [value, key])
);

//POSITION

export const PositionMap = {
  ChiefStateInspectorforFireControl: 'Главный государственный инспектор по пожарному контролю',
  ChiefInspectorofFireControl: 'Старший инспектор по пожарному контролю',
  FireControlInspector: 'Инспектор по пожарному контролю',
} as const

export const UserPositionOptions = {
  ChiefStateInspectorforFireControl: 'ChiefStateInspectorforFireControl',
  ChiefInspectorofFireControl: 'ChiefInspectorofFireControl',
  FireControlInspector: 'FireControlInspector',
}

export const positionMapReverse = Object.keys(PositionMap).reduce((res, key) => {
  res[PositionMap[key as keyof typeof PositionMap]] = UserPositionOptions[key as keyof typeof UserPositionOptions]
  return res
}, {} as Record<string, string>)

export const positionReverseToRussian = Object.keys(UserPositionOptions).reduce((res, key) => {
  res[UserPositionOptions[key as keyof typeof UserPositionOptions]] = PositionMap[key as keyof typeof PositionMap]
  return res
}, {} as Record<string, string>)

export const russianPosition = computed(() => Object.values(PositionMap))

export type position = 'Chief State Inspector for Fire Control' | 'Chief Inspector of Fire Control' | 'Fire Control Inspector'

export type positionRussian = 'Главный государственный инспектор по пожарному контролю' | 'Старший инспектор по пожарному контролю' | 'Инспектор по пожарному контролю'

export const positionTypesMapping = {
  'Chief State Inspector for Fire Control': 'Главный государственный инспектор по пожарному контролю',
  'Chief Inspector of Fire Control': 'Старший инспектор по пожарному контролю',
  'Fire Control Inspector': 'Инспектор по пожарному контролю',
}

export const reversedPositionTypesMapping = Object.fromEntries(
  Object.entries(positionTypesMapping).map(([key, value]) => [value, key])
);
