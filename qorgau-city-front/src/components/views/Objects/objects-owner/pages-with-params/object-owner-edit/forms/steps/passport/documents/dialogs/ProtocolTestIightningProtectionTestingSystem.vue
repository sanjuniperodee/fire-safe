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
          <v-card-text
            style="
              font-weight: 700;
              font-size: 16px;
              font-family: 'Noto Sans', sans-serif;
              margin-top: 20px;
            "
          >
            Категория защиты:
          </v-card-text>

          <v-select
            v-model="data.defenceCategory"
            :items="['1', '2', '3']"
            :rules="commonRules"
            label="Выбрать категорию защиты"
            style="min-width: 450px; padding-left: 20px"
            variant="solo-filled"
          ></v-select>
          <div
            v-for="(item, i) in (data.results as ListRowType[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>
            <v-text-field
              v-model="item.lightningRodType"
              :rules="commonRules"
              label="Тип молниеприемника"
              placeholder="Введите тип молниеприемника"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.numberOfDownconductors"
              :rules="commonRules"
              label="Количество токоотвода"
              placeholder="Введите количество токоотвода"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-select
              v-model="item.groundingType"
              :items="['Совмещенное', 'Отдельное']"
              :rules="commonRules"
              label="Выбрать тип ЗУ"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-select>

            <v-text-field
              v-model="item.conductorAirSection"
              :rules="commonRules"
              label="Сечение (диаметр) токоотводов в воздухе"
              placeholder="Введите сечение (диаметр) токоотводов в воздухе"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.conductorGroundSection"
              :rules="commonRules"
              label="Сечение (диаметр) токоотводов в земле"
              placeholder="Введите сечение (диаметр) токоотводов в земле"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.weldedConnectionsCondition"
              :rules="commonRules"
              label="Состояние сварных соединений"
              placeholder="Введите состояние сварных соединений"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.transitionResistance"
              :rules="commonRules"
              label="Переходное сопротивление болтовых соединений"
              placeholder="Введите переходное сопротивление болтовых соединений"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.groundingResistance"
              :rules="commonRules"
              label="Сопротивление ЗУ"
              placeholder="Введите сопротивление ЗУ"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.note"
              :rules="commonRules"
              label="Примечание"
              placeholder="Введите примечание"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

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
              label="Зав. №"
              placeholder="Введите зав. №"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.range"
              :rules="commonRules"
              label="Диапазон"
              placeholder="Введите диапазон"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>

            <v-text-field
              v-model="item.accuracy"
              :rules="commonRules"
              label="Погрешность"
              placeholder="Введите погрешность"
              type="text"
              style="min-width: 450px; padding-left: 20px"
              variant="solo-filled"
            ></v-text-field>
            <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
              Дата проверки:
            </v-card-text>
            <v-date-picker
              :max="new Date()"
              v-model="item.checkDate"
              style="margin-left: 20px"
              show-adjacent-months
              color="#f57c01"
            ></v-date-picker>
          </div>
          <v-btn
            color="#2297b6"
            prepend-icon="mdi-plus"
            variant="elevated"
            @click="() => createListRow()"
            style="text-transform: none; margin-left: 20px"
            >Добавить запись</v-btn
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

type ListRowType = {
  lightningRodType: string

  // Количество токоотвода
  numberOfDownconductors: string

  // Тип ЗУ (совмещенное, отдельное)
  groundingType: string

  // Сечение (диаметр) токоотводов в воздухе
  conductorAirSection: string

  // Сечение (диаметр) токоотводов в земле
  conductorGroundSection: string

  // Состояние сварных соединений
  weldedConnectionsCondition: string

  // Переходное сопротивление болтовых соединений
  transitionResistance: string

  // Сопротивление ЗУ
  groundingResistance: string

  // Примечание
  note: string

  // Наименование
  name: string

  // Тип
  type: string

  // Зав. №
  serialNumber: string

  // Диапазон
  range: string

  // Погрешность
  accuracy: string

  // Дата проверки
  checkDate: Date
}

const data = ref({
  defenceCategory: '',
  results: []
})

const createListRow = () => {
  data.value.results.push({
    lightningRodType: '',
    numberOfDownconductors: '',
    groundingType: '',
    conductorAirSection: '',
    conductorGroundSection: '',
    weldedConnectionsCondition: '',
    transitionResistance: '',
    groundingResistance: '',
    note: '',
    name: '',
    type: '',
    serialNumber: '',
    range: '',
    accuracy: '',
    checkDate: new Date()
  } as never)
}

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const DOCUMENT_KEY = 'ПРОТОКОЛ ИСПЫТАНИЙ проверки систем молниезащиты'
const documentsStore = useDocumentsStore()

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
