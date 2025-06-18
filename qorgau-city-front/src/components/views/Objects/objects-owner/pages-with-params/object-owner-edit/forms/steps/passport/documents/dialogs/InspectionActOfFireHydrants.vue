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
            НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ, ПРОВОДИВШЕЙ ОБСЛЕДОВАНИЕ:
          </v-card-text>
          <v-text-field
            :rules="BINRules"
            v-model="data.organizationName.BIN"
            style="min-width: 450px; padding-left: 20px"
            :counter="12"
            label="БИН"
            type="text"
            placeholder="Введите БИН организации"
            variant="solo-filled"
          ></v-text-field>
          <v-text-field
            :rules="organizationNameRules"
            v-model="data.organizationName.organizationName"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование организации"
            type="text"
            placeholder="Введите наименование организации"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Председатель комиссии:
          </v-card-text>
          <v-text-field
            :rules="IINRules"
            v-model="data.chairmanOfCommision.IIN"
            style="min-width: 450px; padding-left: 20px"
            label="ИИН"
            placeholder="Введите ваш ИИН"
            :counter="12"
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
          <v-card-text
            style="font-weight: 700; font-size: 24px; width: 100%; margin: 30px 0 20px 0"
          >
            ХАРАКТЕРИСТИКИ И МАРКИРОВКА ПОЖАРНОГО ГИДРАНТА:
          </v-card-text>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наименование:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.name"
            :rules="fireHydrantNameRules"
            style="min-width: 450px; padding-left: 20px"
            label="Наименование"
            placeholder="Введите наименование"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Адрес изготовителя:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.manufacturerAddress"
            :rules="fireHydrantAddressRules"
            style="min-width: 450px; padding-left: 20px"
            label="Адрес изготовителя"
            placeholder="Введите адрес изготовителя"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Товарный знак изготовителя:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.manufacturerTrademark"
            :rules="fireHydrantTrademarkRules"
            style="min-width: 450px; padding-left: 20px"
            label="Товарный знак изготовителя"
            placeholder="Введите товарный знак изготовителя"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Условное обозначение по системе изготовителя:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.manufacturerDesignation"
            :rules="fireHydrantDesignationRules"
            style="min-width: 450px; padding-left: 20px"
            label="Условное обозначение по системе изготовителя"
            placeholder="Введите условное обозначение по системе изготовителя"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Заводской номер:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.serialNumber"
            :rules="fireHydrantSerialNumberRules"
            style="min-width: 450px; padding-left: 20px"
            label="Заводской номер"
            placeholder="Введите заводской номер"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Высота пожарного гидранта:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.height"
            :rules="fireHydrantHeightRules"
            style="min-width: 450px; padding-left: 20px"
            label="Высота пожарного гидранта"
            type="number"
            suffix="мм"
            placeholder="Введите высоту пожарного гидранта"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Условный проход внутреннего диаметра корпуса:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.internalDiameterPassage"
            :rules="fireHydrantInternalDiameterRules"
            style="min-width: 450px; padding-left: 20px"
            label="Условный проход внутреннего диаметра корпуса"
            placeholder="Введите условный проход внутреннего диаметра корпуса"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Год выпуска:
          </v-card-text>
          <v-text-field
            v-model="data.fireHydrantCharacteristics.manufacturingYear"
            :rules="fireHydrantYearRules"
            style="min-width: 450px; padding-left: 20px"
            label="Год выпуска"
            placeholder="Введите год выпуска"
            variant="solo-filled"
            type="number"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            УСЛОВИЯ ОБСЛЕДОВАНИЯ:
          </v-card-text>
          <v-text-field
            v-model="data.inspectionConditions"
            :rules="inspectionConditionsRules"
            style="min-width: 450px; padding-left: 20px"
            label="Условия обследования"
            placeholder="Введите условия обследования"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ДАННЫЕ О СРЕДСТВАХ ИЗМЕРЕНИЙ И ИСПЫТАТЕЛЬНОМ ОБОРУДОВАНИИ:
          </v-card-text>
          <v-text-field
            v-model="data.measurementAndTestingEquipment"
            :rules="measurementAndTestingEquipmentRules"
            style="min-width: 450px; padding-left: 20px"
            label="Данные о средствах измерений и испытательном оборудовании"
            placeholder="Введите данные о средствах измерений и испытательном оборудовании"
            variant="solo-filled"
          ></v-text-field>
          <!-- Исправность люка и крышки водопроводного колодца, крышек и резьбы ниппеля, верхнего квадрата штанги и корпуса пожарного гидранта -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Исправность люка и крышки водопроводного колодца, крышек и резьбы ниппеля, верхнего
            квадрата штанги и корпуса пожарного гидранта:
          </v-card-text>
          <v-text-field
            v-model="data.coverAndThreadCondition"
            :rules="coverAndThreadConditionRules"
            style="min-width: 450px; padding-left: 20px"
            label="Исправность люка и крышки"
            placeholder="Введите состояние"
            variant="solo-filled"
          ></v-text-field>

          <!-- Работоспособность сливного устройства -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Работоспособность сливного устройства:
          </v-card-text>
          <v-text-field
            v-model="data.drainDeviceFunctionality"
            :rules="drainDeviceFunctionalityRules"
            style="min-width: 450px; padding-left: 20px"
            label="Работоспособность сливного устройства"
            placeholder="Введите состояние"
            variant="solo-filled"
          ></v-text-field>

          <!-- Наличие воды в корпусе пожарного гидранта и в колодце -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Наличие воды в корпусе пожарного гидранта и в колодце:
          </v-card-text>
          <v-text-field
            v-model="data.waterPresence"
            :rules="waterPresenceRules"
            style="min-width: 450px; padding-left: 20px"
            label="Наличие воды"
            placeholder="Введите состояние"
            variant="solo-filled"
          ></v-text-field>

          <!-- Герметичность клапана (задвижки), а также соединений и уплотнений при рабочем давлении -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Герметичность клапана (задвижки), а также соединений и уплотнений при рабочем давлении:
          </v-card-text>
          <v-text-field
            v-model="data.valveSeal"
            :rules="valveSealRules"
            style="min-width: 450px; padding-left: 20px"
            label="Герметичность клапана"
            placeholder="Введите состояние"
            variant="solo-filled"
          ></v-text-field>

          <!-- Работоспособность пожарного гидранта при установке на него пожарной колонки -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Работоспособность пожарного гидранта при установке на него пожарной колонки:
          </v-card-text>
          <v-text-field
            v-model="data.hydrantFunctionality"
            :rules="hydrantFunctionalityRules"
            style="min-width: 450px; padding-left: 20px"
            label="Работоспособность пожарного гидранта"
            placeholder="Введите состояние"
            variant="solo-filled"
          ></v-text-field>

          <!-- Усилия открытия или закрытия пожарного гидранта -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Усилия открытия или закрытия пожарного гидранта:
          </v-card-text>
          <v-text-field
            v-model="data.hydrantOperationEffort"
            :rules="hydrantOperationEffortRules"
            style="min-width: 450px; padding-left: 20px"
            label="Усилия открытия/закрытия"
            placeholder="Введите усилия"
            variant="solo-filled"
          ></v-text-field>

          <!-- Расход воды (водоотдача) в диапазоне давления в водопроводной сети от 0,4 до 0,6 МПа -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Расход воды (водоотдача) в диапазоне давления в водопроводной сети от 0,4 до 0,6 МПа:
          </v-card-text>
          <v-text-field
            v-model="data.waterDischarge"
            :rules="waterDischargeRules"
            style="min-width: 450px; padding-left: 20px"
            label="Расход воды"
            placeholder="Введите расход"
            variant="solo-filled"
          ></v-text-field>

          <!-- Способ обследования на водоотдачу -->
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Способ обследования на водоотдачу:
          </v-card-text>
          <v-text-field
            v-model="data.waterInspectionMethod"
            :rules="waterInspectionMethodRules"
            style="min-width: 450px; padding-left: 20px"
            label="Способ обследования на водоотдачу"
            placeholder="Введите способ обследования"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Фактическая водоотдача:
          </v-card-text>
          <v-text-field
            v-model="data.actualWaterYield"
            :rules="actualWaterYieldRules"
            style="min-width: 450px; padding-left: 20px"
            label="Фактическая водоотдача"
            type="number"
            suffix="л./с"
            placeholder="Введите фактическую водоотдачу"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Требуемая водоотдача:
          </v-card-text>
          <v-text-field
            v-model="data.requiredWaterYield"
            :rules="requiredWaterYieldRules"
            style="min-width: 450px; padding-left: 20px"
            label="Вид требуемая водоотдача"
            type="number"
            suffix="л./с"
            placeholder="Введите требуемую водоотдачу"
            variant="solo-filled"
          ></v-text-field>
          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            ЗАКЛЮЧЕНИЕ КОМИССИИ:
          </v-card-text>
          <v-textarea
            v-model="data.commissionConclusion"
            :rules="commissionConclusionRules"
            style="min-width: 450px; padding-left: 20px"
            placeholder="Введите заключение комиссии"
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
  organizationName: {
    organizationName: '',
    BIN: ''
  },
  chairmanOfCommision: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  commissionMembers: [],
  fireHydrantCharacteristics: {
    name: '',
    manufacturerAddress: '',
    manufacturerTrademark: '',
    manufacturerDesignation: '',
    serialNumber: '',
    height: null,
    internalDiameterPassage: '',
    manufacturingYear: null
  },
  inspectionConditions: '',
  measurementAndTestingEquipment: '',
  coverAndThreadCondition: '',
  drainDeviceFunctionality: '',
  waterPresence: '',
  valveSeal: '',
  hydrantFunctionality: '',
  hydrantOperationEffort: '',
  waterDischarge: '',
  waterInspectionMethod: '',
  actualWaterYield: '',
  requiredWaterYield: '',
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

