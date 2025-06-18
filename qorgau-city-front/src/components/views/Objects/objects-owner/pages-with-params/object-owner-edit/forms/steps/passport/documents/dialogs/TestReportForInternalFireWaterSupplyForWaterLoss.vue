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
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%"> Город: </v-card-text>
          <v-text-field
            :rules="cityRules"
            v-model="data.city"
            style="min-width: 450px; padding-left: 20px"
            label="Город"
            placeholder="Введите город"
            variant="solo-filled"
          ></v-text-field>
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
            Номера стояков пожарного крана:
          </v-card-text>
          <v-text-field
            :rules="commonRules"
            v-model="data.numbersOfFireHydrantRisers"
            style="min-width: 450px; padding-left: 20px"
            label="Номер стояков пожарного крана"
            type="text"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            НОМЕРА ИСПЫТЫВАЕМЫХ ПОЖАРНЫХ КРАНОВ:
          </v-card-text>
          <v-text-field
            :rules="commonRules"
            v-model="data.numberOfTestedFireValues"
            style="min-width: 450px; padding-left: 20px"
            label="Номера испытываемых пожарных кранов"
            type="text"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="hydrantTypeRules"
            v-model="data.hydrantType"
            style="min-width: 450px; padding-left: 20px"
            label="Клапан пожарного крана типа"
            placeholder="Введите тип клапана пожарного крана"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="fireHoseTypeRules"
            v-model="data.fireHoseType"
            style="min-width: 450px; padding-left: 20px"
            label="Ручной пожарный ствол типа"
            placeholder="Введите тип ручного пожарного ствола"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="fireHoseLengthRules"
            v-model="data.fireHoseLength"
            type="number"
            style="min-width: 450px; padding-left: 20px"
            label="Длина пожарного рукава"
            suffix="м"
            placeholder="Введите длину пожарного рукава"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="fireHoseDiameterRules"
            v-model="data.fireHoseDiameter"
            type="number"
            style="min-width: 450px; padding-left: 20px"
            label="Диаметр пожарного рукава"
            suffix="мм"
            placeholder="Введите диаметр пожарного рукава"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="firePumpTypeRules"
            v-model="data.firePumpType"
            style="min-width: 450px; padding-left: 20px"
            label="Пожарный насос типа"
            placeholder="Введите тип пожарного насоса"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="pumpPressureRules"
            v-model="data.pumpPressure"
            type="number"
            style="min-width: 450px; padding-left: 20px"
            label="Напор пожарного насоса при закрытых пожарных кранах"
            suffix="Мпа"
            placeholder="Введите напор пожарного насоса"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="flowRateRules"
            v-model="data.flowRate"
            style="min-width: 450px; padding-left: 20px"
            type="number"
            label="Расход 'диктующего' пожарного крана"
            placeholder="Введите расход пожарного крана"
            suffix="л/c"
            variant="solo-filled"
          ></v-text-field>

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

          <v-text-field
            :rules="simultaneousSprinklersRules"
            v-model="data.simultaneousSprinklers"
            suffix="шт"
            type="number"
            style="min-width: 450px; padding-left: 20px"
            label="Количество одновременно испытываемых пожарных кранов на водоотдачу"
            placeholder="Введите количество пожарных кранов"
            variant="solo-filled"
          ></v-text-field>
          <!--  -->

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            РЕЗУЛЬТАТЫ ИСПЫТАНИЙ ВНУТРЕННЕГО ПРОТИВОПОЖАРНОГО ВОДОСНАБЖЕНИЯ НА ВОДООТДАЧУ ПО
            "ДИКТУЮЩЕМУ" ПОЖАРНОМУ КРАНУ:
          </v-card-text>

          <div
            v-for="(item, i) in (data.results as resultItem[])"
            :key="item.testNumber"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              :rules="testNumberRules"
              v-model="item.testNumber"
              style="min-width: 450px; padding-left: 20px"
              label="Номер испытаний"
              placeholder="Введите номер испытаний"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="standpipesAndFireHydrantsNumbersRules"
              v-model="item.standpipesAndFireHydrantsNumbers"
              style="min-width: 450px; padding-left: 20px"
              label="Номера стояков - пожарных кранов согласно гидравлической схеме (диаметр)"
              placeholder="Введите номера стояков - пожарных кранов"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="outletDiameterRules"
              v-model="item.outletDiameter"
              style="min-width: 450px; padding-left: 20px"
              label="Диаметр выходного отверстия, мм"
              suffix="мм"
              placeholder="Введите диаметр выходного отверстия"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="hoseLineLengthRules"
              v-model="item.hoseLineLength"
              style="min-width: 450px; padding-left: 20px"
              label="Длина рукавной линии, м"
              suffix="м"
              placeholder="Введите длину рукавной линии"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="measuredPressureRules"
              v-model="item.measuredPressure"
              style="min-width: 450px; padding-left: 20px"
              label="Давление, МПа (измеренное)"
              suffix="Мпа"
              placeholder="Введите измеренное давление"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="requiredPressureRules"
              v-model="item.requiredPressure"
              style="min-width: 450px; padding-left: 20px"
              label="Давление, МПа (требуемое)"
              suffix="Мпа"
              placeholder="Введите требуемое давление"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="requiredFlowRateRules"
              v-model="item.requiredFlowRate"
              style="min-width: 450px; padding-left: 20px"
              label="Требуемый расход, л/с"
              suffix="л/с"
              placeholder="Введите требуемый расход"
              type="number"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              :rules="requiredJetHeightRules"
              v-model="item.requiredJetHeight"
              style="min-width: 450px; padding-left: 20px"
              label="Требуемая высота компактной части струи, м"
              suffix="м"
              placeholder="Введите требуемую высоту струи"
              type="number"
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

          <v-text-field
            :rules="minWaterFlowRateDictatingValveRules"
            v-model="data.minWaterFlowRateDictatingValve"
            style="min-width: 450px; padding-left: 20px"
            label="Минимальная водоотдача внутреннего противопожарного водоснабжения"
            placeholder="Введите минимальную водоотдачу"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="commonRules"
            v-model="data.inAmount"
            style="min-width: 450px; padding-left: 20px"
            label="В количестве"
            placeholder="Введите количество"
            type="number"
            suffix="шт"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="pressureRequirementRules"
            v-model="data.pressureRequirement"
            style="min-width: 450px; padding-left: 20px"
            label="Давление"
            placeholder="Введите требуемое давление"
            type="number"
            suffix="Мпа"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="flowRateRequirementRules"
            v-model="data.flowRateRequirement"
            style="min-width: 450px; padding-left: 20px"
            label="Расход"
            placeholder="Введите требуемый расход"
            type="number"
            suffix="л/с"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="jetHeightRequirementRules"
            v-model="data.jetHeightRequirement"
            style="min-width: 450px; padding-left: 20px"
            label="Высота компактной части струи"
            placeholder="Введите требуемую высоту струи"
            suffix="м"
            type="number"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="complianceExplanationRules"
            v-model="data.complianceExplanation"
            style="min-width: 450px; padding-left: 20px"
            label="Пояснение о соответствии"
            placeholder="Введите пояснение о соответствии"
            variant="solo-filled"
          ></v-text-field>

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

