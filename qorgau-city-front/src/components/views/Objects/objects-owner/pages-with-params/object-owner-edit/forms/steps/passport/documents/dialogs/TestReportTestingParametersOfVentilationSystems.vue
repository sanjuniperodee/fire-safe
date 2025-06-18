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
            ДАТА ИСПЫТАНИЙ:
          </v-card-text>

          <v-date-picker
            :max="new Date()"
            v-model="data.testDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>
          <v-text-field
            v-model="data.organizationName"
            :rules="commonRules"
            label="Наименование организации проводившей испытание"
            placeholder="Введите наименование организации проводившей испытание"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.organizationAddress"
            :rules="commonRules"
            label="Адрес организации проводившей испытание"
            placeholder="Введите адрес организации проводившей испытание"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.customerName"
            :rules="commonRules"
            label="Наименование Заказчика"
            placeholder="Введите наименование Заказчика"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.objectAddress"
            :rules="commonRules"
            label="Адрес объекта"
            placeholder="Введите адрес объекта"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.basisForTesting"
            :rules="commonRules"
            label="Основание для проведения испытания"
            placeholder="Введите основание для проведения испытания"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.testingMethod"
            :rules="commonRules"
            label="Метод испытаний"
            placeholder="Введите метод испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>
          <!--  -->

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Основные результаты:
          </v-card-text>

          <div
            v-for="(item, i) in (data.mainResults as mainResultItem[])"
            :key="i + 'mainResultItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              v-model="item.systemType"
              :rules="commonRules"
              label="Тип системы"
              placeholder="Введите тип системы"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.systemName"
              :rules="commonRules"
              label="Наименование системы"
              placeholder="Введите наименование системы"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.fact"
              :rules="commonRules"
              label="Факт."
              placeholder="Введите факт."
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.projectFlowRate"
              :rules="commonRules"
              label="Проектный расход, м3/ч"
              placeholder="Введите проектный расход, м3/ч"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.actualFlowRate"
              :rules="commonRules"
              label="Фактический расход, м3/ч"
              placeholder="Введите фактический расход, м3/ч"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.compliancePercentage"
              :rules="commonRules"
              label="Величина соответствия, %"
              placeholder="Введите величину соответствия, %"
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

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Результаты испытания системы приточной противодымной вентиляции:
          </v-card-text>
          <div
            v-for="(item, i) in (data.testResults as testResultItem[])"
            :key="i + 'testResultItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-text-field
              v-model="item.ventilationSystemType"
              :rules="commonRules"
              label="Тип системы"
              placeholder="Введите тип системы"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationSystemName"
              :rules="commonRules"
              label="Наименование"
              placeholder="Введите наименование"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationFact"
              :rules="commonRules"
              label="Факт."
              placeholder="Введите факт."
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationProjectPressure"
              :rules="commonRules"
              label="Проектное давление, Па"
              placeholder="Введите проектное давление, Па"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationProjectSpeed"
              :rules="commonRules"
              label="Проектная скорость, м/с"
              placeholder="Введите проектную скорость, м/с"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationActualPressure"
              :rules="commonRules"
              label="Фактическое давление, Па"
              placeholder="Введите фактическое давление, Па"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationActualSpeed"
              :rules="commonRules"
              label="Фактическая скорость, м/с"
              placeholder="Введите фактическую скорость, м/с"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.ventilationConclusion"
              :rules="commonRules"
              label="Заключение  о соответствии"
              placeholder="Введите заключение о соответствии"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createNewRowOfTestResults()"
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

const data = ref({
  testDate: new Date(),
  organizationName: '',
  organizationAddress: '',
  customerName: '',
  objectAddress: '',
  basisForTesting: '',
  testingMethod: '',
  mainResults: [],
  testResults: [],
  smokeGasPermeability: '',
  testingResults: ''
})

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

type mainResultItem = {
  systemType: string
  systemName: string
  fact: string
  projectFlowRate: string
  actualFlowRate: string
  compliancePercentage: string
}

type testResultItem = {
  ventilationSystemType: string
  ventilationSystemName: string
  ventilationFact: string
  ventilationProjectPressure: string
  ventilationProjectSpeed: string
  ventilationActualPressure: string
  ventilationActualSpeed: string
  ventilationConclusion: string
}

const DOCUMENT_KEY = 'Протокол испытаний испытание параметров систем вентиляции'
const documentsStore = useDocumentsStore()

const createNewRowOfResults = () => {
  data.value.mainResults.push({
    systemType: '',
    systemName: '',
    fact: '',
    projectFlowRate: '',
    actualFlowRate: '',
    compliancePercentage: ''
  } as never)
}

const createNewRowOfTestResults = () => {
  data.value.testResults.push({
    ventilationSystemType: '',
    ventilationSystemName: '',
    ventilationFact: '',
    ventilationProjectPressure: '',
    ventilationProjectSpeed: '',
    ventilationActualPressure: '',
    ventilationActualSpeed: '',
    ventilationConclusion: ''
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
