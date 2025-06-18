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
            Дата проведения испытаний:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.testDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-text-field
            v-model="data.testObjectName"
            :rules="commonRules"
            label="Наименование объекта испытаний"
            placeholder="Введите наименование объекта испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.testObjectAddress"
            :rules="commonRules"
            label="Адрес объекта испытаний"
            placeholder="Введите адрес объекта испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Результаты измерений:
          </v-card-text>
          <div
            v-for="(item, i) in (data.results as resultItem[])"
            :key="i + 'resultItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-card-text
              style="
                font-weight: 700;
                font-size: 16px;
                font-family: 'Noto Sans', sans-serif;
                margin-top: 20px;
              "
            >
              Наименование участка питающего кабеля и оборудования
            </v-card-text>

            <v-select
              v-model="item.cableSectionAndEquipmentName"
              :items="cableSectionAndEquipmentNameList"
              :rules="commonRules"
              label="Выбрать наименование участка"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-select>

            <v-text-field
              v-model="item.insulationResistanceAB"
              :rules="commonRules"
              label="Сопротивление изоляции, Мом A-B"
              placeholder="Введите сопротивление изоляции A-B"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.insulationResistanceAC"
              :rules="commonRules"
              label="Сопротивление изоляции, Мом A-C"
              placeholder="Введите сопротивление изоляции A-C"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.insulationResistanceBC"
              :rules="commonRules"
              label="Сопротивление изоляции, Мом B-C"
              placeholder="Введите сопротивление изоляции B-C"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.insulationResistanceA0"
              :rules="commonRules"
              label="Сопротивление изоляции, Мом A-0"
              placeholder="Введите сопротивление изоляции A-0"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.insulationResistanceB0"
              :rules="commonRules"
              label="Сопротивление изоляции, Мом B-0"
              placeholder="Введите сопротивление изоляции B-0"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.insulationResistanceC0"
              :rules="commonRules"
              label="Сопротивление изоляции, Мом C-0"
              placeholder="Введите сопротивление изоляции C-0"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.normResistance"
              :rules="commonRules"
              label="Норма сопротивления, Мом"
              placeholder="Введите норму сопротивления"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createNewRowOfResults()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <!--  -->

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Измерения сопротивления растеканию тока заземляющих устройств:
          </v-card-text>

          <div
            v-for="(item, i) in (data.measurementsOfGroundingDevicesLeakageResistance as measurementsOfGroundingDevicesLeakageResistanceItem[])"
            :key="i + 'measurementsOfGroundingDevicesLeakageResistanceItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              v-model="item.measurementObject"
              :rules="commonRules"
              label="Объект измерения (заземлитель или заземляющее устройство)"
              placeholder="Введите объект измерения"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.normativeResistance"
              :rules="commonRules"
              label="Сопротивление по норме (или по проекту), Ом"
              placeholder="Введите сопротивление по норме"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.measuredResistance"
              :rules="commonRules"
              label="Сопротивление измерение, Ом"
              placeholder="Введите измеренное сопротивление"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createNewRowOfMeasurementsOfGroundingDevicesLeakageResistance()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-text-field
            v-model="data.additionalChecks"
            :rules="commonRules"
            label="Дополнительные проверки"
            placeholder="Введите информацию о дополнительных проверках"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.environmentalConditions"
            :rules="commonRules"
            label="Условия окружающей среды при проведении испытаний"
            placeholder="Введите условия окружающей среды"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.normativeDocuments"
            :rules="commonRules"
            label="Нормативно-технические документы"
            placeholder="Введите нормативно-технические документы"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Измерительные приборы:
          </v-card-text>

          <div
            v-for="(item, i) in (data.measuringInstruments as measuringInstrumentsItem[])"
            :key="i + 'measuringInstrumentsItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-text-field
              v-model="item.name"
              :rules="commonRules"
              label="Наименование"
              placeholder="Введите наименование"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.type"
              :rules="commonRules"
              label="Тип"
              placeholder="Введите тип"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.serialNumber"
              :rules="commonRules"
              label="Заводской №"
              placeholder="Введите заводской номер"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.voltage"
              :rules="commonRules"
              label="Напряжение, В"
              placeholder="Введите напряжение"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.errorMargin"
              :rules="commonRules"
              label="Погрешность"
              placeholder="Введите погрешность"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
              Дата след. проверки:
            </v-card-text>
            <v-date-picker
              :max="new Date()"
              v-model="item.nextCalibrationDate"
              style="margin-left: 20px"
              show-adjacent-months
              color="#f57c01"
            ></v-date-picker>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createNewRowOfMeasuringInstruments()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-text-field
            v-model="data.conclusionNTD"
            :rules="commonRules"
            label="Вывод на соответствие требованиям НТД"
            placeholder="Введите вывод на соответствие требованиям НТД"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Испытания провели:
          </v-card-text>

          <div
            v-for="(item, i) in (data.testConducted as TestConductedMember[])"
            :key="item.BIN"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Сотрудник {{ i + 1 }}
            </v-card-text>
            <v-text-field
              :rules="IINRules"
              v-model="item.IIN"
              style="min-width: 450px; padding-left: 20px"
              label="ИИН"
              placeholder="Введите ваш ИИН"
              :counter="20"
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
            @click="() => createNewTestConducted()"
            style="text-transform: none; margin-left: 20px"
            >Добавить</v-btn
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
  <div id="content"></div>
