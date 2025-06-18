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
            Дата проведения испытания:
          </v-card-text>
          <v-date-picker
            :max="new Date()"
            v-model="data.testDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-text-field
            v-model="data.laboratoryName"
            :rules="commonRules"
            label="Наименование лаборатории"
            placeholder="Введите наименование лаборатории"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.laboratoryAddress"
            :rules="commonRules"
            label="Адрес лаборатории"
            placeholder="Введите адрес лаборатории"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.clientName"
            :rules="commonRules"
            label="Наименование заказчика"
            placeholder="Введите наименование заказчика"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.clientAddress"
            :rules="commonRules"
            label="Адрес заказчика"
            placeholder="Введите адрес заказчика"
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
            v-model="data.testBasis"
            :rules="commonRules"
            label="Основание для проведения испытаний"
            placeholder="Введите основание для проведения испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.normativeDocumentation"
            :rules="commonRules"
            label="Наименование нормативной и (или) технической документации"
            placeholder="Введите наименование документации"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наименование организации, проводившей огнезащитную обработку
          </v-card-text>

          <v-text-field
            v-model="data.fireProtectionOrganizationName.BIN"
            :rules="commonRules"
            label="БИН"
            type="number"
            style="min-width: 450px; padding-left: 20px"
            variant="outlined"
            placeholder="Введите БИН организации"
          ></v-text-field>

          <v-text-field
            v-model="data.fireProtectionOrganizationName.organizationName"
            :rules="commonRules"
            label="Наименование организации"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="outlined"
            placeholder="Введите наименование организации"
          ></v-text-field>

          <v-text-field
            v-model="data.materialName"
            :rules="commonRules"
            label="Наименование материала"
            placeholder="Введите наименование материала"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.materialCharacteristics"
            :rules="commonRules"
            label="Характеристики материала"
            placeholder="Введите характеристики материала"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.surfaceDensity"
            :rules="commonRules"
            label="Поверхностная плотность, г/м^2"
            placeholder="Введите поверхностную плотность, г/м^2"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.measuringDevice"
            :rules="commonRules"
            label="Прибор для измерения"
            placeholder="Введите прибор для измерения"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Экспериментальные данные:
          </v-card-text>
          <div
            v-for="(item, i) in (data.results as resultItem[])"
            :key="i + 'resultItem'"
          >
            <v-text-field
              v-model="item.registeredParameters"
              :rules="commonRules"
              label="Регистрируемые параметры"
              placeholder="Введите регистрируемые параметры"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <template
              :key="`alongBase${num}`"
              v-for="num in [1, 2, 3, 4, 5, 6, 7]"
            >
              <v-text-field
                v-model="item[`alongBase${num}` as keyof resultItem]"
                :rules="commonRules"
                :label="`Вдоль основы ${num}`"
                :placeholder="`Введите значение Вдоль основы ${num}`"
                type="text"
                style="min-width: 450px; padding-left: 20px"
                variant="solo-filled"
              ></v-text-field>
            </template>

            <v-text-field
              v-model="item.resultingParametersAlongBase"
              :rules="commonRules"
              label="Вдоль основы результирующие параметры"
              placeholder="Введите результирующие параметры вдоль основы"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <template
              :key="`alongBase${num}`"
              v-for="num in [1, 2, 3, 4, 5, 6, 7]"
            >
              <v-text-field
                v-model="item[`alongWeft${num}` as keyof resultItem]"
                :rules="commonRules"
                :label="`Вдоль утка ${num}`"
                :placeholder="`Введите значение Вдоль утка ${num}`"
                type="text"
                style="min-width: 450px; padding-left: 20px"
                variant="solo-filled"
              ></v-text-field>
            </template>

            <v-text-field
              v-model="item.resultingParametersAlongWeft"
              :rules="commonRules"
              label="Вдоль утка результирующие параметры"
              placeholder="Введите результирующие параметры вдоль утка"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createMeasurementResults()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
          >

          <v-textarea
            v-model="data.note"
            :rules="commonRules"
            style="min-width: 450px; padding-left: 20px"
            label="Примечание"
            placeholder="Введите примечание"
            variant="solo-filled"
          ></v-textarea>
          <v-textarea
            v-model="data.conclusion"
            :rules="commonRules"
            style="min-width: 450px; padding-left: 20px"
            label="Заключение"
            placeholder="Введите заключение"
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

const downloadPdf = () => {
  console.log('downloadPdf')
}

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
// // @ts-expect-error already in the documents
// import { runFont } from '@/helpers/jsPdfFont.js'

// import { jsPDF } from "jspdf";
// import { formatDateWithoutTime } from '@/helpers/formatTime';

type resultItem = {
  registeredParameters: string
  alongBase1: string
  alongBase2: string
  alongBase3: string
  alongBase4: string
  alongBase5: string
  alongBase6: string
  alongBase7: string
  resultingParametersAlongBase: string
  alongWeft1: string
  alongWeft2: string
  alongWeft3: string
  alongWeft4: string
  alongWeft5: string
  alongWeft6: string
  alongWeft7: string
  resultingParametersAlongWeft: string
}

const data = ref({
  testDate: new Date(),
  laboratoryName: '',
  laboratoryAddress: '',
  clientName: '',
  clientAddress: '',
  objectAddress: '',
  testBasis: '',
  normativeDocumentation: '',
  fireProtectionOrganizationName: {
    BIN: '',
    organizationName: ''
  },
  materialName: '',
  materialCharacteristics: '',
  surfaceDensity: '',
  measuringDevice: '',
  results: [],
  note: '',
  conclusion: ''
})

const DOCUMENT_KEY = 'ПРОТОКОЛ ИСПЫТАНИЙ метод испытания на воспламеняемость и классификация'
const documentsStore = useDocumentsStore()
const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const createMeasurementResults = () => {
  data.value.results.push({
    registeredParameters: '',
    alongBase1: '',
    alongBase2: '',
    alongBase3: '',
    alongBase4: '',
    alongBase5: '',
    alongBase6: '',
    alongBase7: '',
    resultingParametersAlongBase: '',
    alongWeft1: '',
    alongWeft2: '',
    alongWeft3: '',
    alongWeft4: '',
    alongWeft5: '',
    alongWeft6: '',
    alongWeft7: '',
    resultingParametersAlongWeft: ''
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