const fireHydrantNameRules = [(v: any) => !!v || 'Наименование обязательно']

const fireHydrantAddressRules = [(v: any) => !!v || 'Адрес обязателен']

const fireHydrantTrademarkRules = [(v: any) => !!v || 'Товарный знак обязателен']

const fireHydrantDesignationRules = [(v: any) => !!v || 'Условное обозначение обязательно']

const fireHydrantSerialNumberRules = [(v: any) => !!v || 'Заводской номер обязателен']

const fireHydrantHeightRules = [
  (v: any) => !!v || 'Вызота обязательна',
  (v: any) => !isNaN(v) || 'Высота должна быть числом'
]

const fireHydrantInternalDiameterRules = [
  (v: any) => !!v || 'Условный проход внутреннего диаметра обязателен'
]

const fireHydrantYearRules = [
  (v: any) => !!v || 'Год выпуска обязателен',
  (v: any) => !isNaN(v) || 'Год выпуска должен быть числом',
  (v: any) =>
    (v >= 0 && v <= new Date().getFullYear()) || 'Год выпуска должен быть между 0 и текущим годом'
]

const inspectionConditionsRules = [(v: any) => !!v || 'Условия обследования обязательны']

const measurementAndTestingEquipmentRules = [
  (v: any) => !!v || 'Данные о средствах измерений и испытательном оборудовании обязательны'
]

