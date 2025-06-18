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
            Наименование организации - заказчика:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.customerOrganizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите БИН заказчика"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.customerOrganizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации заказчика"
            placeholder="Введите ваше наименование организации заказчика"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Решением от:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.solutionFrom"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Номер решения о назначении комиссии:
          </v-card-text>
          <v-text-field
            :rules="numberOfTheDecisionRules"
            v-model="data.numberOfTheDecision"
            style="min-width: 450px; padding-left: 20px"
            label="Номер решения о назначении комиссии"
            prefix="№"
            placeholder="Введите Номер решения о назначении комиссии"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Председатель - представитель заказчика (генподрядчика):
          </v-card-text>
          <v-text-field
            :rules="IINRules"
            v-model="data.chairmanRepresentativeOfCustomer.IIN"
            style="min-width: 450px; padding-left: 20px"
            label="ИИН"
            placeholder="Введите ИИН"
            :counter="12"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="nameRules"
            v-model="data.chairmanRepresentativeOfCustomer.name"
            style="min-width: 450px; padding-left: 20px"
            label="ФИО"
            placeholder="Введите ФИО"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="jobTitleRules"
            v-model="data.chairmanRepresentativeOfCustomer.jobTitle"
            style="min-width: 450px; padding-left: 20px"
            label="Должность"
            placeholder="Введите должность"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="BINRules"
            v-model="data.chairmanRepresentativeOfCustomer.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите БИН"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.chairmanRepresentativeOfCustomer.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации"
            placeholder="Введите ваше наименование организации"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Члены комиссии - представители монтажной организации:
          </v-card-text>

          <div
            v-for="(item, i) in (data.commissionMembersInstallationOrganization as commisionMember[])"
            :key="item.BIN"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Член комиссии - представитель монтажной организации {{ i + 1 }}:
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
            @click="() => createNewCommissionMemberInstallationOrganization()"
            style="text-transform: none; margin-left: 20px"
            >Добавить</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Члены комиссии - представители пусконаладочной организации
          </v-card-text>

          <div
            v-for="(item, i) in (data.commissionMembersCommissioningOrganization as commisionMember[])"
            :key="item.BIN"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Член комиссии - представитель монтажной организации {{ i + 1 }}:
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
            @click="() => createNewCommissionMemberCommissioningOrganization()"
            style="text-transform: none; margin-left: 20px"
            >Добавить</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Произвела проверку выполненных работ и УСТАНОВИЛА:
          </v-card-text>
          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Наименование установки:
          </v-card-text>
          <v-text-field
            v-model="data.installationName"
            :rules="commonRules"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование установки"
            placeholder="Введите наименование установки"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
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

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Наименования организации разработавший проект:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.developedProjectOrganizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите БИН организации разработавший проект"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.developedProjectOrganizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации разработавший проект"
            placeholder="Введите ваше наименование организации разработавший проект"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Наименование организации выполнившая монтажные работы:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.performedInstallationWorkOrganizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите БИН организации разработавший проект"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.performedInstallationWorkOrganizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации разработавший проект"
            placeholder="Введите ваше наименование организации разработавший проект"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Монтажные работы выполнены с:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.installationWorkCarriedOutFrom"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>
          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Монтажные работы выполнены по:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.installationWorkCarriedOutTo"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Наименование организации выполнившая пусконаладочные работы:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.performedCommissioningWorkOrganizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите БИН организации разработавший проект"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.performedCommissioningWorkOrganizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации разработавший проект"
            placeholder="Введите ваше наименование организации разработавший проект"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Пусконаладочные работы выполнены с:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.commissioningWorkCarriedOutFrom"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Пусконаладочные работы выполнены по:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.commissioningWorkCarriedOutTo"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Считать принятой в эксплуатацию с:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.acceptedForOperationFrom"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Oценка качества выполненных работ:
          </v-card-text>
          <v-select
            v-model="data.assessmentQualityWork"
            :rules="commonRules"
            label="Выберите заключение комиссии"
            style="min-width: 450px; padding-left: 20px"
            :items="['Отлично', 'Хорошо', 'Удовлетворительно']"
            variant="solo-filled"
          ></v-select>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Перечень прилагаемой к акту документации
          </v-card-text>
          <v-textarea
            v-model="data.listofDocumentation"
            :rules="commonRules"
            style="min-width: 450px; padding-left: 20px"
            placeholder="Введите заключение по результатам испытаний"
            variant="solo-filled"
          ></v-textarea>
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
// @ts-ignore
import { robotoBase64 } from './fontData'
import { jsPDF } from 'jspdf'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const form = ref(null)
const snackbarStore = useSnackbarStore()

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
  IIN: ''
  name: ''
  jobTitle: ''
  BIN: ''
  organizationName: ''
}

const data = ref({
  customerOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  solutionFrom: new Date(),
  numberOfTheDecision: '',
  chairmanRepresentativeOfCustomer: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  commissionMembersInstallationOrganization: [],
  commissionMembersCommissioningOrganization: [],
  commissionMembers: [],
  chairmanOfCommision: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  installationPlace: '',
  revealedDuringExamination: '',
  elementsName: '',
  commissionConclusion: '',
  installationName: '',
  objectName: {
    rka: '',
    address: '',
    objectName: ''
  },
  developedProjectOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  performedInstallationWorkOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  performedCommissioningWorkOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  carriedOutTo: new Date(),
  carriedOutFrom: new Date(),
  installationWorkCarriedOutFrom: new Date(),
  installationWorkCarriedOutTo: new Date(),
  commissioningWorkCarriedOutFrom: new Date(),
  commissioningWorkCarriedOutTo: new Date(),
  acceptedForOperationFrom: new Date(),
  assessmentQualityWork: '',
  listofDocumentation: ''
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

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const numberOfTheDecisionRules = ref([
  (v: any) => !!v || 'Номер решения обязателен',
  (v: any) => !isNaN(Number(v)) || 'Номер решения должен быть числом'
])

const DOCUMENT_KEY = 'АКТ приемки в эксплуатацию систем и установок пожарной автоматики'
const documentsStore = useDocumentsStore()

const createNewCommissionMemberInstallationOrganization = () => {
  data.value.commissionMembersInstallationOrganization.push({
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  } as never)
}

const createNewCommissionMemberCommissioningOrganization = () => {
  data.value.commissionMembersCommissioningOrganization.push({
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
  }
}

const downloadPdf = () => {
  if (data.value) {
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
    data.value.commissionMembers.forEach((member: commisionMember, index: number) => {
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
    snackbarStore.pullSnackbar('Данные отсутствуют. Невозможно сгенерировать PDF.', 3000, '#d20f0d')
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
