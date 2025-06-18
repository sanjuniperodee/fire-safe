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
            Председатель комиссии:
          </v-card-text>
          <v-text-field
            :rules="IINRules"
            v-model="data.chairmanOfCommision.IIN"
            style="min-width: 450px; padding-left: 20px"
            label="ИИН"
            placeholder="Введите ваш ИИН"
            :counter="20"
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
            @click="() => createNewCommissionMember()"
            style="text-transform: none; margin-left: 20px"
            >Добавить</v-btn
          >
          <!--  -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Комиссия произвела испытания внутреннего противопожарного водопровода на водоотдачу:
          </v-card-text>
          <v-text-field
            :rules="numberAndHydrantRules"
            v-model="data.numberAndHydrant"
            style="min-width: 450px; padding-left: 20px"
            label="Номера стояков и пожарных кранов"
            placeholder="Введите номера стояков и пожарных кранов"
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
            :rules="regulatoryComplianceRules"
            v-model="data.regulatoryCompliance"
            style="min-width: 450px; padding-left: 20px"
            label="В соответствии с требованиями нормативных правовых актов, действующих на территории Республики Казахстан"
            placeholder="Введите соответствие требованиям"
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
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            РЕЗУЛЬТАТЫ ИСПЫТАНИЙ:
          </v-card-text>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Потребления воды на хозяйственные нужды от:
          </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.waterConsumptionForHouseholdNeedsFromTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%"> До: </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.waterConsumptionForHouseholdNeedsToTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            :rules="waterFlowRateRules"
            v-model="data.waterFlowRate"
            style="min-width: 450px; padding-left: 20px"
            label="Не менее ____ л/с"
            suffix="л/c"
            type="number"
            placeholder="Введите минимальную водоотдачу"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
            Пояснение о соответствии:
          </v-card-text>
          <v-select
            v-model="data.complianceExplanation"
            :rules="complianceExplanationRules"
            label="Выберите заключение комиссии"
            style="min-width: 450px; padding-left: 20px"
            :items="['Соответствует', 'Не соответствует']"
            variant="solo-filled"
          ></v-select>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ЗАКЛЮЧЕНИЕ ПО РЕЗУЛЬТАТАМ ИСПЫТАНИЙ:
          </v-card-text>
          <v-textarea
            v-model="data.commissionConclusion"
            :rules="commissionConclusionRules"
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

type commisionMember = {
  id: ''
  IIN: ''
  name: ''
  jobTitle: ''
  BIN: ''
  organizationName: ''
}

const data = ref({
  city: '',
  operatingOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  serviceOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  testTime: '',
  testDate: new Date(),

  chairmanOfCommision: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  commissionMembers: [],
  numberAndHydrant: '',
  hydrantType: '',
  fireHoseType: '',
  fireHoseLength: '',
  fireHoseDiameter: '',
  firePumpType: '',
  pumpPressure: '',
  regulatoryCompliance: '',
  flowRate: '',
  pressure: '',
  simultaneousSprinklers: '',
  waterFlowRate: '',
  waterConsumptionForHouseholdNeedsFromTime: '',
  waterConsumptionForHouseholdNeedsToTime: '',
  complianceExplanation: '',
  commissionConclusion: ''
})

const IINRules = ref([
  (v: any) => !!v || 'ИИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'ИИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина ИИН должна быть 12 цифр'
])

const nameRules = ref([
  (v: string) => !!v || 'ФИО обязательно',
  (v: string) => v.split(' ').length === 3 || 'Напишите полное ФИО'
])

const cityRules = ref([(v: any) => !!v || 'Город обязателен'])

const jobTitleRules = ref([(v: any) => !!v || 'Должность обязательна'])

const BINRules = ref([
  (v: any) => !!v || 'БИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'БИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина БИН должна быть 12 цифр'
])

const organizationNameRules = ref([(v: any) => !!v || 'Наименование организации обязательно'])

const timeRules = ref([(v: any) => !!v || 'Время обязательно'])

const commissionCarriedOutTestsRules = ref([(v: any) => !!v || 'Поле обязательно'])

const numberAndHydrantRules = ref([
  (v: any) => !!v || 'Номера стояков и пожарных кранов обязательны'
])

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

const firePumpTypeRules = ref([(v: any) => !!v || 'Тип пожарного насоса обязателен'])

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

const waterFlowRateRules = ref([
  (v: any) => !!v || 'Минимальная водоотдача обязательна',
  (v: any) => typeof v === 'number' || !isNaN(parseFloat(v)) || 'Введите числовое значение'
])

const complianceExplanationRules = ref([(v: any) => !!v || 'Пояснение о соответствии обязательно'])

const commissionConclusionRules = ref([(v: any) => !!v || 'Выберите заключение комиссии'])

const DOCUMENT_KEY =
  'АКТ ИСПЫТАНИЙ систем внутреннего противопожарного водоснабжения на работоспособность'
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
</script>

<style lang="scss" scoped>
.body {
  display: flex;
  flex-direction: column;
  align-items: start !important;
}
</style>
