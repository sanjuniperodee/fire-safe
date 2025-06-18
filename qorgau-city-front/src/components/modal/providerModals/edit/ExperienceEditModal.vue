<script setup lang="ts">
import { rules } from '@components/forms/rules/statementRules'
import LoaderInModal from '@components/loader/LoaderInModal.vue'
import MediaUpload from '@components/mediaUpload/MediaUpload.vue'
import { useExperienceStore } from '@stores/providerProfileStore/ExperienceStore'
import { computed, onMounted, ref, watch } from 'vue'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { type Achievement, type Experience } from '@/types/ProviderProfile'
import { deleteBasket } from '@/assets/svg'

const props = defineProps<{
  showModal: boolean
  id: number
}>()

const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const snackbarStore = useSnackbarStore();
const experienceStore = useExperienceStore();

const isUploadLoading = ref<boolean>(false);
const uploadedFile = ref<{ name: string; url: string } | null>(null);

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];
    uploadedFile.value = {
      name: file.name,
      url: URL.createObjectURL(file),
    };
    if (experienceStore.experience) {
      experienceStore.experience.media = file;
    }
  }
};

const removeFile = () => {
  uploadedFile.value = null;
  
};

const validateForm = () => {
  const errors: string[] = [];

  const experience = experienceStore.experience;

  if (!experience?.company_name) errors.push('Поле "Название компании" обязательно для заполнения.');
  if (!experience?.year_start || isNaN(experience.year_start) || experience.year_start <= 0)
    errors.push('Поле "Год начала" должно быть числом больше нуля.');
  if (!experience!.performing_now && (!experience!.year_end || isNaN(experience!.year_end) || experience!.year_end <= 0))
    return('Поле "Год окончания" должно быть числом больше нуля.');
  if (!experience?.media) errors.push('Вы должны загрузить медиафайл.');

  return errors[0];
};

const handleSubmit = async () => {
  const validationErrors = validateForm();
  if (validationErrors) {
    snackbarStore.pullSnackbar(validationErrors, 3000, '#d20f0d');
    return;
  }

  const formData = new FormData();
  let hasChanges = false;

  const experience = experienceStore.experience;
  const originalExperience = ref<Experience | null>(null);

  if (experience?.company_name !== originalExperience.value?.company_name) {
    formData.append('company_name', experience!.company_name);
    hasChanges = true;
  }
  if (experience?.year_start !== originalExperience.value?.year_start) {
    formData.append('year_start', experience!.year_start.toString());
    hasChanges = true;
  }
  if (experience?.year_end !== originalExperience.value?.year_end) {
    formData.append('year_end', experience!.year_end.toString());
    hasChanges = true;
  }
  if (experience?.performing_now !== originalExperience.value?.performing_now) {
    formData.append('performing_now', experience!.performing_now.toString());
    hasChanges = true;
  }
  if (experience?.media instanceof File) {
    formData.append('media', experience.media);
    hasChanges = true;
  }

  if (!hasChanges) {
    snackbarStore.pullSnackbar('Нет изменений для сохранения.', 3000, '#5b9271');
    return;
  }

  try {
    isUploadLoading.value = true;
    await experienceStore.editExperience(props.id, formData);
    snackbarStore.pullSnackbar('Опыт успешно обновлен.', 3000, '#5b9271');
    isUploadLoading.value = false;
    toggleModal();
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
    snackbarStore.pullSnackbar('Не удалось обновить запись об опыте.', 3000, '#d20f0d');
    isUploadLoading.value = false;
  }
}

const initializeExperience = async (id: number) => {
  await experienceStore.getExperience(id);
  uploadedFile.value = null;
};

const handleDelete = async(id: number) => {
  try {
    isUploadLoading.value = true;
    await experienceStore.deleteExperience(id);
    experienceStore.experience = null
    snackbarStore.pullSnackbar('Опыт успешно удален.', 3000, '#5b9271');
    isUploadLoading.value = false;
  } catch(error) {
    console.error(error)
    snackbarStore.pullSnackbar('Не удалось удалить запись об опыте.', 3000, '#d20f0d');
    isUploadLoading.value = false;
  }
}

watch(() => props.id, async (newId) => {
  if (newId) {
    await initializeExperience(newId);
  }
}, { immediate: true });

onMounted(async () => {
  if (props.id != null && props.id > 0) {
    await initializeExperience(props.id);
  }
});

const displayedMedia = computed(() => {
  const experience = experienceStore.experience;
  if (experience?.media instanceof File) {
    return uploadedFile.value?.url;
  }
  return experience?.media;
});

</script>

<template>
  <div v-if="showModal && experienceStore.experience" class="modal-overlay">
    <LoaderInModal v-if="isUploadLoading" />
    <div class="modal">
      <form @submit.prevent="handleSubmit">
        <div class="header">
          <h2 class="modal-title">Редактировать Опыт</h2>

          <div class="header-toolbar">
            <button @click.stop="handleDelete(experienceStore.experience?.id!)" class="header-delete-btn">
              <span v-html="deleteBasket"></span>
            </button>

            <button @click="toggleModal" class="close-btn">&times;</button>
          </div>
        </div>

        <div class="statement-list">
          <v-text-field
            v-model="experienceStore.experience!.company_name"
            label="Название компании"
            :rules="[rules.required]"
          ></v-text-field>

          <div class="year-average">
            <v-text-field
              v-model.number="experienceStore.experience!.year_start"
              label="Год начала"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>

            <v-text-field
              v-if="!experienceStore.experience!.performing_now"
              v-model.number="experienceStore.experience!.year_end"
              label="Год окончания"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>
          </div>

          <v-switch
            v-model="experienceStore.experience!.performing_now"
            label="Работаю сейчас"
            inset
          ></v-switch>

          <MediaUpload v-if="!displayedMedia" :title="'Фото Диплома'" :handleFileChange="handleFileChange"/>

          <div v-if="displayedMedia" class="file-preview">
            <img :src="displayedMedia.toString()" :alt="uploadedFile?.name || 'Experience media'" class="file-thumbnail" />
            <div class="file-info">
              <button type="button" class="delete-btn" @click="removeFile">
                <v-icon>mdi-delete</v-icon>
              </button>
            </div>
          </div>
        </div>

        <div class="footer">
          <v-btn class="send-btn" type="submit" :loading="isUploadLoading" color="#f57c01">
            Сохранить изменения
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
  z-index: 999;
  width: 100%;
  height: 70px;
  background-color: white;
  padding: 5px 20px;
}

h2 {
  font-size: 20px;
  font-weight: 500;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.footer {
  display: flex;
  justify-content: center;
  align-items: center;
  position: sticky;
  bottom: 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.header-toolbar{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.year-average{
  display: flex;
  gap: 20px;
}

.close-btn, .header-delete-btn {
  background: none;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30px;
  font-size: 30px;
  border-radius: 5px;
  cursor: pointer;
  transition: .3s ease-in-out;

  &:hover{
    background-color: #f5f5f5;
  }
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
</style>
