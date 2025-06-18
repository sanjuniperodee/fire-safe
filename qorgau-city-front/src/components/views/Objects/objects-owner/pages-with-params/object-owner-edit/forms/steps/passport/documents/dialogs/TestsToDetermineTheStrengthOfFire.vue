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
            v-model="data.customerName"
            :rules="commonRules"
            label="Наименование заказчика"
            placeholder="Введите наименование заказчика"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.customerAddress"
            :rules="commonRules"
            label="Адрес заказчика"
            placeholder="Введите адрес заказчика"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.testingBasis"
            :rules="commonRules"
            label="Основание для проведения испытаний"
            placeholder="Введите основание для проведения испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.documentationName"
            :rules="commonRules"
            label="Наименование нормативной и (или) технической документации"
            placeholder="Введите наименование нормативной и (или) технической документации"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.objectCharacteristics"
            :rules="commonRules"
            label="Характеристика испытываемого объекта"
            placeholder="Введите характеристику испытываемого объекта"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.testingConditions"
            :rules="commonRules"
            label="Условия проведения испытаний"
            placeholder="Введите условия проведения испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.testingEquipment"
            :rules="commonRules"
            label="Средства испытаний"
            placeholder="Введите средства испытаний"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-text-field
            v-model="data.stairVisualInspection"
            :rules="commonRules"
            label="Визуальный осмотр лестницы"
            placeholder="Введите результат визуального осмотра лестницы"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Результаты испытаний:
          </v-card-text>

          <div
            v-for="(item, i) in (data.testResults as testResultItem[])"
            :key="i + 'testResultItem'"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              v-model="item.testElementName"
              :rules="commonRules"
              label="Наименование испытываемого элемента конструкции"
              placeholder="Введите наименование испытываемого элемента конструкции"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.numberOfTestPoints"
              :rules="commonRules"
              label="Кол-во испытываемых точек"
              placeholder="Введите количество испытываемых точек"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.loadInKiloNewtons"
              :rules="commonRules"
              label="Нагрузка, кН"
              placeholder="Введите нагрузку в кН"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.testingResults"
              :rules="commonRules"
              label="Результаты испытаний"
              placeholder="Введите результаты испытаний"
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
            Выводы по результатам испытаний:
          </v-card-text>
          <v-text-field
            v-model="data.testingResults"
            :rules="commonRules"
            label="Выводы по результатам испытания"
            placeholder="Введите выводы по результатам испытания"
            type="text"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-text-field>
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

type testResultItem = {
  testElementName: string
  numberOfTestPoints: string
  loadInKiloNewtons: string
  testingResults: string
}

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const data = ref({
  testDate: new Date(),
  organizationName: '',
  customerName: '',
  customerAddress: '',
  testingBasis: '',
  documentationName: '',
  objectCharacteristics: '',
  testingConditions: '',
  testingEquipment: '',
  stairVisualInspection: '',
  testResults: [],
  testingResults: ''
})

const DOCUMENT_KEY =
  'Испытания по определению прочностей пожарных наружных стационарных лестниц и ограждения кровли'
const documentsStore = useDocumentsStore()

const createNewRowOfResults = () => {
  data.value.testResults.push({
    testElementName: '',
    numberOfTestPoints: '',
    loadInKiloNewtons: '',
    testingResults: ''
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
