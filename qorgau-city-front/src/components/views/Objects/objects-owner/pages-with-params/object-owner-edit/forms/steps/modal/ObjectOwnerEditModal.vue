<template>
  <v-dialog class="dialog" v-model="objectStore.isKeyDialogOpen">
    <v-card class="dialog__card">
      <v-card-title class="dialog__title"> {{ title }}</v-card-title>
      <div class="dialog__box">
        <div class="d-flex" style="align-items: center; gap: 1em; margin-bottom: 20px">
          <v-file-input accept="application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint,
                    text/plain, application/pdf, image/*" color="#f57c01" :loading="isUploadLoading"
            :disabled="isUploadLoading" @change="(e: any) => uploadFile(e)" variant="solo-filled" chips
            hide-details="auto" label="Загрузите соответствующий документ"></v-file-input>
        </div>
        <v-textarea color="#f57c01" :loading="isUploadLoading" :disabled="isUploadLoading" v-model="commentRef"
          class="dialog__input" label="Примечание" variant="outlined"></v-textarea>
        <div class="comment-block instagram-comment">
          <div class="header">
            <div class="username">Инспектор</div>
            <div class="date-block" v-if="inspectorCommentRef.length > 0">
              <p class="date">{{ formatDateTime(inspectorCommentUpdatedDate) }}</p>
            </div>
          </div>
          <div class="comment-container">
            <div class="comment-content">
              <p class="comment-text" v-if="inspectorCommentRef.length > 0">
                {{ inspectorCommentRef }}
              </p>
            </div>
          </div>
        </div>


        <!-- <v-text-field
          readonly
          v-model="inspectorCommentRef"
          class="dialog__input"
          label="Примечание от Инспектора"
          variant="outlined"
          disabled
        ></v-text-field> -->
        <LoaderSpinner v-if="fileStore.isFilesLoading" />
        <div v-if="!fileStore.isFilesLoading" class="dialog__doc-list">
          <FileVue v-for="filebody in fileStore.files" :filebody="filebody" :extension="getFileExtension(filebody.name)"
            :name="filebody.name" :key="filebody.id" />
        </div>
      </div>
      <v-card-actions style="justify-content: end">
        <v-btn :loading="isUploadLoading" :disabled="isUploadLoading" @click="() => saveFiles()" color="#5b9271"
          variant="elevated" class="text-white text-capitalize" prepend-icon="mdi-content-save">
          <span style="padding-top: 4px">Сохранить</span>
        </v-btn>
        <v-btn :loading="isUploadLoading" :disabled="isUploadLoading" color="#d20f0d" variant="elevated"
          class="text-white text-capitalize" @click="closeModal" prepend-icon="mdi-cancel">
          <span style="padding-top: 3px">Отмена</span>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useObjectStore } from '@stores/ObjectStore'
import { ref, toRefs, watch } from 'vue'
import FileVue from './FileVue.vue'
import { generateUniqueId, getFileExtension } from '@/utils/fileUtils'
import { useFileStore } from '@/stores/FileStore'
import type { FileBody } from '@/types/FileBody'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'
import { useRoute, useRouter } from 'vue-router'
import { fileService } from '@/services/file.service'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'

const props = defineProps<{
  title: string
  comment: string
  uuid: number
  inspector_comment: string
  inspector_comment_updated_date: Date | undefined
}>()

const objectStore = useObjectStore()
const objectInfoStore = useObjectInfoStore()
const fileStore = useFileStore()
const isUploadLoading = ref<boolean>(false)
const snackbarStore = useSnackbarStore()
const route = useRoute()
const router = useRouter()

const saveFiles = async () => {
  isUploadLoading.value = true
  try {
    for (const file of fileStore.newFiles) {
      const formData = new FormData()
      formData.append('building', route.params.id as string)
      formData.append('document_key', props.uuid.toString())
      formData.append('path', file.file)
      formData.append('comment', commentRef.value)
      await fileService.uploadFile(formData)
    }

    isUploadLoading.value = false
    await closeModal()
    snackbarStore.pullSnackbar(
      'Ваши документы успешно сохранены. Обновляем страницу.',
      2000,
      '#5b9271'
    )
    objectInfoStore.updateComment(commentRef.value, props.title)

    fileStore.files = []
    fileStore.newFiles = []

    await objectInfoStore.getObjectInfo(route.params.id as string)
    objectInfoStore.calculateProgressForEachTopic()

  } catch (error) {
    isUploadLoading.value = false
    snackbarStore.pullSnackbar(
      'Не удалось загрузить ваши документы. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
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

const closeModal = async () => {
  objectStore.isKeyDialogOpen = false
  updateNewFilesOnClose()
  fileStore.newFiles = []
  fileStore.files = []
  commentRef.value = props.comment

}

const uploadFile = (e: any) => {
  const selectedFile: File = e.target.files[0]
  const fileBody: FileBody = {
    id: generateUniqueId(),
    name: selectedFile.name
  }
  const reader = new FileReader()

  reader.onloadend = () => {
    fileStore.files.push(fileBody)
    fileStore.newFiles.push({
      ...fileBody,
      file: selectedFile
    })
  }
  reader.readAsDataURL(selectedFile)
}

const updateNewFilesOnClose = () => {
  let updatedObject = objectInfoStore.objectDocumentsInfo
  fileStore.newFiles.forEach((newFile) => {
    updatedObject.forEach((topic) => {
      if (topic.subParagraphs) {
        topic.subParagraphs.forEach((subParagraph: any) => {
          subParagraph.keys.forEach((key: any) => {
            key.files = key.files.filter((keyFile: any) => keyFile.id !== newFile.id)
          })
        })
        return
      }
      // keys
      topic.keys.forEach((key: any) => {
        key.files = key.files.filter((keyFile: any) => keyFile.id !== newFile.id)
      })
    })
  })
  objectInfoStore.objectDocumentsInfo = updatedObject
}

const { comment: commentToRefed, inspector_comment: inspectorCommentToRefed, inspector_comment_updated_date: insCommentDateToRef } = toRefs(props)
const commentRef = ref<string>('')
const inspectorCommentRef = ref<string>('')
const inspectorCommentUpdatedDate = ref<Date>()

watch(commentToRefed, () => {
  commentRef.value = commentToRefed.value
})

watch(inspectorCommentToRefed, () => {
  inspectorCommentRef.value = inspectorCommentToRefed.value
})

watch(insCommentDateToRef, () => {
  inspectorCommentUpdatedDate.value = insCommentDateToRef.value
})
</script>

<style lang="scss" scoped>
.comment {
  width: 100%;
  min-height: 30px;
  background-color: #e0e0e0;
  border-radius: 7px;
  padding: 10px;
  margin: 10px 0;

  p {
    font-size: 14px;
    font-weight: 300;
  }
}

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

.date-block {
  max-width: 100%;
  margin-bottom: 10px;
  display: flex;
  justify-content: end;
  align-items: center;
}

.instagram-comment {
  background-color: white;
  border: 1px solid #dbdbdb;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;

    .username {
      font-weight: 600;
      color: #262626;
      font-size: 14px;
    }

    .date-block {
      .date {
        color: #8e8e8e;
        font-size: 12px;
      }
    }
  }

  .comment-container {
    .comment-content {
      .comment-text {
        color: #262626;
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
      }
    }
  }
}

</style>
