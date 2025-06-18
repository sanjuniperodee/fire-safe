<template>
  <v-dialog
    class="dialog"
    v-model="objectStore.isKeyDialogOpen"
  >
    <v-card class="dialog__card">
      <v-card-title class="dialog__title"> {{ title }}</v-card-title>
      <div class="dialog__box">
        <div class="date-block" v-if="inspectorCommentRef.length > 0">
          <p class="date">{{ formatDateTime(inspectorCommentDate) }}</p>
        </div>
        <v-text-field
          v-model="inspectorCommentRef"
          class="dialog__input"
          label="Примечание от Инспектора"
          variant="outlined"
        ></v-text-field>

        <div class="date-block" v-if="commentRef.length > 0">
          <p class="date">{{ formatDateTime(commentDate) }}</p>
        </div>
        <v-textarea
          readonly
          v-model="commentRef"
          class="dialog__input"
          label="Примечание от владельца обьекта"
          variant="outlined"
        ></v-textarea>
       
        <div class="dialog__doc-list">
          <FileVue
            v-for="filebody in fileStore.files"
            :filebody="filebody"
            :extension="getFileExtension(filebody.name)"
            :name="filebody.name"
            :key="filebody.id"
          />
        </div>
      </div>
      <v-card-actions style="justify-content: end">
        <v-btn
          :loading="isUploadLoading"
          :disabled="isUploadLoading"
          @click="saveFiles"
          color="#5b9271"
          variant="elevated"
          class="text-white text-capitalize"
          prepend-icon="mdi-content-save"
        >
          <span style="padding-top: 4px">Сохранить</span>
        </v-btn>

        <v-btn
          color="#d20f0d"
          variant="elevated"
          class="text-white text-capitalize"
          @click="() => closeModal()"
          prepend-icon="mdi-close"
          >Закрыть</v-btn
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useObjectStore } from '@stores/ObjectStore'
import { ref, toRefs, watch, onMounted } from 'vue'
import FileVue from './FileVue.vue'
import { getFileExtension } from '@/utils/fileUtils'
import { useFileStore } from '@/stores/FileStore'
import { useRoute } from 'vue-router'
import type { DocumentRemark } from '@/types/ObjectBuilding'
import { useSnackbarStore } from '@stores/SnackbarStore'
 
const props = defineProps<{
  title: string
  comment: string
  comment_updated_date: Date | undefined
  inspector_comment: string
  inspector_comment_updated_date: Date | undefined
  uuid: number
}>()

const route = useRoute()
const objectStore = useObjectStore()
const fileStore = useFileStore()
const isUploadLoading = ref<boolean>(false)
const snackbarStore = useSnackbarStore()

const closeModal = () => {
  objectStore.isKeyDialogOpen = false
  fileStore.newFiles = []
  fileStore.files = []
  commentRef.value = props.comment
  commentDate.value = props.comment_updated_date
  inspectorCommentRef.value = props.inspector_comment
  inspectorCommentDate.value = props.inspector_comment_updated_date
}

const { comment: commentToRefed, inspector_comment: inspectorCommentToRef, comment_updated_date: commentToDate, inspector_comment_updated_date: inspectorCommentToDate} = toRefs(props)
const commentRef = ref<string>('')
const commentDate = ref<Date>()
const inspectorCommentRef = ref<string>('')
const inspectorCommentDate = ref<Date>()

const saveFiles = async () => {
  console.log('building', route.params.id as string)
  console.log('document_key', props.uuid.toString())
  console.log('inspectorCommentRef', inspectorCommentRef.value)

  const body: DocumentRemark = {
    building: Number(route.params.id),
    document_key: Number(props.uuid.toString()),
    content: inspectorCommentRef.value,
  }

  try {
    objectStore.createDocumentRemark(body)
    snackbarStore.pullSnackbar('Подздание создано успешно!', 3000, '#5b9271')
  } catch (error) {
    console.log(error)
    snackbarStore.pullSnackbar('Не удалось создать подздание', 3000, '#d20f0d')
  }
}

const formatDateTime = (dateTimeString: Date | string | undefined): string => {
  if (!dateTimeString) return '';
  
  // Если получаем строку
  if (typeof dateTimeString === 'string') {
    const regex = /(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})/;
    const matches = dateTimeString.match(regex);
    
    if (!matches) return '';
    
    const [_, year, month, day, hours, minutes, seconds] = matches;
    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
  }
  
  // Если получаем объект Date
  if (dateTimeString instanceof Date) {
    const year = dateTimeString.getFullYear();
    const month = String(dateTimeString.getMonth() + 1).padStart(2, '0');
    const day = String(dateTimeString.getDate()).padStart(2, '0');
    const hours = String(dateTimeString.getHours()).padStart(2, '0');
    const minutes = String(dateTimeString.getMinutes()).padStart(2, '0');
    const seconds = String(dateTimeString.getSeconds()).padStart(2, '0');
    
    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
  }
  
  return '';
};

watch(commentToRefed, () => {
  commentRef.value = commentToRefed.value
})

watch(inspectorCommentToRef, () => {
  inspectorCommentRef.value = inspectorCommentToRef.value
})

watch(commentToDate, () => {
  commentDate.value = commentToDate.value
})

watch(inspectorCommentToDate, () => {
  inspectorCommentDate.value = inspectorCommentToDate.value
})
</script>

<style lang="scss" scoped>
.dialog {
  width: 800px;

  &__card {
    padding: 10px;
    display: flex;
    flex-direction: column;
    min-height: 500px;
  }

  &__title {
    font-size: 24px;
    font-family: 'Overpass', sans-serif;
  }

  &__box {
    padding: 30px;
    flex: 1 1 auto;
  }

  &__doc-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
  }
}

@media only screen and (max-width: 830px) {
  .dialog {
    &__title {
      hyphens: none !important;
      text-overflow: initial !important;
      white-space: initial;
      font-size: 18px;
    }

    width: 100%;
  }
}

@media only screen and (max-width: 830px) {
  .dialog {
    &__title {
      font-weight: 700;
      font-size: 16px;
    }

    &__input {
      font-size: 14px !important;
    }

    &__box {
      padding: 15px;
    }
  }

  .v-field__input {
    font-size: 14px !important;
  }

  .v-btn {
    font-size: 12px !important;
  }
}

.dialog__box {
  padding: 20px;
}

.date-block {
  max-width: 100%;
  margin-bottom: 10px;
  display: flex;
  justify-content: end;
  align-items: center;
}

.date {
  color: #757575; /* Светло-серый цвет */
  font-size: 14px;
  font-weight: 400;
  background-color: #f5f5f5; /* Фон для блока */
  padding: 5px 10px;
  border-radius: 5px;
  border: 1px solid #e0e0e0; /* Граница */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* Легкая тень */
}

/* Можно добавить еще некоторые стили для hover или focus */
.date:hover {
  background-color: #e0e0e0; /* Изменение фона при наведении */
}

.date-block p {
  margin: 0;
}
</style>
