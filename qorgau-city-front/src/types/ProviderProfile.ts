export type Education = {
  id?: number,
  college_name: string,
  degree: DegreeOptions,
  year_start: number,
  year_end: number,
  media: File,
  show_photo_to_clients: boolean,
  performing_now: boolean
};

export type Experience = {
  id?: number,
  company_name:string,
  year_start: number,
  year_end: number,
  media: File,
  performing_now: boolean
};

export type Achievement = {
  id?: number,
  certificate_name: string,
  year_received: number,
  media: File,
  show_photo_to_clients: boolean
};

export type OtherAchievements = {
  id?: number,
  name:string,
  year_start: number,
  year_end: number,
  media: File,
  show_photo_to_clients: boolean,
  performing_now: boolean
};

export type DegreeOptions = 'Bachelor' | 'Masters' | 'Other' | 'Unspecified'
export type DegreeOptionsRussian = 'Бакалавр' | 'Магистр' | 'Другое' | 'Не указан'

export const DegreeOptionsMapping: { [key in DegreeOptionsRussian]: DegreeOptions } = {
  'Бакалавр': 'Bachelor',
  'Магистр': 'Masters',
  'Другое': 'Other',
  'Не указан': 'Unspecified',
}

export const DegreeOptionsReverseMapping: { [key in DegreeOptions]: DegreeOptionsRussian } = {
  'Bachelor': 'Бакалавр',
  'Masters': 'Магистр',
  'Other': 'Другое',
  'Unspecified': 'Не указан',
}

export const getEnglishDegreeOptions = (
  localDegree: DegreeOptionsRussian
): DegreeOptions => {
  return DegreeOptionsMapping[localDegree]
}

export const getLocalDegreeOptions = (
  englishDegree: DegreeOptions
): DegreeOptionsRussian => {
  return DegreeOptionsReverseMapping[englishDegree]
}