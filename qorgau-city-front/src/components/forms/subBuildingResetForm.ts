import { formatDateForValidation } from '@/helpers/formatTime'
import type { FunctionalPO } from '@utils/LongFormsStorage'

export const resetForm = (formState: any, selectedValues: any) => {
  formState.value = {
    organization_object: 'Здание',
    title: '',
    functional_purpose: '',
    floor_number: 0,
    total_floors: 0,
    building_foundation: formatDateForValidation(new Date()),
    external_walls_material: '',
    inner_walls_material: '',
    roof: '',
    stairs: '',
    building_height: 0,
    area: 0,
    volume: 0,
    lighting: '',
    ventilation: '',
    heating: '',
    security: '',
    year_construction_reconstruction: 0,
    date_commissioning: formatDateForValidation(new Date()),
    fire_resistance_rating: '',
    structural_po_class: '',
    functional_po_class: [] as FunctionalPO[],
    rating: '3',
    change_functional_purpose_date: formatDateForValidation(new Date())
  }
  selectedValues.value = {}
}
