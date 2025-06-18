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

          <v-card-text style="font-weight: 700; font-size: 16px; margin-top: 20px">
            Наименования организации проводившей испытания
          </v-card-text>

          <v-text-field
            v-model="data.testingOrganizationName.BIN"
            label="БИН"
            type="number"
            placeholder="Введите БИН организации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.testingOrganizationName.organizationName"
            label="Наименование организации"
            placeholder="Введите наименование организации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 16px; margin-top: 20px">
            Наименования организации - заказчика
          </v-card-text>

          <v-text-field
            v-model="data.customerOrganizationName.BIN"
            label="БИН"
            type="number"
            placeholder="Введите БИН организации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.customerOrganizationName.organizationName"
            label="Наименование организации"
            placeholder="Введите наименование организации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.testBasis"
            label="Основание для проведения испытаний"
            placeholder="Введите основание для проведения испытаний"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 16px; margin-top: 20px">
            Наименование (вид) огнезащитного средства
          </v-card-text>
          <v-text-field
            v-model="data.fireProtectiveAgent.manufacturerDetails"
            label="Сведения об изготовителе"
            placeholder="Введите сведения об изготовителе"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.fireProtectiveAgent.trademark"
            label="Товарный знак"
            placeholder="Введите товарный знак"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.fireProtectiveAgent.fireProtectionMarking"
            label="Маркировка огнезащитного средства"
            placeholder="Введите маркировку огнезащитного средства"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.normativeDocumentation"
            label="Наименование нормативной и (или) технической документации"
            placeholder="Введите наименование документации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.batchNumber"
            label="Номер партии"
            placeholder="Введите номер партии"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Дата изготовления партии:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.batchDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 16px; margin-top: 20px">
            Наименование организации, проводившей огнезащитную обработку
          </v-card-text>

          <v-text-field
            v-model="data.fireProtectionOrganizationName.BIN"
            label="БИН"
            type="number"
            placeholder="Введите БИН организации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.fireProtectionOrganizationName.organizationName"
            label="Наименование организации"
            placeholder="Введите наименование организации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.fireProtectionObjectType"
            label="Тип конструкции объекта огнезащиты"
            placeholder="Введите тип конструкции объекта огнезащиты"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.fireProtectionObjectCondition"
            label="Состояние объекта огнезащиты (отобранных образцов)"
            placeholder="Введите состояние объекта огнезащиты"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.treatmentMethod"
            label="Способ обработки"
            placeholder="Введите способ обработки"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.treatmentArea"
            label="Площадь обработки"
            placeholder="Введите площадь обработки"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.operatingConditions"
            label="Условия эксплуатации"
            placeholder="Введите условия эксплуатации"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.testingMethod"
            label="Метод проведения испытаний"
            placeholder="Введите метод проведения испытаний"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-text-field
            v-model="data.testConditions"
            label="Условия проведения испытаний"
            placeholder="Введите условия проведения испытаний"
            style="min-width: 450px; padding-left: 20px"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Результаты испытаний:
          </v-card-text>

          <div
            v-for="(item, i) in (data.results as resultItem[])"
            :key="i + 'resultItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Номер образца {{ i + 1 }}
            </v-card-text>
            <v-text-field
              v-model="item.sampleNumber"
              label="Номер образца"
              placeholder="Введите номер образца"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              v-model="item.sampleCollectionLocation"
              label="Место отбора образца"
              placeholder="Введите место отбора образца"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              v-model="item.testResults"
              label="Результаты испытаний"
              placeholder="Введите результаты испытаний"
              style="min-width: 450px; padding-left: 20px"
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
            :rules="commonRules"
            style="min-width: 450px; padding-left: 20px"
            label="Заключение"
            placeholder="Введите заключение"
            variant="solo-filled"
          ></v-textarea>

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

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  form.value?.reset()
}

const downloadPdf = () => {
  console.log('downloadPdf')
}

type resultItem = {
  sampleNumber: string
  sampleCollectionLocation: string
  testResults: string
}

const data = ref({
  testDate: new Date(),
  testingOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  customerOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  testBasis: '',
  fireProtectiveAgent: {
    manufacturerDetails: '',
    trademark: '',
    fireProtectionMarking: ''
  },
  normativeDocumentation: '',
  batchNumber: '',
  batchDate: new Date(),
  fireProtectionOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  fireProtectionObjectType: '',
  fireProtectionObjectCondition: '',
  treatmentMethod: '',
  treatmentArea: '',
  operatingConditions: '',
  testingMethod: '',
  testConditions: '',
  results: [],
  testConducted: [],
  conclusion: ''
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

const jobTitleRules = ref([(v: any) => !!v || 'Должность обязательна'])

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])
const organizationNameRules = ref([(v: any) => !!v || 'Наименование организации обязательно'])

const BINRules = ref([
  (v: any) => !!v || 'БИН обязателен',
  (v: any) => !isNaN(Number(v)) || 'БИН должен быть числом',
  (v: any) => parseInt(v.length) === 12 || 'Длина БИН должна быть 12 цифр'
])

const DOCUMENT_KEY =
  'Форма протокола контрольных испытаний по определению качества обработки объекта огнезащитной по деревянным конструкциям'
const documentsStore = useDocumentsStore()

const createNewRowOfResults = () => {
  data.value.results.push({
    sampleNumber: '',
    sampleCollectionLocation: '',
    testResults: ''
  } as never)
}

type TestConductedMember = {
  IIN: ''
  name: ''
  jobTitle: ''
  BIN: ''
  organizationName: ''
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
        //@ts-expect-error
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
