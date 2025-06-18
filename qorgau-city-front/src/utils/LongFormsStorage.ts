import { ref } from 'vue'
import { fireResistanceRating, functionalPoClass, externalWallsMaterials, innerWallsMaterials, roofTypes, stairsMaterials, stairsTypes, stairsСlassification, lightingOptionsItem, ventilationOptions, heatingOptionsRussian, securityOptionsRussian } from './subBuildingOptions'
import { categories } from '@/utils/categoryList'
import type { OrganizationTypes, MainOrganizationTypes, MainOrganizationTypesLocal } from '@/types/Provider'
import type { position, rank, rankRussian, positionRussian } from '@/types/User'
import {type OrganizationTypeObject, type OrgananizationSubTypeLocal, SubbuildingMaintypes, type OrganizationCharacteristics} from '@/types/ObjectBuilding'
import type { RefSymbol } from '@vue/reactivity'

export type subBuildingInfoItem = {
  key: string
  title: string
  value: string | number | Date | []
  type: 'text' | 'number' | 'select' | 'list' | 'metrics' | 'date' | 'image'
  rules?: ((v: any) => boolean | string)[]
  items?: FunctionalPO[] | string[]
  selectedValue?: string | null
  metricType?: string
}

export type FunctionalPO = {
  title: string
  items: string[]
  selectedValue?: any
}

