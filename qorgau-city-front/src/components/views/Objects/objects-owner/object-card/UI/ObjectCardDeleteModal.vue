<template>
  <v-dialog
    persistent
    v-model="isDeleteDialogOpen"
    width="auto"
  >
    <v-card style="padding: 40px; font-family: 'Overpass', sans-serif">
      <v-card-title class="text-center"
        ><b>Вы уверены что хотите удалить данный объект?</b></v-card-title
      >
      <v-card-text class="text-center"
        >Напишите <b>"УДАЛИТЬ"</b> если вы уверены что хотите удалить данный объект</v-card-text
      >
      <v-text-field
        v-model="textInput"
        @input="checkDeleteStatus"
      >
      </v-text-field>
      <v-card-actions>
        <v-btn
          :loading="isLoading"
          style="width: 50%"
          @click="deleteCard(id!)"
          color="#d20f0d"
          prepend-icon="mdi-delete"
          :disabled="isDeleteButtonDisabled || isLoading"
          stacked
          >Подтвердить удаление</v-btn
        >
        <v-btn
          :disabled="isLoading"
          style="width: 50%"
          @click="$emit('close')"
          color="#d20f0d"
          prepend-icon="mdi-cancel"
          stacked
          >Отмена</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { useObjectStore } from '@/stores/ObjectStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { ref, toRefs } from 'vue'

const objectStore = useObjectStore()
const snackbarStore = useSnackbarStore()
const textInput = ref('')
const isDeleteButtonDisabled = ref(true)

const props = defineProps({
  id: Number,
  isDeleteDialogOpen: Boolean
})

const isLoading = ref(false)
const emit = defineEmits(['close'])

const { isDeleteDialogOpen } = toRefs(props)

const deleteCard = (objectId: number) => {
  try {
    isLoading.value = true
    objectStore.deleteObject(objectId)
    snackbarStore.pullSnackbar('Объект успешно удален.', 2000, '#5b9271')
    emit('close')
    isLoading.value = false
  } catch (error) {
    snackbarStore.pullSnackbar('Не удалось удалить паспорт ПБО. Попробуйте позже.', 3000, '#d20f0d')
    isLoading.value = false
  }
}

const checkDeleteStatus = () => {
  if (textInput.value === 'УДАЛИТЬ') {
    isDeleteButtonDisabled.value = false
  } else {
    isDeleteButtonDisabled.value = true
  }
}
</script>

<style lang="scss" scoped></style>
