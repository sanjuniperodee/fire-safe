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
          <div
            v-for="(item, i) in (data.results as ListRowType[])"
            :key="i"
          >
            <v-card-text style="font-weight: 700; font-size: 18px; width: 100%">
              Запись {{ i + 1 }}
            </v-card-text>

            <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
              № протокола и дата:
            </v-card-text>

            <v-text-field
              v-model="item.protocolNumber"
              :rules="commonRules"
              style="min-width: 450px; padding-left: 20px"
              label="№ протокола"
              placeholder="Введите номер протокола"
              variant="solo-filled"
            ></v-text-field>

            <v-date-picker
              :rules="commonRules"
              :max="new Date()"
              v-model="item.protocolDate"
              style="margin-left: 20px"
              show-adjacent-months
              color="#f57c01"
              label="Дата протокола"
            ></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.customerName"
              label="Наименование заказчика"
              placeholder="Введите наименование владельца объекта"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.objectName"
              label="Наименование объекта"
              placeholder="Введите наименование объекта"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.address"
              label="Адрес объекта"
              placeholder="Введите адрес объекта"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.testingArea"
              label="Область испытания"
              placeholder="Введите область испытания"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.contactPhone"
              label="Контактный телефон"
              placeholder="Введите контактный телефон"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              :rules="emailRules"
              v-model="item.contactEmail"
              label="Электронная почта"
              placeholder="Введите электронную почту"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-text-field
              :rules="commonRules"
              v-model="item.contactPerson"
              label="ФИО контактного лица"
              placeholder="Введите ФИО контактного лица"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>

            <v-date-picker
              :max="new Date()"
              v-model="item.nextTestDate"
              style="margin-left: 20px"
              show-adjacent-months
              color="#f57c01"
              label="Дата следующего испытания"
            ></v-date-picker>

            <v-text-field
              :rules="commonRules"
              v-model="item.comment"
              label="Примечание"
              multiline
              placeholder="Введите примечание"
              style="min-width: 450px; padding-left: 20px"
            ></v-text-field>
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

type ListRowType = {
  protocolNumber: string
  protocolDate: Date
  customerName: string
  objectName: string
  address: string
  testingArea: string
  contactPhone: string
  contactEmail: string
  contactPerson: string
  nextTestDate: Date
  comment: string
}

const data = ref({
  results: []
})

const createListRow = () => {
  data.value.results.push({
    protocolNumber: '',
    protocolDate: new Date(),
    customerName: '',
    objectName: '',
    address: '',
    testingArea: '',
    contactPhone: '',
    contactEmail: '',
    contactPerson: '',
    nextTestDate: new Date(),
    comment: ''
  } as never)
}

const emailRules = ref([
  (v: any) => !!v || 'Поле обязательно',
  (v: any) => /.+@.+\..+/.test(v) || 'Введите действительный адрес электронной почты'
])

const commonRules = ref([(v: any) => !!v || 'Поле обязательно'])

const DOCUMENT_KEY = 'Журнал регистрации протоколов испытательной лаборатории'
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
