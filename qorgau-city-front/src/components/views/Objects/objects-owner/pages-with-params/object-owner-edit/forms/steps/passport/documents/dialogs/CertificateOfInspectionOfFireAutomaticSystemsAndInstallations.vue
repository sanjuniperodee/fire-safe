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
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наименование объекта:
          </v-card-text>
          <v-text-field
            :rules="rkaRules"
            v-model="data.objectName.rka"
            style="min-width: 450px; padding-left: 20px"
            label="РКА"
            placeholder="Введите номер РКА"
            :counter="16"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="addressRules"
            v-model="data.objectName.address"
            style="min-width: 450px; padding-left: 20px"
            label="Адрес"
            type="text"
            placeholder="Введите адрес объекта"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="objectNameRules"
            v-model="data.objectName.objectName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование объекта"
            type="text"
            placeholder="Введите наименование объекта"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Председатель комиссии:
          </v-card-text>
          <v-text-field
            :rules="IINRules"
            v-model="data.chairmanOfCommision.IIN"
            style="min-width: 450px; padding-left: 20px"
            label="ИИН"
            placeholder="Введите ваш ИИН"
            :counter="12"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="nameRules"
            v-model="data.chairmanOfCommision.name"
            style="min-width: 450px; padding-left: 20px"
            label="ФИО"
            placeholder="Введите ваше ФИО"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="jobTitleRules"
            v-model="data.chairmanOfCommision.jobTitle"
            style="min-width: 450px; padding-left: 20px"
            label="Должность"
            placeholder="Введите вашу должность"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="BINRules"
            v-model="data.chairmanOfCommision.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите ваш БИН"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.chairmanOfCommision.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации"
            placeholder="Введите ваше наименование организации"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Члены комиссии:
          </v-card-text>

          <div
            v-for="(item, i) in (data.commissionMembers as commisionMember[])"
            :key="item.id"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Член комиссии {{ i + 1 }}
            </v-card-text>
            <v-text-field
              :rules="IINRules"
              v-model="item.IIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН"
              placeholder="Введите ваш ИИН"
              :counter="12"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              :rules="nameRules"
              v-model="item.name"
              style="min-width: 450px; padding-left: 20px"
              label="ФИО"
              placeholder="Введите ваше ФИО"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              :rules="jobTitleRules"
              v-model="item.jobTitle"
              style="min-width: 450px; padding-left: 20px"
              label="Должность"
              placeholder="Введите вашу должность"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              :rules="BINRules"
              v-model="item.BIN"
              style="min-width: 450px; padding-left: 20px"
              label="БИН"
              placeholder="Введите ваш БИН"
              variant="solo-filled"
            ></v-text-field>
            <v-text-field
              :rules="organizationNameRules"
              v-model="item.organizationName"
              style="min-width: 450px; padding-left: 20px"
              label="Наименование организации"
              placeholder="Введите ваше наименование организации"
              variant="solo-filled"
            ></v-text-field>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createNewCommissionMember()"
            style="text-transform: none; margin-left: 20px"
            >Добавить</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наименование установки:
          </v-card-text>
          <v-text-field
            v-model="data.installationName"
            :rules="installationNameRules"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование установки"
            placeholder="Введите наименование установки"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Место размещения установки:
          </v-card-text>
          <v-text-field
            v-model="data.installationPlace"
            :rules="installationLocationRules"
            style="min-width: 450px; padding-left: 20px"
            label="Место размещения установки"
            placeholder="Введите место размещения установки"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наименование элементов:
          </v-card-text>
          <v-text-field
            v-model="data.elementsName"
            :rules="elementsNameRules"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование элементов"
            placeholder="Введите наименование элементов"
            variant="solo-filled"
          ></v-text-field>

          <div style="display: flex; justify-content: space-between; flex-wrap: wrap">
            <div>
              <v-card-text style="font-weight: 700; font-size: 22px">
                Работа выполнялись с:
              </v-card-text>
              <v-date-picker v-model="data.carriedOutFrom"></v-date-picker>
            </div>
            <div>
              <v-card-text style="font-weight: 700; font-size: 22px">
                Работа выполнялись по:
              </v-card-text>
              <v-date-picker v-model="data.carriedOutTo"></v-date-picker>
            </div>
          </div>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ПРИ ОСМОТРЕ ВЫЯВЛЕНО:
          </v-card-text>
          <v-textarea
            v-model="data.revealedDuringExamination"
            :rules="inspectionResultsRules"
            style="min-width: 450px; padding-left: 20px"
            placeholder="Введите что было выявлено при осмотре"
            variant="solo-filled"
          ></v-textarea>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ЗАКЛЮЧЕНИЕ КОМИССИИ:
          </v-card-text>
          <v-select
            v-model="data.commissionConclusion"
            :rules="commissionConclusionRules"
            label="Выберите заключение комиссии"
            style="min-width: 450px; padding-left: 20px"
            :items="[
              'Дальнейшая эксплуатация существующих систем и установок пожарной автоматики возможна/невозможна или необходимо выполнить монтаж новых систем и установок',
              'Требуется ремонт отдельных технических средств систем и установок пожарной автоматики',
              'Необходимо продлить эксплуатацию систем и установок пожарной автоматики, с указанием срока следующего освидетельствования'
            ]"
            variant="solo-filled"
          ></v-select>
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
  <div id="content"></div>
