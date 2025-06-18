<template>
  <CabinetProviderLayout>
    <v-card
      max-width="700px"
      class="mx-auto my-5"
    >
      <v-card-title>
        <span class="headline">Создать объявление</span>
      </v-card-title>
      <v-card-text>
        <v-form
          ref="form"
          v-model="valid"
          lazy-validation
        >
          <v-row>
            <v-col cols="12">
              <v-select
                class="v-select-list"
                v-model="advertisement.category"
                :items="categories"
                label="Категория"
                :rules="[rules.required]"
                required
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="advertisement.title"
                :rules="[rules.required]"
                label="Заголовок"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="advertisement.text"
                :rules="[rules.required]"
                label="Текст"
                required
              ></v-textarea>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="advertisement.min_price"
                :rules="[rules.required, rules.isNumber]"
                label="Мин. цена(тг)"
                type="number"
                required
              ></v-text-field>
            </v-col>
            <v-col
              cols="12"
              sm="6"
            >
              <v-text-field
                v-model="advertisement.max_price"
                :rules="[rules.required, rules.isNumber]"
                label="Макс. цена(тг)"
                type="number"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="advertisement.contract_name"
                :rules="[rules.required]"
                label="Контактное лицо"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="advertisement.phone"
                :rules="[rules.required, rules.isPhone]"
                v-maska:[options]
                type="tel"
                label="Телефон"
                placeholder="+7 (7__) ___-__-__"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="advertisement.address"
                :rules="[rules.required]"
                label="Адрес"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="advertisement.specification"
                :rules="[rules.required]"
                label="Спецификации"
                required
              ></v-textarea>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue darken-1"
          @click="dialog = false"
          >Отменить</v-btn
        >
        <v-btn
          color="blue darken-1"
          @click="submitForm"
          >Создать</v-btn
        >
      </v-card-actions>
    </v-card>
  </CabinetProviderLayout>
</template>

<script setup lang="ts">
import CabinetProviderLayout from '@/layouts/CabinetProviderLayout.vue'
import { ref } from 'vue'
import { advertisementService } from '@/services/advertisements.service'
import { type Advertisement } from '@/types/Advertisements'
import { useUserStore } from '@stores/UserStore'
import { vMaska } from 'maska'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { categories } from '@/utils/categoryList'

const snackbarStore = useSnackbarStore()
const options = { mask: '+77#########' }
const userStore = useUserStore()
const dialog = ref(false)
const valid = ref(false)
const form = ref(null)
const advertisement = ref<Advertisement>({
  category: '',
  author: 1 || userStore.user?.id!,
  title: '',
  text: '',
  min_price: 0,
  max_price: 0,
  contract_name: '',
  phone: '+77',
  address: '',
  specification: ''
})

const rules = {
  required: (value: any) => !!value || 'Поле обязательно',
  isNumber: (value: any) => !isNaN(value) || 'Значение должно быть числом',
  isPhone: (value: string) => /^\+?[1-9]\d{1,14}$/.test(value) || 'Некорректный номер телефона'
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

const submitForm = async () => {
  if (await isValid()) {
    try {
      await advertisementService.createAdvertisements(advertisement.value)
      snackbarStore.pullSnackbar('Объявление успешно создано.', 3000, '#5b9271')
      dialog.value = false
      resetForm()
    } catch (error) {
      console.error('Ошибка создания объявления:', error)
      snackbarStore.pullSnackbar('Неудалось создать обьявление.', 3000, '#d20f0d')
    }
  }
}
</script>

<style scoped>
.headline {
  font-weight: bold;
}
</style>
