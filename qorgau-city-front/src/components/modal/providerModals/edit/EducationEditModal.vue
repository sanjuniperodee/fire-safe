<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useEducationStore } from '@/stores/providerProfileStore/EducationStore'
import { useSnackbarStore } from '@stores/SnackbarStore'
import {
  type Education,
  type DegreeOptionsRussian,
  getEnglishDegreeOptions,
  getLocalDegreeOptions
} from '@/types/ProviderProfile'
import { deleteBasket } from "@/assets/svg"
import { rules } from '@components/forms/rules/statementRules'
import LoaderInModal from '@components/loader/LoaderInModal.vue'
import MediaUpload from '@components/mediaUpload/MediaUpload.vue'

const props = defineProps<{
  showModal: boolean
  id: number
}>()

const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const snackbarStore = useSnackbarStore();
const educationStore = useEducationStore();

const originalEducation = ref<Education | null>(null)

const degreeOptions = ref<string[]>([
  'Бакалавр',
  'Магистр',
  'Другое',
  'Не указан'
]);

const selectedDegree = computed<string>({
  get: () => {
    return educationStore.education?.degree 
      ? getLocalDegreeOptions(educationStore.education?.degree) 
      : "";
  },
  set: (value: string) => {
    if (educationStore.education) {
      educationStore.education.degree = getEnglishDegreeOptions(value as DegreeOptionsRussian);
    }
  }
});

const displayedMedia = computed(() => {
  const media = educationStore.education?.media;
  if (media instanceof File) {
    return URL.createObjectURL(media);
  }
  return media;
});

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];
    if (educationStore.education) {
      educationStore.education.media = file;
    }
  }
};

const removeFile = () => {
  if (educationStore.education) {
    educationStore.education.media = new File([], ""); // создаем пустой файл
  }
};

const validateForm = (): string | null => {
  const education = educationStore.education;
  if (!education) return 'Данные об образовании отсутствуют.';

  if (!education.college_name) return 'Поле "Название колледжа" обязательно для заполнения.';
  if (!education.year_start || isNaN(education.year_start) || education.year_start <= 0)
    return 'Поле "Год начала" должно быть числом больше нуля.';
  if (!education.performing_now && (!education.year_end || isNaN(education.year_end) || education.year_end <= 0))
    return 'Поле "Год окончания" должно быть числом больше нуля.';
  if (!education.media) return 'Вы должны загрузить медиафайл.';

  return null;
};

const handleSubmit = async () => {
  const validationError = validateForm();
  if (validationError) {
    snackbarStore.pullSnackbar(validationError, 3000, '#d20f0d');
    return;
  }

  const formData = new FormData();
  let hasChanges = false;
  const education = educationStore.education;

  if (education) {
    if (education.college_name !== originalEducation.value?.college_name) {
      formData.append('college_name', education.college_name);
      hasChanges = true;
    }
    if (education.degree !== originalEducation.value?.degree) {
      formData.append('degree', education.degree);
      hasChanges = true;
    }
    if (education.year_start !== originalEducation.value?.year_start) {
      formData.append('year_start', education.year_start.toString());
      hasChanges = true;
    }
    if (education.year_end !== originalEducation.value?.year_end) {
      formData.append('year_end', education.year_end.toString());
      hasChanges = true;
    }
    if (education.performing_now !== originalEducation.value?.performing_now) {
      formData.append('performing_now', education.performing_now.toString());
      hasChanges = true;
    }
    if (education.media instanceof File) {
      formData.append('media', education.media);
      hasChanges = true;
    }
    if (education.show_photo_to_clients !== originalEducation.value?.show_photo_to_clients) {
      formData.append('show_photo_to_clients', education.show_photo_to_clients.toString());
      hasChanges = true;
    }
  }

  if (!hasChanges) {
    snackbarStore.pullSnackbar('Нет изменений для сохранения.', 3000, '#5b9271');
    return;
  }

  try {
    await educationStore.editEducation(props.id, formData);
    await educationStore.getEducations()
    snackbarStore.pullSnackbar('Образование успешно обновлено.', 3000, '#5b9271');
    toggleModal();
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
    snackbarStore.pullSnackbar('Не удалось обновить запись об образовании.', 3000, '#d20f0d');
  }
}

const handleDelete = async(id: number) => {
  try {
    await educationStore.deleteEducation(id);
    await educationStore.getEducations()
    educationStore.education = null
    snackbarStore.pullSnackbar('Образование успешно удалено.', 3000, '#5b9271');
  } catch(error) {
    console.error(error)
    snackbarStore.pullSnackbar('Не удалось удалить запись об образовании.', 3000, '#d20f0d');
  }
}

watch(() => props.id, async (newId) => {
  if (newId) {
    await educationStore.getEducation(newId);
  }
}, { immediate: true });

onMounted(async () => {
  if (props.id) {
    await educationStore.getEducation(props.id);
  }
});
</script>

<template>
  <div v-if="showModal && educationStore.education" class="modal-overlay">
    <LoaderInModal v-if="educationStore.isLoading" />
    <div class="modal">
      <form @submit.prevent="handleSubmit">
        <div class="header">
          <h2 class="modal-title">Редактировать Образование</h2>

          <div class="header-toolbar">
            <button @click.stop="handleDelete(educationStore.education?.id!)" class="header-delete-btn">
              <span v-html="deleteBasket"></span>
            </button>

            <button @click="toggleModal" class="close-btn">&times;</button>
          </div>
        </div>

        <div class="statement-list">
          <v-select
            v-model="selectedDegree"
            :items="degreeOptions"
            label="Степень"
            :rules="[rules.required]"
          ></v-select>

          <v-text-field
            v-model="educationStore.education.college_name"
            label="Название ВУЗ-а как в дипломе"
            :rules="[rules.required]"
          ></v-text-field>

          <div class="year-average">
            <v-text-field
              v-model.number="educationStore.education.year_start"
              label="Год начала"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>

            <v-text-field
              v-if="!educationStore.education.performing_now"
              v-model.number="educationStore.education.year_end"
              label="Год окончания"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>
          </div>

          <v-switch
            v-model="educationStore.education.performing_now"
            label="Учусь сейчас"
            inset
          ></v-switch>

          <MediaUpload v-if="!displayedMedia" :title="'Фото Диплома'" :handleFileChange="handleFileChange"/>

          <div v-if="displayedMedia" class="file-preview">
            <img :src="displayedMedia.toString()" :alt="educationStore.education?.media?.name || 'Education media'" class="file-thumbnail" />
            <div class="file-info">
              <button type="button" class="delete-btn" @click="removeFile">
                <v-icon>mdi-delete</v-icon>
              </button>
            </div>
          </div>

          <v-switch
            v-model="educationStore.education.show_photo_to_clients"
            label="Показывать фото клиентам"
            inset
          ></v-switch>
        </div>

        <div class="footer">
          <v-btn class="send-btn" type="submit" :loading="educationStore.isLoading" color="#f57c01">
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
  font-weight: bold;
}

.year-average{
  display: flex;
  gap: 20px;
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
