<template>
  <v-dialog
    v-model="documentsStore.dialogs[DOCUMENT_KEY]"
    width="auto"
  >
    <v-card style="padding: 20px">
      <v-card-title>
        {{ DOCUMENT_KEY }}
      </v-card-title>
      <v-card-item>
        <v-form
          ref="form"
          class="body"
        >
          <div
            v-for="(item, i) in (data.results as ListRowType[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              :rules="numberRules"
              v-model="item.serialNumber"
              style="min-width: 450px; padding-left: 20px"
              label="№ п/п"
              placeholder="Введите порядковый номер"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="rkaRules"
              v-model="item.objectRKANumber"
              style="min-width: 450px; padding-left: 20px"
              label="РКА объекта"
              placeholder="Введите РКА объекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="objectNameRules"
              v-model="item.objectName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование объекта"
              placeholder="Введите наименование объекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="addressRules"
              v-model="item.objectAddress"
              style="min-width: 450px; padding-left: 20px"
              label="Адрес объекта"
              placeholder="Введите адрес объекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="BINRules"
              v-model="item.ownerBIN"
              style="min-width: 450px; padding-left: 20px"
              label="БИН владельца объекта"
              placeholder="Введите БИН владельца объекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.ownerName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование владельца объекта"
              placeholder="Введите наименование владельца объекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.projectPositionAndSpecificationNumber"
              style="min-width: 450px; padding-left: 20px"
              label="Номер позиции и спецификации проекта"
              placeholder="Введите номер позиции и спецификации проекта"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.instrumentAndEquipmentName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование прибора и оборудования"
              placeholder="Введите наименование прибора и оборудования"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.instrumentAndEquipmentType"
              style="min-width: 450px; padding-left: 20px"
              label="Тип прибора и оборудования"
              placeholder="Введите тип прибора и оборудования"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.instrumentAndEquipmentSerialNumber"
              style="min-width: 450px; padding-left: 20px"
              label="Заводской номер прибора и оборудования"
              placeholder="Введите заводской номер прибора и оборудования"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.customerRepresentativeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН представителя заказчика"
              placeholder="Введите ИИН представителя заказчика"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="nameRules"
              v-model="item.customerRepresentativeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО представителя заказчика"
              placeholder="Введите ФИО представителя заказчика"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="jobTitleRules"
              v-model="item.customerRepresentativeJobTitle"
              style="min-width: 450px; padding-left: 20px"
              label="Должность представителя заказчика"
              placeholder="Введите должность представителя заказчика"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="IINRules"
              v-model="item.installationOrganizationRepresentativeIIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН представителя монтажной организации"
              placeholder="Введите ИИН представителя монтажной организации"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="nameRules"
              v-model="item.installationOrganizationRepresentativeFullName"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО представителя монтажной организации"
              placeholder="Введите ФИО представителя монтажной организации"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="jobTitleRules"
              v-model="item.installationOrganizationRepresentativeJobTitle"
              style="min-width: 450px; padding-left: 20px"
              label="Должность представителя монтажной организации"
              placeholder="Введите должность представителя монтажной организации"
              variant="solo-filled"
            ></v-text-field>
            <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
              Примечание
            </v-card-text>
            <v-textarea
              v-model="item.caption"
              :rules="commonRules"
              style="min-width: 450px; padding-left: 20px"
              placeholder="Введите примечание"
              variant="solo-filled"
            ></v-textarea>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createListRow()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >
        </v-form>
      </v-card-item>
      <v-card-actions style="display: flex; justify-content: end">
        <v-btn
          color="primary"
          @click="downloadPdf"
          >Скачать PDF</v-btn
        >
        <v-btn
          color="#d20f0d"
          variant="tonal"
          @click="() => documentsStore.closeDialog(DOCUMENT_KEY)"
          style="text-transform: none"
          >Отмена</v-btn
        >
        <v-btn
          color="#5b9271"
          variant="elevated"
          @click="() => generateDocument()"
          style="text-transform: none"
          >Сохранить</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useDocumentsStore } from '@/stores/DocumentsStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { ref } from 'vue'
// @ts-expect-error
import { robotoBase64 } from './fontData'
import { jsPDF } from 'jspdf'

const form = ref(null)
const snackbarStore = useSnackbarStore()

const isValid = async () => {
  // @ts-expect-error
  const { valid } = await form.value!.validate()
  return valid
}

const resetForm = () => {
  // @ts-expect-error
  form.value?.reset()
}