</template>

<script setup lang="ts">
import { useDocumentsStore } from '@/stores/DocumentsStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { ref } from 'vue'

const form = ref(null)
const snackbarStore = useSnackbarStore()

const isValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await form.value!.validate()
  return valid
}

const downloadPdf = () => {
  console.log('downloadPdf')
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  form.value?.reset()
}

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

const cableSectionAndEquipmentNameList = [
  'КРПТ 3х10',
  'АПВ 1 3(1х4)',
  'АПВ 1 3(1х6)',
  'АПВ 1 3(1х16)',
  'КРПТ 3х10',
  'АВВГ 4х2,5',
  'АВВГ 4х16',
  'АПВ 1 3(1х16)',
  'АПВ 1 3(1х16)',
  'АПВ 1 3(1х6)',
  'АПВ 1 3(1х6)',
  'АВВГ 3х10+1х6',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'ВВГ 4х2,5',
  'ВВГ',
  'ВВГ',
  'АВВГ 4х6',
  'АВВГ 3х2,5',
  'АВВГ 3х2,5',
  'АВВГ 3х4',
  'АВВГ 4х6',
  'АКВВГ 10х2,5',
  'АВВГ 4х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х4+1х2,5',
  'АВВГ 3х10+1х2,5',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВГ 4х4',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВГ 4х16',
  'АПВ 1 3(1х16)',
  'АПВ 1 3(1х16)',
  'АПВ 1 3(1х6)',
  'АПВ 1 3(1х6)',
  'АВВГ 3х10+1х6',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'ВВГ 4х2,5',
  'ВВГ',
  'ВВГ',
  'АВВГ 4х6',
  'АВВГ 3х2,5',
  'АВВГ 3х2,5',
  'АВВГ 3х4',
  'АВВГ 4х6',
  'АКВВГ 10х2,5',
  'АВВГ 4х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВГ 3х4+1х2,5',
  'АВВГ 3х10+1х2,5',
  'АВВГ 3х10+1х6',
  'АВВГ 3х10+1х6',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВГ 4х4',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВГ 4х4',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  '2АПРТО 3 (1х70)',
  'АВВГ 4х6',
  'АВВГ 3х16+1х6',
  'АКВВГ 9х2,5',
  'АВВГ 3х35+1х16',
  'АВВГ 3х35+1х16',
  'АВВГ 4х4',
  'АКВВГ 9х2,5',
  'АКВВГ 9х2,5',
  'АВВГ 2х10',
  'АВВГ 4х6',
  'АКВВГ 12х2,5',
  'АВВ 2х2,5',
  '2АПРТО 3 (1х70)',
  'АВВГ 3х35+1х16',
  'АВВГ 3х35+1х16',
  'АВВГ 3х16+1х10',
  'АВВГ 3х16+1х10',
  'АВВГ 3х16+1х10',
  'АВВГ 3х16+1х10',
  'АПВ 1 3(1х70)',
  'КРПТ 4х4',
  'АВВГ 3х6',
  'КРПТ 4х6',
  'АВВГ 3х4+1х2,5',
  'АВВ 2х2,5',
  'АВВ 2х2,5',
  'АВВГ 4х2,5',
  'АПВ 1 2х4',
  'АВВГ 4х4',
  'АВВГ 3х16+1х6',
  'АВВГ 3х25+1х10',
  'КГ 3х4+1х2,5',
  'АППВ 2х2,5',
  'КГ 3х10+1х6',
  'КГ 4х2,5',
  'КГ 3х4+1х2,5',
  'NYM 2х2,5'
]

