import { ref } from 'vue';
import { useSnackbarStore } from '@/stores/SnackbarStore';
import { useAchievementStore } from '@/stores/providerProfileStore/AchievementStore';

export function useAchievementForm() {
  const snackbarStore = useSnackbarStore();
  const achievementStore = useAchievementStore()

  const isUploadLoading = ref<boolean>(false);
  const uploadedFile = ref<{ name: string; url: string } | null>(null)

  const showPhotoToClients = ref<boolean>(true);

  const achievement = ref({
    certificate_name: '',
    year_received: 0,
    media: new File([], '')
  })

  const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files[0]) {
      const file = target.files[0]
      uploadedFile.value = {
        name: file.name,
        url: URL.createObjectURL(file)
      }
      achievement.value.media = file
    }
  }

  const removeFile = () => {
    uploadedFile.value = null
    achievement.value.media = new File([], '')
  }

  const resetForm = () => {
    achievement.value = {
      certificate_name: '',
      year_received: new Date().getFullYear(),
      media: new File([], '')
    }
    uploadedFile.value = null
    showPhotoToClients.value = false;
  }

  const validateForm = () => {
    const errors: string[] = [];

    if (!achievement.value.certificate_name) errors.push('Поле "Название сертификата" обязательно для заполнения.');
    if (!achievement.value.year_received || isNaN(achievement.value.year_received) || achievement.value.year_received <= 0)
      errors.push('Поле "Год достижения" должно быть числом больше нуля.');
    if (!uploadedFile.value) errors.push('Вы должны загрузить медиафайл.');

    return errors[0];
  };

  const submitForm = async (toggleModal: () => void) => {
    const validationErrors = validateForm();

    if (validationErrors) {
      snackbarStore.pullSnackbar(validationErrors, 3000, '#d20f0d');
      return;
    }

    const formData = new FormData();
    formData.append('certificate_name', achievement.value.certificate_name);
    formData.append('year_received', achievement.value.year_received.toString());
    formData.append('media', achievement.value.media);
    formData.append('show_photo_to_clients', showPhotoToClients.value.toString());

    try {
      isUploadLoading.value = true;
      await achievementStore.createAchievement(formData);
      await achievementStore.getAchievements();
      snackbarStore.pullSnackbar('Запись достижения успешно создана. Обновляем страницу', 3000, '#5b9271');
      isUploadLoading.value = false;
      resetForm();
      toggleModal();
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      snackbarStore.pullSnackbar('Не удалось создать запись о достижении.', 3000, '#d20f0d');
      isUploadLoading.value = false;
    }
  };

  return {
    isUploadLoading,
    uploadedFile,
    achievement,
    showPhotoToClients,
    removeFile,
    handleFileChange,
    resetForm,
    validateForm,
    submitForm,
  };
}
