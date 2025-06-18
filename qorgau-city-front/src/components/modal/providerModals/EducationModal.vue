<script setup lang="ts">
import { useEducationForm } from '@components/forms/providerForms/useEducationForm'
import { rules } from '@components/forms/rules/statementRules'
import LoaderInModal from '@components/loader/LoaderInModal.vue'
import MediaUpload from '@components/mediaUpload/MediaUpload.vue'
import CheckBox from './UI/CheckBox.vue'

const {
  isUploadLoading,
  degreeOptions,
  selectedDegree,
  education,
  uploadedFile,
  showPhotoToClients,
  performingNow,
  handleFileChange,
  removeFile,
  submitForm
} = useEducationForm()

defineProps<{
  showModal: boolean
}>()

const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const handleSubmit = async () => {
  await submitForm(toggleModal)
}
</script>

<template>
  <div v-if="showModal" class="modal-overlay">
    <LoaderInModal v-if="isUploadLoading" />
    <div class="modal">
      <form @submit.prevent="handleSubmit">
        <div class="header">
          <button @click="toggleModal" class="close-btn">&times;</button>
          <h2 class="modal-title">Образование</h2>
        </div>

        <div class="statement-list">
          <v-select
            v-model="selectedDegree"
            :items="degreeOptions"
            label="Степень"
            :rules="[rules.required]"
          ></v-select>

          <v-text-field
            v-model="education.college_name"
            label="Название ВУЗ-а как в дипломе"
            :rules="[rules.required]"
          ></v-text-field>

          <div class="year-average">
            <v-text-field
              v-model.number="education.year_start"
              label="Год начала"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>

            <v-text-field
              v-if="!performingNow"
              v-model.number="education.year_end"
              label="Год окончания"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>
          </div>

          <v-switch
            v-model="performingNow"
            label="Учусь сейчас"
            inset
          ></v-switch>

          <MediaUpload v-if="!uploadedFile" :title="'Фото Диплома'" :handleFileChange="handleFileChange"/>

          <div v-if="uploadedFile" class="file-preview">
            <img :src="uploadedFile.url" :alt="uploadedFile.name" class="file-thumbnail" />
            <div class="file-info">
              <p>{{uploadedFile.name}}</p>
              <button type="button" class="delete-btn" @click="removeFile">
                <v-icon>mdi-delete</v-icon>
              </button>
            </div>
          </div>

          <v-switch
            v-model="showPhotoToClients"
            label="Показывать фото клиентам"
            inset
          ></v-switch>
        </div>

        <div class="footer">
          <v-btn class="send-btn" type="submit" :loading="isUploadLoading" color="#f57c01">
            Сохранить
          </v-btn>
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
  border-radius: 10px;
  width: 100%;
  margin: 0 10px;
  max-width: 700px;
  max-height: 80vh;
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

.year-average{
  display: flex;
  gap: 20px;
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

.file-preview {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-thumbnail {
  width: 100px;
  height: 100px;
  border-radius: 5px;
  object-fit: cover;
  margin-right: 10px;
}

.send-btn {
  width: 100%;
}

.delete-btn {
  color: #d54d5b;
}

@media only screen and (max-width: 720px) {
  .year-average{
    flex-direction: column;
    gap: 10px;
  }
}
</style>
