<template>
  <v-dialog
    v-model="documentsStore.dialogs[DOCUMENT_KEY]"
    width="auto"
    min-width="800"
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
            Наименование объекта:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.objectName.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите номер BIN"
            :counter="12"
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

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%"> Выдан: </v-card-text>
          <v-text-field
            :rules="IINRules"
            v-model="data.issuedMember.IIN"
            style="min-width: 450px; padding-left: 20px"
            label="ИИН"
            placeholder="Введите ваш ИИН"
            :counter="12"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="nameRules"
            v-model="data.issuedMember.name"
            style="min-width: 450px; padding-left: 20px"
            label="ФИО"
            placeholder="Введите ваше ФИО"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="jobTitleRules"
            v-model="data.issuedMember.jobTitle"
            style="min-width: 450px; padding-left: 20px"
            label="Должность"
            placeholder="Введите вашу должность"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="BINRules"
            v-model="data.issuedMember.BIN"
            style="min-width: 450px; padding-left: 20px"
            label="БИН"
            placeholder="Введите ваш БИН"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.issuedMember.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации"
            placeholder="Введите ваше наименование организации"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Разрешено производство:
          </v-card-text>
          <v-text-field
            :rules="fireWorksNameRules"
            v-model="data.fireWorksName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование огневых работ"
            placeholder="Введите наименование огневых работ"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="locationRules"
            v-model="data.location"
            style="min-width: 450px; padding-left: 20px"
            label="Место проведения"
            placeholder="Введите место проведения"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наименование мероприятий:
          </v-card-text>
          <v-text-field
            :rules="eventNamesRules"
            v-model="data.eventNames"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование мероприятий"
            placeholder="Введите наименование мероприятий"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Разрешение действительно с:
          </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.permissionValidFromTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>
          <v-date-picker
            :max="new Date()"
            v-model="data.permissionValidFromDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%"> До: </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.permissionValidToTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>
          <v-date-picker
            :max="new Date()"
            v-model="data.permissionValidToDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Разрешение продлено с:
          </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.extendedFromTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>
          <v-date-picker
            :max="new Date()"
            v-model="data.extendedFromDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%"> До: </v-card-text>
          <v-text-field
            :rules="timeRules"
            type="time"
            step="1"
            v-model="data.extendedToTime"
            style="min-width: 450px; padding-left: 20px"
            label="Время"
            placeholder="Введите время"
            variant="solo-filled"
          ></v-text-field>
          <v-date-picker
            :max="new Date()"
            v-model="data.extendedToDate"
            style="margin-left: 20px"
            show-adjacent-months
            color="#f57c01"
          ></v-date-picker>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Проводящий работы:
          </v-card-text>
          <v-text-field
            :rules="IINRules"
            v-model="data.carryOutWorker.IIN"
            style="min-width: 450px; padding-left: 20px"
            label="ИИН"
            placeholder="Введите ваш ИИН"
            :counter="12"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="nameRules"
            v-model="data.carryOutWorker.name"
            style="min-width: 450px; padding-left: 20px"
            label="ФИО"
            placeholder="Введите ваше ФИО"
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

const data = ref({
  objectName: {
    BIN: '',
    objectName: ''
  },
  issuedMember: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  fireWorksName: '',
  location: '',
  eventNames: '',
  permissionValidFromTime: '',
  permissionValidFromDate: new Date(),
  permissionValidToTime: '',
  permissionValidToDate: new Date(),
  extendedFromTime: '',
  extendedFromDate: new Date(),
  extendedToTime: '',
  extendedToDate: new Date(),
  carryOutWorker: {
    IIN: '',
    name: ''
  }
})

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

const fireWorksNameRules = ref([(v: any) => !!v || 'Наименование огневых работ обязательно'])

const locationRules = ref([(v: any) => !!v || 'Место проведения обязательно'])

const eventNamesRules = ref([(v: any) => !!v || 'Наименование мероприятий обязательно'])

const timeRules = ref([(v: any) => !!v || 'Время обязательно'])

const DOCUMENT_KEY = 'РАЗРЕШЕНИЕ на производство огневых работ'
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