type resultItem = {
  testNumber: string
  standpipesAndFireHydrantsNumbers: string
  outletDiameter: string
  hoseLineLength: string
  measuredPressure: string
  requiredPressure: string
  requiredFlowRate: string
  requiredJetHeight: string
  testResults: string
}
const cityRules = ref([(v: any) => !!v || 'Город обязателен'])

const data = ref({
  city: '',
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
  testTime: '',
  numbersOfFireHydrantRisers: '',
  numberOfTestedFireValues: '',
  testDate: new Date(),
  results: [],
  hydrantType: '',
  fireHoseType: '',
  fireHoseLength: '',
  fireHoseDiameter: '',
  pumpPressure: '',
  flowRate: '',
  pressure: '',
  simultaneousSprinklers: '',
  minWaterFlowRateDictatingValve: '',
  pressureRequirement: '',
  flowRateRequirement: '',
  jetHeightRequirement: '',
  complianceExplanation: '',
  inAmount: '',
  testConducted: []
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

const firePumpTypeRules = ref([(v: any) => !!v || 'Тип пожарного насоса обязателен'])

const hydrantTypeRules = ref([(v: any) => !!v || 'Тип клапана пожарного крана обязателен'])

const fireHoseTypeRules = ref([(v: any) => !!v || 'Тип ручного пожарного ствола обязателен'])

const fireHoseLengthRules = ref([
  (v: any) => !!v || 'Длина пожарного рукава обязательна',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const fireHoseDiameterRules = ref([
  (v: any) => !!v || 'Диаметр пожарного рукава обязателен',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const pumpPressureRules = ref([
  (v: any) => !!v || 'Напор пожарного насоса при закрытых пожарных кранах обязателен',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const regulatoryComplianceRules = ref([(v: any) => !!v || 'Соответствие требованиям обязательно'])

const flowRateRules = ref([
  (v: any) => !!v || 'Расход пожарного крана обязателен',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const pressureRules = ref([
  (v: any) => !!v || 'Давление пожарного крана обязательно',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const simultaneousSprinklersRules = ref([
  (v: any) => !!v || 'Количество пожарных кранов обязательно',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const timeRules = ref([(v: any) => !!v || 'Время обязательно'])

const testNumberRules = ref([(v: any) => !!v || 'Номер испытаний обязателен'])

const standpipesAndFireHydrantsNumbersRules = ref([
  (v: any) => !!v || 'Номера стояков - пожарных кранов обязательны'
])

const outletDiameterRules = ref([(v: any) => !!v || 'Диаметр выходного отверстия, мм обязателен'])

const hoseLineLengthRules = ref([(v: any) => !!v || 'Длина рукавной линии, м обязательна'])

const measuredPressureRules = ref([(v: any) => !!v || 'Давление, МПа (измеренное) обязательно'])

const requiredPressureRules = ref([(v: any) => !!v || 'Давление, МПа (требуемое) обязательно'])

const requiredFlowRateRules = ref([(v: any) => !!v || 'Требуемый расход, л/с обязателен'])

const requiredJetHeightRules = ref([
  (v: any) => !!v || 'Требуемая высота компактной части струи, м обязательна'
])

const testResultsRules = ref([(v: any) => !!v || 'Результаты испытаний обязательны'])

const testConductedRules = ref([(v: any) => !!v || 'Поле "Испытание провели" обязательны'])

const minWaterFlowRateDictatingValveRules = ref([
  (v: any) => !!v || 'Минимальная водоотдача обязательна'
])

const pressureRequirementRules = ref([(v: any) => !!v || 'Давление обязательно'])

const flowRateRequirementRules = ref([(v: any) => !!v || 'Расход обязателен'])

const jetHeightRequirementRules = ref([
  (v: any) => !!v || 'Высота компактной части струи обязательна'
])

const complianceExplanationRules = ref([(v: any) => !!v || 'Пояснение о соответствии обязательно'])

const DOCUMENT_KEY = 'Протокол испытаний внутреннего противопожарного водоснабжения на водоотдачу'
const documentsStore = useDocumentsStore()

const createNewRowOfResults = () => {
  data.value.results.push({
    testNumber: '',
    standpipesAndFireHydrantsNumbers: '',
    outletDiameter: '',
    hoseLineLength: '',
    measuredPressure: '',
    requiredPressure: '',
    requiredFlowRate: '',
    requiredJetHeight: '',
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
