<script setup lang="ts">
import { rules } from '@components/forms/rules/statementRules'
import LoaderInModal from '@components/loader/LoaderInModal.vue'
import MediaUpload from '@components/mediaUpload/MediaUpload.vue'
import { useOtherAchievementsStore } from '@stores/providerProfileStore/OtherAchievementsStore'
import { computed, onMounted, ref, watch } from 'vue'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { deleteBasket } from "@/assets/svg"
import type { OtherAchievements } from '@/types/ProviderProfile'

const props = defineProps<{
  showModal: boolean
  id: number
}>()

const emit = defineEmits(['close'])

const toggleModal = () => {
  emit('close')
}

const snackbarStore = useSnackbarStore();
const otherAchievementStore = useOtherAchievementsStore();

const originalOtherAchievement = ref<OtherAchievements | null>(null)
const isUploadLoading = computed(() => otherAchievementStore.isLoading);

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    otherAchievementStore.otherAchievement!.media = target.files[0];
  }
};

const removeFile = () => {
  if (otherAchievementStore.otherAchievement) {
    otherAchievementStore.otherAchievement.media = new File([], "");
  }
};

const validateForm = () => {
  const errors: string[] = [];

  if (!otherAchievementStore.otherAchievement?.name) errors.push('Поле "Название" обязательно для заполнения.');
  if (!otherAchievementStore.otherAchievement?.year_start || isNaN(otherAchievementStore.otherAchievement.year_start) || otherAchievementStore.otherAchievement.year_start <= 0)
    errors.push('Поле "Год начала" должно быть числом больше нуля.');
  if (!otherAchievementStore.otherAchievement!.performing_now && (!otherAchievementStore.otherAchievement!.year_end || isNaN(otherAchievementStore.otherAchievement!.year_end) || otherAchievementStore.otherAchievement!.year_end <= 0))
    return('Поле "Год окончания" должно быть числом больше нуля.');
  if (!otherAchievementStore.otherAchievement?.media) errors.push('Вы должны загрузить медиафайл.');

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

  if (otherAchievementStore.otherAchievement?.name !== originalOtherAchievement.value?.name) {
    formData.append('certificate_name', otherAchievementStore.otherAchievement!.name);
    hasChanges = true;
  }
  if (otherAchievementStore.otherAchievement?.year_start !== originalOtherAchievement.value?.year_start) {
    formData.append('year_start', otherAchievementStore.otherAchievement!.year_start.toString());
    hasChanges = true;
  }
  if (otherAchievementStore.otherAchievement?.year_end !== originalOtherAchievement.value?.year_end) {
    formData.append('year_end', otherAchievementStore.otherAchievement!.year_end.toString());
    hasChanges = true;
  }
  if (otherAchievementStore.otherAchievement?.show_photo_to_clients !== originalOtherAchievement.value?.show_photo_to_clients) {
    formData.append('show_photo_to_clients', otherAchievementStore.otherAchievement!.show_photo_to_clients.toString());
    hasChanges = true;
  }
  if (otherAchievementStore.otherAchievement?.media instanceof File) {
    formData.append('media', otherAchievementStore.otherAchievement.media);
    hasChanges = true;
  }

  if (!hasChanges) {
    snackbarStore.pullSnackbar('Нет изменений для сохранения.', 3000, '#5b9271');
    return;
  }

  try {
    await otherAchievementStore.editOtherAchievement(props.id, formData);
    await otherAchievementStore.getOtherAchievements()
    snackbarStore.pullSnackbar('Достижение успешно обновлено.', 3000, '#5b9271');
    toggleModal();
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
    snackbarStore.pullSnackbar('Не удалось обновить запись о достижении.', 3000, '#d20f0d');
  }
}

const handleDelete = async (id: number) => {
  try {
    await otherAchievementStore.deleteOtherAchievement(id);
    await otherAchievementStore.getOtherAchievements()
    otherAchievementStore.otherAchievement = null
    snackbarStore.pullSnackbar('Достижение успешно удалено.', 3000, '#5b9271');
  } catch (error) {
    console.error(error)
    snackbarStore.pullSnackbar('Не удалось удалить запись о достижении.', 3000, '#d20f0d');
  }
}

watch(() => props.id, async (newId) => {
  if (newId) {
    await otherAchievementStore.getOtherAchievement(newId);
  }
}, { immediate: true });

onMounted(async () => {
  if (props.id) {
    await otherAchievementStore.getOtherAchievement(props.id);
  }
});

const displayedMedia = computed(() => {
  if (otherAchievementStore.otherAchievement?.media instanceof File) {
    return URL.createObjectURL(otherAchievementStore.otherAchievement.media);
  }
  return otherAchievementStore.otherAchievement?.media;
});

</script>

<template>
  <div v-if="showModal && otherAchievementStore.otherAchievement" class="modal-overlay">
    <LoaderInModal v-if="isUploadLoading" />
    <div class="modal">
      <form @submit.prevent="handleSubmit">
        <div class="header">
          <h2 class="modal-title">Редактировать Заслугу</h2>

          <div class="header-toolbar">
            <button @click.stop="handleDelete(otherAchievementStore.otherAchievement?.id!)" class="header-delete-btn">
              <span v-html="deleteBasket"></span>
            </button>

            <button @click="toggleModal" class="close-btn">&times;</button>
          </div>
        </div>

        <div class="statement-list">
          <v-text-field
            v-model="otherAchievementStore.otherAchievement.name"
            label="Название"
            :rules="[rules.required]"
          ></v-text-field>

          <div class="year-average">
            <v-text-field
              v-model.number="otherAchievementStore.otherAchievement!.year_start"
              label="Год начала"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>

            <v-text-field
              v-if="!otherAchievementStore.otherAchievement!.performing_now"
              v-model.number="otherAchievementStore.otherAchievement!.year_end"
              label="Год окончания"
              type="number"
              :rules="[rules.required, rules.isNumber]"
            ></v-text-field>
          </div>

          <v-switch
            v-model="otherAchievementStore.otherAchievement!.performing_now"
            label="Работаю сейчас"
            inset
          ></v-switch>

          <MediaUpload v-if="!displayedMedia" :title="'Фото Сертификата'" :handleFileChange="handleFileChange"/>

          <div v-if="displayedMedia" class="file-preview">
            <img :src="displayedMedia.toString()" :alt="otherAchievementStore.otherAchievement?.media.name" class="file-thumbnail" />
            <div class="file-info">
              <button type="button" class="delete-btn" @click="removeFile">
                <v-icon>mdi-delete</v-icon>
              </button>
            </div>
          </div>

          <v-switch
            v-model="otherAchievementStore.otherAchievement.show_photo_to_clients"
            label="Показывать фото клиентам"
            inset
          ></v-switch>
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
  font-weight: bold;
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
