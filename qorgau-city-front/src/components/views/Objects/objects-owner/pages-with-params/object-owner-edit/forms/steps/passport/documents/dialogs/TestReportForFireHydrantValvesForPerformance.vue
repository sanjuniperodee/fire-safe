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
            НАИМЕНОВАНИЕ ЭКСПЛУАТИРУЮЩЕЙ ОРГАНИЗАЦИИ:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.operatingOrganizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            :counter="12"
            label="БИН"
            type="text"
            placeholder="Введите БИН организации"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.operatingOrganizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации"
            type="text"
            placeholder="Введите наименование организации"
            variant="solo-filled"
          ></v-text-field>

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
            НАИМЕНОВАНИЕ ОБСЛУЖИВАЮЩЕЙ ОРГАНИЗАЦИИ:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.serviceOrganizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            :counter="12"
            label="БИН"
            type="text"
            placeholder="Введите БИН организации"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.serviceOrganizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации"
            type="text"
            placeholder="Введите наименование организации"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ДАТА И ВРЕМЯ ИСПЫТАНИЙ:
          </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.testTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>
          <v-date-picker
            :max="new Date()"
            v-model="data.testDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Клапаны пожарного крана типа:
          </v-card-text>
          <v-text-field
            :rules="fireHydrantTypeValvesRules"
            v-model="data.fireHydrantTypeValves"
            style="min-width: 450px; padding-left: 20px"
            label="Тип клапанов пожарного крана"
            type="text"
            placeholder="Введите тип клапанов пожарного крана"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Пожарный насос типа:
          </v-card-text>
          <v-text-field
            :rules="firePumpTypeRules"
            v-model="data.firePumpType"
            style="min-width: 450px; padding-left: 20px"
            label="Тип пожарного насоса"
            type="text"
            placeholder="Введите тип пожарного насоса"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Давление у "диктующего" закрытого пожарного крана:
          </v-card-text>
          <v-text-field
            :rules="pressureRules"
            v-model="data.pressure"
            style="min-width: 450px; padding-left: 20px"
            label="Давление у 'диктующего' пожарного крана"
            placeholder="Введите давление пожарного крана"
            type="number"
            suffix="Мпа"
            variant="solo-filled"
          ></v-text-field>
          <!--  -->

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            РЕЗУЛЬТАТЫ ИСПЫТАНИЙ КЛАПАНОВ ПОЖАРНЫХ КРАНОВ НА РАБОТОСПОСОБНОСТЬ:
          </v-card-text>

          <div
            v-for="(item, i) in (data.results as resultItem[])"
            :key="item.valveNumber"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              v-model="item.valveNumber"
              :rules="valveNumberRules"
              style="min-width: 450px; padding-left: 20px"
              label="Номер стояка - номер крана"
              placeholder="Введите номер стояка - номер крана"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="valveDiaphragmNumberRules"
              v-model="item.valveDiaphragmNumber"
              style="min-width: 450px; padding-left: 20px"
              label="Номер диафрагмы крана"
              placeholder="Введите номер диафрагмы крана"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="allowableDiaphragmDiameterRules"
              v-model="item.allowableDiaphragmDiameter"
              style="min-width: 450px; padding-left: 20px"
              label="Диаметр диафрагмы, мм (допустимый)"
              suffix="мм"
              placeholder="Введите допустимый диаметр диафрагмы"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="measuredDiaphragmDiameterRules"
              v-model="item.measuredDiaphragmDiameter"
              style="min-width: 450px; padding-left: 20px"
              label="Диаметр диафрагмы, мм (измеренный)"
              suffix="мм"
              placeholder="Введите измеренный диаметр диафрагмы"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="valveCycleCountRules"
              v-model="item.valveCycleCount"
              style="min-width: 450px; padding-left: 20px"
              label="Количество циклов 'Открытие - Закрытие' клапана"
              placeholder="Введите количество циклов"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="leakageSealRules"
              v-model="item.leakageSeal"
              style="min-width: 450px; padding-left: 20px"
              label="Герметичность (наличие протечек)"
              placeholder="Введите герметичность"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="testResultsRules"
              v-model="item.testResults"
              style="min-width: 450px; padding-left: 20px"
              label="Результаты испытаний"
              placeholder="Введите результаты испытаний"
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

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ЗАКЛЮЧЕНИЕ ПО РЕЗУЛЬТАТАМ ИСПЫТАНИЙ:
          </v-card-text>
          <v-textarea
            v-model="data.conclusion"
            :rules="сonclusionRules"
            style="min-width: 450px; padding-left: 20px"
            placeholder="Введите заключение по результатам испытаний"
            variant="solo-filled"
          ></v-textarea>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ИСПЫТАНИЯ ПРОВЕЛИ:
          </v-card-text>
          <div
            v-for="(item, i) in data.testConducted as any"
            :key="i"
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
            @click="() => addTestConducted()"
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

const downloadPdf = () => {
  console.log('downloadPdf')
}

const isValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await form.value!.validate()
  return valid
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  form.value?.reset()
}
// // @ts-expect-error already in the documents
// import { runFont } from '@/helpers/jsPdfFont.js'

// import { jsPDF } from "jspdf";
// import { formatDateWithoutTime } from '@/helpers/formatTime';

type resultItem = {
  valveNumber: string
  valveDiaphragmNumber: string
  allowableDiaphragmDiameter: string
  measuredDiaphragmDiameter: string
  valveCycleCount: string
  leakageSeal: string
  testResults: string
}

const data = ref({
  operatingOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  objectName: {
    rka: '',
    address: '',
    objectName: ''
  },
  serviceOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  firePumpType: '',
  fireHydrantTypeValves: '',
  testTime: '',
  testDate: new Date(),
  results: [],
  pressure: '',
  testConducted: [],
  conclusion: ''
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

const fireHydrantTypeValvesRules = ref([
  (v: any) => !!v || 'Тип клапанов пожарного крана обязателен'
])

const firePumpTypeRules = ref([(v: any) => !!v || 'Тип пожарного насоса обязателен'])

const timeRules = ref([(v: any) => !!v || 'Время обязательно'])

const pressureRules = ref([(v: any) => !!v || 'Давление обязательно'])

const valveNumberRules = ref([(v: any) => !!v || 'Номер стояка - номер крана обязателен'])

const valveDiaphragmNumberRules = ref([(v: any) => !!v || 'Номер диафрагмы крана обязателен'])

const allowableDiaphragmDiameterRules = ref([
  (v: any) => !!v || 'Диаметр диафрагмы, мм (допустимый) обязателен'
])

const measuredDiaphragmDiameterRules = ref([
  (v: any) => !!v || 'Диаметр диафрагмы, мм (измеренный) обязателен'
])

const valveCycleCountRules = ref([
  (v: any) => !!v || 'Количество циклов "Открытие - Закрытие" клапана обязательно'
])

const leakageSealRules = ref([(v: any) => !!v || 'Герметичность (наличие протечек) обязательна'])

const testResultsRules = ref([(v: any) => !!v || 'Результаты испытаний обязательны'])

const сonclusionRules = ref([(v: any) => !!v || 'Выберите заключение по результатам испытаний'])

const DOCUMENT_KEY = 'Протокол испытаний клапанов пожарных кранов на работоспособность'
const documentsStore = useDocumentsStore()

const createNewRowOfResults = () => {
  data.value.results.push({
    valveNumber: '',
    valveDiaphragmNumber: '',
    allowableDiaphragmDiameter: '',
    measuredDiaphragmDiameter: '',
    valveCycleCount: '',
    leakageSeal: '',
    testResults: ''
  } as never)
}

const addTestConducted = () => {
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
