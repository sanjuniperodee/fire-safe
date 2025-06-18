import {
  type ObjectCoordinatesType,
  ratingColors,
  ratingDescriptionMap,
  ratingPercentages,
  ratingTypes
} from '@/types/Map'
import { toggleHeatMode } from '@/hooks/useGoogleMaps'

export function getMarkerContent(body: ObjectCoordinatesType) {
  const { iin, address, organization_name, owner, rating } = body.building
  return `
  <div class="mark">
    <div class="mark__title">${address}</div>
    <div class="mark__field-row">
      <div class="mark__field">ИИН/БИН:</div>
      <div class="mark__value">${iin}</div>
    </div>
    <div class="mark__field-row">
      <div class="mark__field">Адрес:</div>
      <div class="mark__value">${address}</div>
    </div>
    <div class="mark__field-row">
      <div class="mark__field">Наименование организации:</div>
      <div class="mark__value">${organization_name}</div>
    </div>
    <div class="mark__field-row">
      <div class="mark__field">Собственник объекта:</div>
      <div class="mark__value">${owner?.first_name}  ${owner?.last_name}</div>
    </div>
    <div class="mark__field-row" style="color: ${ratingColors[rating]} !important; font-weight: 700">
      <div class="mark__field">Уровень опасности объекта:</div>
      <div class="mark__value" >${ratingDescriptionMap[rating]}</div>
    </div> 
    <div style="margin-top: 20px" class="mark__field">Почему этот объект имеет такой уровень опасности объекта?</div>
    <div style="margin-top: 8px" class="mark__value">Уровень опасности объекта зависит от того, насколько собственник объекта заполнил свой Паспорт Пожарной Безопасности Объекта.</div>
    <div style="margin-top: 8px; color: ${ratingColors[rating]} !important; font-weight: 500" class="mark__value">Заполненность Паспорта ПБО этого объекта: ${ratingPercentages[rating]}</div>
  </div>
  `
}

export function findMostFrequentAwTypeColor(markers: any[]) {
  const count = {
    Safe: 0,
    Normal: 0,
    Danger: 0
  }

  // Count the occurrences of each "targetElement.title" type
  markers.forEach((marker: any) => {
    switch (marker.targetElement.title) {
      case 'Safe':
        count['Safe']++
        break
      case 'Normal':
        count['Normal']++
        break
      case 'Danger':
        count['Danger']++
        break
    }
  })

  // Find the type with the maximum count
  let mostFrequentType = 'Safe'
  let maxCount = count['Safe']

  for (const type in count) {
    if (count[type as keyof typeof count] > maxCount) {
      mostFrequentType = type
      maxCount = count[type as keyof typeof count]
    }
  }

  return ratingColors[
    ratingTypes[mostFrequentType as keyof typeof ratingTypes] as keyof typeof ratingColors
  ]
}
