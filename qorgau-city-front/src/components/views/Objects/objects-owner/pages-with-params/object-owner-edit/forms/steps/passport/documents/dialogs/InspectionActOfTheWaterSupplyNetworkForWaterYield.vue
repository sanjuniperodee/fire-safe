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
            @click="() => createNewCommissionMember()"
            style="text-transform: none; margin-left: 20px"
            >Добавить</v-btn
          >

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Вид водопроводной сети:
          </v-card-text>
          <v-text-field
            v-model="data.waterSupplyNetworkType"
            :rules="waterSupplyNetworkTypeRules"
            style="min-width: 450px; padding-left: 20px"
            label="Вид водопроводной сети"
            placeholder="Введите вид водопроводной сети"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Диаметр:
          </v-card-text>
          <v-text-field
            v-model="data.diameter"
            :rules="diameterRules"
            style="min-width: 450px; padding-left: 20px"
            type="number"
            suffix="мм"
            label="Диаметр"
            placeholder="Введите диаметр"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Давление в сети - атмосфера:
          </v-card-text>
          <v-text-field
            v-model="data.networkPressureAtmosphere"
            :rules="networkPressureAtmosphereRules"
            style="min-width: 450px; padding-left: 20px"
            label="Давление в сети - атмосфера"
            type="number"
            placeholder="Введите давление в сети - атмосфера"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Типоразмер установленных пожарных гидрантов:
          </v-card-text>
          <v-text-field
            v-model="data.typeAndSizeOfInstalledFireHydrants"
            :rules="typeAndSizeOfInstalledFireHydrantsRules"
            style="min-width: 450px; padding-left: 20px"
            label="Типоразмер установленных пожарных гидрантов"
            placeholder="Введите типоразмер установленных пожарных гидрантов"
            variant="solo-filled"
          ></v-text-field>

          <v-card-text style="font-weight: 700; font-size: 24px; width: 100%">
            Способ обследований на водоотдачу:
          </v-card-text>
          <v-text-field
            v-model="data.waterYieldInspectionMethod"
            :rules="waterYieldInspectionMethodRules"
            style="min-width: 450px; padding-left: 20px"
            label="Способ обследований на водоотдачу"
            placeholder="Введите способ обследований на водоотдачу"
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
          <v-select
            v-model="data.commissionConclusion"
            :rules="commissionConclusionRules"
            label="Выберите заключение комиссии"
            style="min-width: 450px; padding-left: 20px"
            :items="[
              'Дальнейшая эксплуатация существующих систем и установок пожарной автоматики возможна/невозможна или необходимо выполнить монтаж новых систем и установок',
              'Требуется ремонт отдельных технических средств систем и установок пожарной автоматики',
              'Необходимо продлить эксплуатацию систем и установок пожарной автоматики, с указанием срока следующего освидетельствования'
            ]"
            variant="solo-filled"
          ></v-select>
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
          @click="generateDocument"
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
  chairmanOfCommision: {
    IIN: '',
    name: '',
    jobTitle: '',
    BIN: '',
    organizationName: ''
  },
  commissionMembers: [],
  waterSupplyNetworkType: '',
  diameter: '',
  networkPressureAtmosphere: '',
  typeAndSizeOfInstalledFireHydrants: '',
  waterYieldInspectionMethod: '',
  actualWaterYield: '',
  requiredWaterYield: '',
  commissionConclusion: ''
})

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

const cityRules = ref([(v: any) => !!v || 'Город обязателен'])

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

const waterSupplyNetworkTypeRules = ref([(v: any) => !!v || 'Вид водопроводной сети обязателен'])

const diameterRules = ref([
  (v: any) => !!v || 'Диаметр обязателен',
  (v: any) => !isNaN(Number(v)) || 'Диаметр должен быть числом'
])

const networkPressureAtmosphereRules = ref([
  (v: any) => !!v || 'Давление в сети - атмосфера обязательно'
])

const typeAndSizeOfInstalledFireHydrantsRules = ref([
  (v: any) => !!v || 'Типоразмер установленных пожарных гидрантов обязателен'
])

const waterYieldInspectionMethodRules = ref([
  (v: any) => !!v || 'Способ обследований на водоотдачу обязателен'
])

const actualWaterYieldRules = ref([
  (v: any) => !!v || 'Фактическая водоотдача обязательна',
  (v: any) => !isNaN(Number(v)) || 'Фактическая водоотдача должна быть числом'
])

const requiredWaterYieldRules = ref([
  (v: any) => !!v || 'Требуемая водоотдача обязательна',
  (v: any) => !isNaN(Number(v)) || 'Требуемая водоотдача должна быть числом'
])

const commissionConclusionRules = ref([(v: any) => !!v || 'Выберите заключение комиссии'])

const DOCUMENT_KEY = 'АКТ ОБСЛЕДОВАНИЯ водопроводной сети на водоотдачу'
const documentsStore = useDocumentsStore()

function generateUniqueId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
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