type ListRowType = {
  serialNumber: string
  objectRKANumber: string
  objectName: string
  objectAddress: string
  ownerBIN: string
  ownerName: string
  projectPositionAndSpecificationNumber: string
  instrumentAndEquipmentName: string
  instrumentAndEquipmentType: string
  instrumentAndEquipmentSerialNumber: string
  customerRepresentativeIIN: string
  customerRepresentativeFullName: string
  customerRepresentativeJobTitle: string
  installationOrganizationRepresentativeIIN: string
  installationOrganizationRepresentativeFullName: string
  installationOrganizationRepresentativeJobTitle: string
  caption: string
}

const data = ref({
  results: []
})

const createListRow = () => {}
console.log('createListRow')

// data.value.results.push({
//   serialNumber: '',
//   objectRKANumber: '',
//   objectName: '',
//   objectAddress: '',
//   ownerBIN: '',
//   ownerName: '',
//   projectPositionAndSpecificationNumber: '',
//   instrumentAndEquipmentName: '',
//   instrumentAndEquipmentType: '',
//   instrumentAndEquipmentSerialNumber: '',
//   customerRepresentativeIIN: '',
//   customerRepresentativeFullName: '',
//   customerRepresentativeJobTitle: '',
//   installationOrganizationRepresentativeIIN: '',
//   installationOrganizationRepresentativeFullName: '',
//   installationOrganizationRepresentativeJobTitle: '',
//   caption: '',
// } as ListRowType);

const downloadPdf = async () => {
  if (await isValid()) {
    const doc = new jsPDF()
    doc.addFileToVFS('Roboto-Regular.ttf', robotoBase64)
    doc.addFont('Roboto-Regular.ttf', 'Roboto', 'normal')
    doc.setFont('Roboto')
    const lineSpacing = 10
    let linePosition = 20

    const addLine = (text: string) => {
      doc.text(text, 10, linePosition)
      linePosition += lineSpacing
    }

    // Add the title
    doc.setFontSize(16)
    addLine(
      'ВЕДОМОСТЬ смонтированных приборов и оборудования систем и установок пожарной автоматики'
    )
    doc.setFontSize(12)

    // Iterate over each result
    data.value.results.forEach((result: ListRowType) => {
      addLine(`Serial Number: ${result.serialNumber}`)
      addLine(`Object RKA Number: ${result.objectRKANumber}`)
      addLine(`Object Name: ${result.objectName}`)
      // Add other properties of each result object similarly
    })

    // Finalize and download the PDF
    doc.save('inspection_report.pdf')
  } else {
    snackbarStore.pullSnackbar('Заполните все поля прежде чем сохранить PDF.', 3000, '#d20f0d')
  }
}

const rkaRules = ref([
  (v: any) => !!v || 'Номер РКА обязателен',
  (v: any) => !isNaN(Number(v)) || 'Номер РКА должен быть числом',
  (v: any) => v.length === 16 || 'Длина номера РКА обязана быть 16 цифр'
])

const addressRules = ref([(v: any) => !!v || 'Адрес обязателен'])

const numberRules = ref([
  (v: any) => !!v || 'Порядковый номер обязателен',
  (v: any) => !isNaN(Number(v)) || 'Поле должно быть числом'
])

const objectNameRules = ref([(v: any) => !!v || 'Наименование объекта обязателена'])

const IINRules = ref([
  (v: any) => !!v || 'ИИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
  (v: any) => v.length === 12 || 'Длина ИИН должна быть 12 цифр'
])

const nameRules = ref([
  (v: string) => !!v || 'ФИО обязательно',
  (v: string) => v.split(' ').length === 3 || 'Напишите полное ФИО'
])

const jobTitleRules = ref([(v: any) => !!v || 'Должность обязательна'])

const BINRules = ref([
  (v: any) => !!v || 'БИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'БИН должен быть числом',
  (v: any) => v.length === 12 || 'Длина БИН должна быть 12 цифр'
])

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const DOCUMENT_KEY =
  'ВЕДОМОСТЬ смонтированных приборов и оборудования систем и установок пожарной автоматики'
const documentsStore = useDocumentsStore()

const generateDocument = async () => {
  if (await isValid()) {
    await documentsStore.generateDocument(DOCUMENT_KEY, data.value)
    resetForm()
  } else {
    snackbarStore.pullSnackbar('Заполните все поля прежде чем сохранить документ.', 3000, '#d20f0d')
    setTimeout(() => {
      const firstInvalidElement = document.querySelector('.v-input--error .v-input__control')
      if (firstInvalidElement) {
        // Scroll into view
        firstInvalidElement.scrollIntoView({ behavior: 'smooth', block: 'center' })

        // Focus the input element if possible
        const input = firstInvalidElement.querySelector('input, textarea, select')
        // @ts-expect-error
        if (input) input.focus()
      }
    }, 100)
  }
}
</script>

<style lang="scss" scoped>
.body {
  display: flex;
  flex-direction: column;
  align-items: start !important;
}
</style>
