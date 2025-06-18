<script setup lang="ts">
import { categories } from '@/utils/categoryList'
import { useStatementForm } from '@components/forms/useStatementForm'
import { rules } from '@components/forms/rules/statementRules'
import LoaderInModal from '@components/loader/LoaderInModal.vue'

const {
  isUploadLoading,
  selectedCategories,
  uploadedFiles,
  statement,
  day,
  hour,
  handleFileChange,
  removeFile,
  submitForm
} = useStatementForm()

defineProps<{
  showModal: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const toggleModal = () => {
  emit('close')
}

const handleSubmit = async () => {
  await submitForm(toggleModal)
}
</script>

<template>
  <div
    v-if="showModal"
    class="modal-overlay"
  >
    <LoaderInModal v-if="isUploadLoading" />
    <div class="modal">
      <form @submit.prevent="handleSubmit">
        <div class="header">
          <button
            @click="toggleModal"
            class="close-btn"
          >
            &times;
          </button>
          <h2 class="modal-title">Выберите параметры услуги</h2>
        </div>

        <div class="statement-list">
          <v-select
            v-model="selectedCategories"
            :items="categories"
            item-title="name"
            item-value="id"
            label="Выберите категории"
            multiple
            chips
            :rules="[rules.required]"
          >
          </v-select>

          <v-text-field
            v-model="statement.text"
            label="Текст"
            :rules="[rules.required]"
          ></v-text-field>

          <v-text-field
            v-model="statement.location"
            label="Место услуги"
            placeholder="г.Астана, Улы дала 39/1"
            :rules="[rules.required]"
          ></v-text-field>

          <label class="label">Время услуги</label>

          <v-text-field
            v-model="day"
            type="date"
            label="День"
            variant="solo-filled"
            :rules="[rules.required]"
          ></v-text-field>

          <v-text-field
            v-model="hour"
            type="time"
            label="Час"
            variant="solo-filled"
            :rules="[rules.required]"
          ></v-text-field>

          <label class="label">Стоимость</label>

          <v-text-field
            v-model.number="statement.min_price"
            label="Минимальная цена(тг)"
            type="number"
            :rules="[rules.required, rules.isNumber]"
          ></v-text-field>

          <v-text-field
            v-model.number="statement.max_price"
            label="Максимальная цена(тг)"
            type="number"
            :rules="[rules.required, rules.isNumber]"
          ></v-text-field>

          <v-file-input
            label="Загрузите фото/видео"
            multiple
            title="Загрузите фото/видео"
            accept="image/png, image/jpeg, video/*"
            show-size
            @change="handleFileChange"
          ></v-file-input>
        </div>

        <div
          v-if="uploadedFiles.length > 0"
          class="uploaded-files"
        >
          <h3>Загруженные файлы:</h3>
          <div
            v-for="file in uploadedFiles"
            :key="file.name"
            class="file-preview"
          >
            <template
              v-if="
                file.url.endsWith('.jpg') || file.url.endsWith('.jpeg') || file.url.endsWith('.png')
              "
            >
              <img
                :src="file.url"
                :alt="file.name"
                class="file-thumbnail"
              />
            </template>
            <template
              v-if="
                file.url.endsWith('.mp4') ||
                file.url.endsWith('.avi') ||
                file.url.endsWith('.quicktime')
              "
            >
              <video
                :src="file.url"
                controls
                class="file-thumbnail"
              ></video>
            </template>
            <p>{{ file.name }}</p>
            <button
              class="delete-btn"
              @click="removeFile(file.name)"
            >
              <v-icon>mdi-delete</v-icon>
            </button>
          </div>
        </div>

        <div class="footer">
          <v-btn
            class="send-btn"
            type="submit"
            :loading="isUploadLoading"
            color="#f57c01"
          >Отправить</v-btn>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1000;
}
.modal {
  background: white;
  border-radius: 8px;
  width: 100%;
  max-width: 700px;
  max-height: 500px;
  overflow-y: auto;
  position: relative;
}

.header, .footer {
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  width: 100%;
  height: 70px;
  background-color: white;
  padding: 5px 20px;
}

h2 {
  font-size: 20px;
  font-weight: bold;
}

.header {
  position: sticky;
  top: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.footer {
  position: sticky;
  bottom: 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 30px;
  cursor: pointer;
}

.statement-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
}

.uploaded-files {
  margin-top: 20px;
  padding: 0 20px;
}

.file-preview {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-thumbnail {
  width: 80px;
  height: 60px;
  object-fit: cover;
  margin-right: 10px;
}

.label {
  font-size: 18px;
  font-weight: 500;
}

.send-btn {
  width: 100%;
}

.delete-btn {
  color: #d54d5b;
}
</style>