const coverAndThreadConditionRules = [(v: any) => !!v || 'Состояние люка и крышки обязательно']

const drainDeviceFunctionalityRules = [
  (v: any) => !!v || 'Работоспособность сливного устройства обязательна'
]

const waterPresenceRules = [(v: any) => !!v || 'Наличие воды обязательно']

const valveSealRules = [(v: any) => !!v || 'Герметичность клапана обязательна']

const hydrantFunctionalityRules = [
  (v: any) => !!v || 'Работоспособность пожарного гидранта обязательна'
]

const hydrantOperationEffortRules = [(v: any) => !!v || 'Усилия открытия/закрытия обязательны']

const waterDischargeRules = [(v: any) => !!v || 'Расход воды обязателен']

const waterInspectionMethodRules = [
  (v: any) => !!v || 'Способ обследования на водоотдачу обязателен'
]

const actualWaterYieldRules = ref([
  (v: any) => !!v || 'Фактическая водоотдача обязательна',
  (v: any) => !isNaN(Number(v)) || 'Фактическая водоотдача должна быть числом'
])

const requiredWaterYieldRules = ref([
  (v: any) => !!v || 'Требуемая водоотдача обязательна',
  (v: any) => !isNaN(Number(v)) || 'Требуемая водоотдача должна быть числом'
])

const commissionConclusionRules = ref([(v: any) => !!v || 'Выберите заключение комиссии'])

const DOCUMENT_KEY = 'АКТ ОБСЛЕДОВАНИЯ пожарных гидрантов'
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