export const profileItems = ref({
  first_name: {
    name: 'Имя',
    isEditing: false,
    value: '',
    key: 'first_name',
    rules: [(v: any) => !!v || 'Имя обязателено']
  },
  last_name: {
    name: 'Фамилия',
    isEditing: false,
    value: '',
    key: 'last_name',
    rules: [(v: any) => !!v || 'Фамилия обязателено']
  },
  middle_name: {
    name: 'Отчество',
    isEditing: false,
    value: '',
    key: 'middle_name',
    rules: [(v: any) => !!v || 'Отчество обязателено']
  },
  iin: {
    name: 'ИИН',
    isEditing: false,
    value: '',
    key: 'iin',
    rules: [
      (v: any) => !!v || 'ИИН обязателен',
      (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
      (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
    ]
  },
  email: {
    name: 'Email',
    isEditing: false,
    value: '',
    key: 'email',
    rules: [
      (v: any) => !!v || 'Почта обязательна',
      (v: any) => {
        const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
        return v.match(emailPattern) ? true : 'Некорректный формат почты'
      }
    ]
  },
  phone: {
    name: 'Номер телефона',
    isEditing: false,
    value: '',
    key: 'phone',
    rules: [
      (v: any) => !!v || 'Номер телефона обязателен',
      (v: any) => {
        const phoneNumberPattern = /^\+77\d{9}$/ // Match the pattern for +77 followed by 9 digits
        return v.match(phoneNumberPattern) ? true : 'Некорректный формат телефона (+77...)'
      }
    ]
  },
  birthdate: {
    name: 'Дата рождения',
    isEditing: false,
    value: new Date(),
    key: 'birthdate',
    rules: []
  },
  about_myself: {
    name: 'О себе',
    isEditing: false,
    value: '',
    key: 'about_myself',
    rules: [(v: any) => (v && v.length <= 255) || 'Максимальная длина — 255 символов']
  },
  actual_residence_address: {
    name: 'Фактический адрес проживания',
    isEditing: false,
    value: '',
    key: 'actual_residence_address',
    rules: []
  },
  residence_address: {
    name: 'Адрес проживания',
    isEditing: false,
    value: '',
    key: 'residence_address',
    rules: []
  },
  // FOR INSPECTOR
  rank: {
    name: 'Звание',
    isEditing: false,
    value: '' as rank,
    key: 'rank',
    rules: [(v: any) => !!v || 'Звание обязательно']
  },
  position: {
    name: 'Должность',
    isEditing: false,
    value: '' as position,
    key: 'position',
    rules: [(v: any) => !!v || 'Должность обязательно']
  },
  certificate_number: {
    name: 'Номер удостоверение',
    isEditing: false,
    value: '',
    key: 'certificate_number',
    rules: [
      (v: any) => !!v || 'Номер удостоверение обязательно',
      (v: any) => parseInt(v.length) === 5 || 'Длина удостоверение должна быть 5 цифр'
    ]
  },
  inspector_jurisdiction_city: {
    name: 'Город юрисдикции инспектора:',
    isEditing: false,
    value: '',
    key: 'inspector_jurisdiction_city',
    rules: []
  },
  inspector_jurisdiction_district: {
    name: 'Район юрисдикции инспектора:',
    isEditing: false,
    value: '',
    key: 'inspector_jurisdiction_district',
    rules: []
  },
  // FOR PROVIDER
  main_organization_type: {
    name: 'Главный тип организации',
    isEditing: false,
    value: '' as MainOrganizationTypes,
    key: 'main_organization_type',
    rules: [
      (v: any) => !!v || 'Главный тип организации обязателен'
    ]
  },
  organization_type: {
    name: 'Тип организации',
    isEditing: false,
    value: '' as OrganizationTypes,
    key: 'organization_type',
    rules: [
      (v: any) => !!v || 'Тип организации обязателен'
    ]
  },
  organization_sub_type: {
    name: 'Под Тип Организации',
    isEditing: false,
    value: '' ,
    key: 'organization_sub_type',
    rules: [
      (v: any) => !!v || 'Под Тип Организации обязателен'
    ]
  },
  organization_name: {
    name: 'Название организации',
    isEditing: false,
    value: '',
    key: 'organization_name',
    rules: [
      (v: any) => !!v || 'Название организации обязательно'
    ]
  },
  bin_field: {
    name: 'БИН',
    isEditing: false,
    value: '',
    key: 'bin_field',
    rules: [
      (v: any) => !!v || 'БИН обязателен',
      (v: any) => v.length === 12 || 'Длина БИН должна быть 12 цифр'
    ]
  },
  categories: {
    name: 'Категории',
    isEditing: false,
    value: [] as number[],
    options: categories,
    key: 'categories',
    rules: [
      (v: any[]) => v.length > 0 || 'Необходимо выбрать хотя бы одну категорию'
    ]
  }
})

export const generalObjectInfo = ref([
  {
    key: 'organization_name',
    title: 'Наименования организации',
    isEditing: false,
    value: '',
    type: 'text',
    rules: [(v: any) => !!v || 'Наименования организации обязательно']
  },
  {
    key: 'organization_type',
    title: 'Главный Тип организации:',
    isEditing: false,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Тип организации обязательно']
  },
  {
    key: 'organization_optional_type',
    title: 'Тип организации:',
    isEditing: false,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Тип организации обязательно']
  },
  {
    key: 'organization_sub_type',
    title: 'Под тип организации:',
    isEditing: false,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Тип организации обязательно']
  },
  {
    key: 'organization_characteristics',
    title: 'Характеристики организации:',
    isEditing: false,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Тип организации обязательно']
  },
  {
    key: 'iin',
    title: 'БИН / ИИН',
    value: '',
    isEditing: false,
    type: 'text',
    rules: [
      (v: any) => !!v || 'ИИН обязателен',
      (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
      (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
    ]
  },
  {
    key: 'owner',
    title: 'Собственник объекта защиты',
    isEditing: false,
    value: '',
    type: 'text',
    rules: [
      (v: any) => !!v || 'ФИО обязательно',
      (v: any) =>
        v.split(' ').filter(Boolean).length === 3 || 'Должно быть и фамилия и имя и отчество'
    ]
  },
  {
    key: 'address',
    title: 'Адрес местонахождения',
    isEditing: false,
    value: '',
    type: 'text',
    rules: [(v: any) => !!v || 'Адрес местонахождения обязательна']
  }
])

export const subBuildingInfo = ref<subBuildingInfoItem[]>([
  {
    key: 'subbuilding_type',
    title: 'Объект организации',
    items: Object.keys(SubbuildingMaintypes.value),
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Объект организации обязателен']
  },
  {
    key: 'subbuilding_subtype',
    title: 'Под тип здания',
    items: [],
    value: '',
    type: 'select',
    rules: []
  },
  {
    key: 'subbuilding_optional_subtype_type',
    title: 'Дополнительный тип подздания',
    items: [],
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Объект организации обязателен']
  },
  {
    key: 'subbuilding_characteristics',
    title: 'Характеристика подздания',
    items: [],
    value: '',
    type: 'select',
    rules: []
  },
  {
    key: 'title',
    title: 'Название',
    value: '',
    type: 'text',
    rules: [(v: any) => !!v || 'Название обязательно']
  },
  {
    key: 'functional_purpose',
    title: 'Предназначение',
    value: '',
    type: 'text',
    rules: [(v: any) => !!v || 'Предназначение обязательно']
  },
  {
    key: 'floor_number',
    title: 'Этаж',
    value: 0,
    type: 'number',
    rules: [
      (v: any) => !!v || 'Этаж обязательна',
      (v: any) => !isNaN(Number(v)) || 'Этаж должен быть числом'
    ]
  },
  {
    key: 'total_floors',
    title: 'Всего этажей',
    value: 0,
    type: 'number',
    rules: [
      (v: any) => !!v || 'Этажность обязательна',
      (v: any) => !isNaN(Number(v)) || 'Этажность должна быть числом'
    ]
  },
  {
    key: 'building_foundation',
    title: 'Дата постройки',
    value: new Date(),
    type: 'date'
  },
  {
    key: 'external_walls_material',
    title: 'Материал наружных стен',
    items: externalWallsMaterials,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Материал наружных стен обязательна'],
  },
  {
    key: 'inner_walls_material',
    title: 'Внутренние стены и перегородки',
    items: innerWallsMaterials,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Внутренние стены и перегородки обязательна']
  },
  {
    key: 'roof',
    title: 'Тип кровли',
    items: roofTypes,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Кровля обязательна']
  },
  {
    key: 'stairs_material',
    title: 'Материал лестницы',
    items: stairsMaterials,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Лестницы обязательна']
  },
  {
    key: 'stairs_type',
    title: 'Тип лестницы',
    items: stairsTypes,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Лестницы обязательна']
  },
  {
    key: 'stairs_classification',
    title: 'Классификация лестницы',
    items: stairsСlassification,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Лестницы обязательна']
  },
  {
    key: 'building_height',
    title: 'Высота здания',
    value: 0,
    metricType: 'м',
    type: 'metrics',
    rules: [
      (v: any) => !!v || 'Высота здания обязательна',
      (v: any) => !isNaN(Number(v)) || 'Высота здания должна быть числом'
    ]
  },
  {
    key: 'area',
    title: 'Площадь',
    value: 0,
    metricType: 'м²',
    type: 'metrics',
    rules: [
      (v: any) => !!v || 'Площадь обязательна',
      (v: any) => !isNaN(Number(v)) || 'Площадь должна быть числом'
    ]
  },
  {
    key: 'volume',
    title: 'Объем',
    value: 0,
    metricType: 'м³',
    type: 'metrics',
    rules: [
      (v: any) => !!v || 'Объем обязателен',
      (v: any) => !isNaN(Number(v)) || 'Объем должен быть числом'
    ]
  },
  {
    key: 'lighting',
    title: 'Освещение',
    items: lightingOptionsItem,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Это поле обязательно']
  },
  {
    key: 'ventilation',
    title: 'Вентиляция',
    items: ventilationOptions,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Это поле обязательно']
  },
  {
    key: 'heating',
    title: 'Отопление',
    items: heatingOptionsRussian,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Это поле обязательно']
  },
  {
    key: 'security',
    title: 'Объект охраняется',
    items: securityOptionsRussian,
    value: '',
    type: 'select',
    rules: [(v: any) => !!v || 'Это поле обязательно']
  },
  {
    key: 'year_construction_reconstruction',
    title: 'Год реконструкции',
    value: 0,
    type: 'metrics',
    metricType: 'год',
    rules: [(v: any) => !!v || 'Год постройки, реконструкции обязателен']
  },
  {
    key: 'date_commissioning',
    title: 'Дата ввода в эксплуатацию',
    value: new Date(),
    type: 'date'
  },
  {
    key: 'fire_resistance_rating',
    title: 'Степень огнестойкости',
    value: '',
    items: fireResistanceRating,
    type: 'select',
    rules: [ 
      (v: string) => !!v.trim() || 'Степень огнестойкости обязательна',
      (v: string) => v.trim().length <= 500 || 'Значение слишком длинное'
    ]
  },
  {
    key: 'structural_po_class',
    title: 'Класс конструктивной ПО',
    value: '',
    items: ['C1', 'C2', 'C3', 'C4'],
    type: 'select',
    rules: [(v: any) => !!v || 'Класс конструктивной ПО обязателен']
  },
  {
    key: 'functional_po_class',
    title: 'Класс функциональной ПО',
    value: '',
    type: 'list',
    items: functionalPoClass,
    rules: [(v: any) => !!v || 'Класс функциональной ПО обязателен']
  },
  {
    key: 'change_functional_purpose_date',
    title: 'Изменение функционального назначения',
    value: new Date(),
    type: 'date'
  },
  // {
  //   key: 'images',
  //   title: 'Фото подздания',
  //   value: [],
  //   type: 'image',
  // }
])

