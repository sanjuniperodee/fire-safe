import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './UserStore'
import type { User } from '@/types/User'
import { profileItems as items } from '@/utils/LongFormsStorage'
import type { OrganizationTypes, MainOrganizationTypes } from '@/types/Provider'

export const useProfileStore = defineStore('profileStore', () => {
  const userStore = useUserStore()

  const values = ref({
    first_name: '',
    last_name: '',
    middle_name: '',
    iin: '',
    email: '',
    phone: '',
    birthdate: new Date(),
    about_myself: '',
    actual_residence_address: '',
    residence_address: '',
    // for inspector
    rank: '',
    position: '',
    certificate_number: '',
    inspector_jurisdiction_city: '',
    inspector_jurisdiction_district: '',
    // for provider
    main_organization_type: '' as MainOrganizationTypes,
    organization_type: '' as OrganizationTypes,
    organization_sub_type: '',
    organization_name: '',
    bin_field: '',
    categories: [] as number[]
  })

  function fillItemsValues(user: User): void {
    const {
      first_name,
      last_name,
      middle_name,
      iin,
      email,
      phone,
      birthdate,
      about_myself,
      actual_residence_address,
      residence_address,
      // for inspector
      rank,
      position,
      certificate_number,
      inspector_jurisdiction_city,
      inspector_jurisdiction_district,
      // for provider
      main_organization_type,
      organization_type,
      organization_sub_type,
      organization_name,
      bin_field,
      categories,
    } = user
    items.value.first_name.value = first_name
    items.value.last_name.value = last_name
    items.value.middle_name.value = middle_name
    items.value.iin.value = iin
    items.value.email.value = email
    items.value.phone.value = phone
    items.value.birthdate.value = new Date(birthdate)
    items.value.about_myself.value = about_myself
    items.value.actual_residence_address.value = actual_residence_address!
    items.value.residence_address.value = residence_address!
    // for inspector
    items.value.rank.value = rank!
    items.value.position.value = position!
    items.value.certificate_number.value = certificate_number!
    items.value.inspector_jurisdiction_city.value = inspector_jurisdiction_city!
    items.value.inspector_jurisdiction_district.value = inspector_jurisdiction_district!
    // for provider
    items.value.main_organization_type.value = main_organization_type!
    items.value.organization_type.value = organization_type!
    items.value.organization_sub_type.value = organization_sub_type!
    items.value.organization_name.value = organization_name!
    items.value.bin_field.value = bin_field!
    items.value.categories.value = categories!

    values.value.first_name = first_name
    values.value.last_name = last_name
    values.value.middle_name = middle_name
    values.value.iin = iin
    values.value.email = email
    values.value.phone = phone
    values.value.birthdate = new Date(birthdate)
    values.value.about_myself = about_myself
    values.value.actual_residence_address = actual_residence_address!
    values.value.residence_address = residence_address!
    // for inspector
    values.value.rank = rank!
    values.value.position = position!
    values.value.certificate_number = certificate_number!
    values.value.inspector_jurisdiction_city = inspector_jurisdiction_city!
    values.value.inspector_jurisdiction_district = inspector_jurisdiction_district!
    // for provider
    values.value.organization_type = organization_type!
    values.value.organization_name = organization_name!
    values.value.bin_field = bin_field!
    values.value.categories = categories!
  }

  const editField = (key: keyof typeof items.value) => {
    items.value[key].isEditing = true
    if (key === 'birthdate') {
      values.value.birthdate = items.value.birthdate.value
      return
    } else if (key === 'categories'){
      values.value.categories = items.value.categories.value
      return
    }else if (key === 'main_organization_type'){
      values.value.main_organization_type = items.value.main_organization_type.value
      return
    } else if (key === 'organization_type'){
      values.value.organization_type = items.value.organization_type.value
      return
    }else if (key === 'organization_sub_type'){
      values.value.organization_sub_type = items.value.organization_sub_type.value
      return
    }else if (key === 'rank'){
      userStore.user!.rank = items.value.rank.value
      return
    }else if (key === 'position'){
      userStore.user!.position = items.value.position.value
      return
    } else if (key === 'inspector_jurisdiction_city'){
      userStore.user!.inspector_jurisdiction_city = items.value.inspector_jurisdiction_city.value
      return
    }else if (key === 'inspector_jurisdiction_district'){
      userStore.user!.inspector_jurisdiction_district = items.value.inspector_jurisdiction_district.value
      return
    }
    values.value[key] = items.value[key].value
  }

  const cancelEditing = (key: keyof typeof items.value) => {
    items.value[key].isEditing = false
    items.value[key].value = values.value[key]
  }

  const updateFieldValue = async (key: keyof typeof items.value) => {
    items.value[key].isEditing = false
    if (key === 'birthdate') {
      userStore.user!.birthdate = items.value.birthdate.value.toISOString().split('T')[0]
      return
    } else if (key === 'categories'){
      userStore.user!.categories = items.value.categories.value
      return
    }else if (key === 'main_organization_type'){
      userStore.user!.main_organization_type = items.value.main_organization_type.value
      return
    } else if (key === 'organization_type'){
      userStore.user!.organization_type = items.value.organization_type.value
      return
    }else if (key === 'organization_sub_type'){
      userStore.user!.organization_sub_type = items.value.organization_sub_type.value
      return
    }else if (key === 'rank'){
      userStore.user!.rank = items.value.rank.value
      return
    }else if (key === 'position'){
      userStore.user!.position = items.value.position.value
      return
    }else if (key === 'inspector_jurisdiction_city'){
      userStore.user!.inspector_jurisdiction_city = items.value.inspector_jurisdiction_city.value
      return
    }else if (key === 'inspector_jurisdiction_district'){
      userStore.user!.inspector_jurisdiction_district = items.value.inspector_jurisdiction_district.value
      return
    }
    userStore.user![key] = items.value[key].value
  }

  return {
    items,
    editField,
    cancelEditing,
    updateFieldValue,
    fillItemsValues
  }
})