type TestConductedMember = {
  IIN: ''
  name: ''
  jobTitle: ''
  BIN: ''
  organizationName: ''
}

type resultItem = {
  cableSectionAndEquipmentName: string
  insulationResistanceAB: string
  insulationResistanceAC: string
  insulationResistanceBC: string
  insulationResistanceA0: string
  insulationResistanceB0: string
  insulationResistanceC0: string
  normResistance: string
}

type measurementsOfGroundingDevicesLeakageResistanceItem = {
  measurementObject: string // Объект измерения (заземлитель или заземляющее устройство)
  normativeResistance: string // Сопротивление по норме (или по проекту), (Ом)
  measuredResistance: string // Сопротивление измерение (Ом)
}

type measuringInstrumentsItem = {
  name: string // Наименование
  type: string // Тип
  serialNumber: string // Заводской №
  voltage: string // Напряжение, В
  errorMargin: string // Погрешность
  nextCalibrationDate: Date // Дата след. проверки
}

const data = ref({
  testDate: new Date(),
  testObjectName: '',
  testObjectAddress: '',
  results: [],
  measurementsOfGroundingDevicesLeakageResistance: [],
  additionalChecks: '',
  environmentalConditions: '',
  normativeDocuments: '',
  measuringInstruments: [],
  conclusionNTD: '',
  testConducted: []
})

const DOCUMENT_KEY = 'ПРОТОКОЛ ИСПЫТАНИЙ измерения сопротивления изоляции проводов и кабелей'
const documentsStore = useDocumentsStore()
const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const createNewRowOfResults = () => {
  data.value.results.push({
    cableSectionAndEquipmentName: '',
    insulationResistanceAB: '',
    insulationResistanceAC: '',
    insulationResistanceBC: '',
    insulationResistanceA0: '',
    insulationResistanceB0: '',
    insulationResistanceC0: '',
    normResistance: ''
  } as never)
}

const createNewRowOfMeasurementsOfGroundingDevicesLeakageResistance = () => {
  data.value.measurementsOfGroundingDevicesLeakageResistance.push({
    measurementObject: '', // Объект измерения (заземлитель или заземляющее устройство)
    normativeResistance: '', // Сопротивление по норме (или по проекту), (Ом)
    measuredResistance: '' // Сопротивление измерение (Ом)
  } as never)
}

const createNewRowOfMeasuringInstruments = () => {
  data.value.measuringInstruments.push({
    name: '', // Наименование
    type: '', // Тип
    serialNumber: '', // Заводской №
    voltage: '', // Напряжение, В
    errorMargin: '', // Погрешность
    nextCalibrationDate: new Date() // Дата след. проверки
  } as never)
}

const createNewTestConducted = () => {
  data.value.testConducted.push({
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
</script>

<style lang="scss" scoped>
.body {
  display: flex;
  flex-direction: column;
  align-items: start !important;
}
</style>