</template>

<script setup lang="ts">
import { useDocumentsStore } from '@/stores/DocumentsStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { ref } from 'vue'
//@ts-ignore
import { robotoBase64 } from './fontData'
import { jsPDF } from 'jspdf'

const form = ref(null)

const isValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await form.value!.validate()
  return valid
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  form.value?.reset()
}

type commisionMember = {
  id: ''
  IIN: ''
  name: ''
  jobTitle: ''
  BIN: ''
  organizationName: ''
}

const snackbarStore = useSnackbarStore()

const data = ref({
  objectName: {
    rka: '',
    address: '',
    objectName: ''
  },
  chairmanOfCommision: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  commissionMembers: [],
  installationName: '',
  installationPlace: '',
  elementsName: '',
  carriedOutFrom: new Date(),
  carriedOutTo: new Date(),
  revealedDuringExamination: '',
  commissionConclusion: ''
})

const rkaRules = ref([
  (v: any) => !!v || 'Номер РКА обязателен',
  (v: any) => !isNaN(Number(v)) || 'Номер РКА должен быть числом',
  (v: any) => parseInt(v.length) === 16 || 'Длина номера РКА обязана быть 16 цифр'
])

const addressRules = ref([(v: any) => !!v || 'Адрес обязателен'])

const objectNameRules = ref([(v: any) => !!v || 'Наименование объекта обязателена'])

const IINRules = ref([
  (v: any) => !!v || 'ИИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
])

const nameRules = ref([
  (v: string) => !!v || 'ФИО обязательно',
  (v: string) => v.split(' ').length === 3 || 'Напишите полное ФИО'
])

const jobTitleRules = ref([(v: any) => !!v || 'Должность обязательна'])

const BINRules = ref([
  (v: any) => !!v || 'БИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'БИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина БИН должна быть 12 цифр'
])

const organizationNameRules = ref([(v: any) => !!v || 'Наименование организации обязательно'])

const installationNameRules = ref([(v: any) => !!v || 'Наименование установки обязательно'])

const installationLocationRules = ref([(v: any) => !!v || 'Место размещения установки обязательно'])

const elementsNameRules = ref([(v: any) => !!v || 'Наименование элементов обязательно'])

const inspectionResultsRules = ref([(v: any) => !!v || 'Поле обязательно'])

const commissionConclusionRules = ref([(v: any) => !!v || 'Выберите заключение комиссии'])

const DOCUMENT_KEY = 'АКТ освидетельствования систем и установок пожарной автоматики'
const documentsStore = useDocumentsStore()

function generateUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

const createNewCommissionMember = () => {
  data.value.commissionMembers.push({
    id: generateUniqueId(),
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  } as never)
}

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
    addLine('АКТ освидетельствования систем и установок пожарной автоматики')
    doc.setFontSize(12)

    // Add Object Details
    addLine(`РКА Номер: ${data.value.objectName.rka}`)
    addLine(`Адресс: ${data.value.objectName.address}`)
    addLine(`Наименование объекта: ${data.value.objectName.objectName}`)

    // Chairman of Commission
    addLine(`Председатель ИИН: ${data.value.chairmanOfCommision.IIN}`)
    addLine(`Председатель Имя: ${data.value.chairmanOfCommision.name}`)
    addLine(`Председатель Должность: ${data.value.chairmanOfCommision.jobTitle}`)
    addLine(`Председатель БИН: ${data.value.chairmanOfCommision.BIN}`)
    addLine(`Председатель Организация: ${data.value.chairmanOfCommision.organizationName}`)

    // Commission Members
    data.value.commissionMembers.forEach((member: commisionMember, index) => {
      addLine(`Член комисии ${index + 1} ИИН: ${member.IIN}`)
      addLine(`Член комисии ${index + 1} Имя: ${member.name}`)
      addLine(`Член комисии ${index + 1} Должность: ${member.jobTitle}`)
      addLine(`Член комисии ${index + 1} БИН: ${member.BIN}`)
      addLine(`Член комисии ${index + 1} Организация: ${member.organizationName}`)
    })

    // Other Details
    addLine(`Наименование установки: ${data.value.installationName}`)
    addLine(`Место установки: ${data.value.installationPlace}`)
    addLine(`Наименование элементов: ${data.value.elementsName}`)
    addLine(`Работа выполнялись с: ${data.value.carriedOutFrom.toISOString().split('T')[0]}`)
    addLine(`Работа выполнялись по: ${data.value.carriedOutTo.toISOString().split('T')[0]}`)
    addLine(`При осмотре выявлено: ${data.value.revealedDuringExamination}`)
    addLine(`Заключение комиссии: ${data.value.commissionConclusion}`)

    // Finalize and download the PDF
    doc.save('inspection_report.pdf')
  } else {
    snackbarStore.pullSnackbar('Заполните все поля прежде чем сохранить PDF.', 3000, '#d20f0d')
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
