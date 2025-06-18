import { ref } from 'vue';
import { useSnackbarStore } from '@/stores/SnackbarStore';
import { useOtherAchievementsStore } from '@/stores/providerProfileStore/OtherAchievementsStore';

export function useOtherAchievementsForm() {
  const snackbarStore = useSnackbarStore();
  const otherAchievementStore = useOtherAchievementsStore()

  const isUploadLoading = ref<boolean>(false);
  const uploadedFile = ref<{ name: string; url: string } | null>(null)

  const showPhotoToClients = ref<boolean>(true);
  const performingNow = ref<boolean>(false);

  const otherAchievements = ref({
    name: '',
    year_start: 0,
    year_end: 0,
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
      otherAchievements.value.media = file
    }
  }

  const removeFile = () => {
    uploadedFile.value = null
    otherAchievements.value.media = new File([], '')
  }

  const resetForm = () => {
    otherAchievements.value = {
      name: '',
      year_start: new Date().getFullYear(),
      year_end: new Date().getFullYear(),
      media: new File([], '')
    }
    uploadedFile.value = null
    showPhotoToClients.value = false;
    performingNow.value = false;
  }

  const validateForm = () => {
    const errors: string[] = [];

    if (!otherAchievements.value.name) errors.push('Поле "Название" обязательно для заполнения.');
    if (!otherAchievements.value.year_start || isNaN(otherAchievements.value.year_start) || otherAchievements.value.year_start <= 0)
      errors.push('Поле "Год начала" должно быть числом больше нуля.');
    if (!performingNow.value && (!otherAchievements.value.year_end || isNaN(otherAchievements.value.year_end) || otherAchievements.value.year_end <= 0))
      errors.push('Поле "Год окончания" должно быть числом больше нуля.');
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
    formData.append('name', otherAchievements.value.name);
    formData.append('year_start', otherAchievements.value.year_start.toString());
    if (!performingNow.value) {
      formData.append('year_end', otherAchievements.value.year_end.toString());
    }
    formData.append('media', otherAchievements.value.media);
    formData.append('show_photo_to_clients', showPhotoToClients.value.toString());
    formData.append('performing_now', performingNow.value.toString());

    try {
      isUploadLoading.value = true;
      await otherAchievementStore.createOtherAchievements(formData);
      await otherAchievementStore.getOtherAchievements();
      snackbarStore.pullSnackbar('Запись заслуги успешно создана. Обновляем страницу', 3000, '#5b9271');
      isUploadLoading.value = false;
      resetForm();
      toggleModal();
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      snackbarStore.pullSnackbar('Не удалось создать запись о заслуге.', 3000, '#d20f0d');
      isUploadLoading.value = false;
    }
  };

  return {
    isUploadLoading,
    uploadedFile,
    otherAchievements,
    showPhotoToClients,
    performingNow,
    removeFile,
    handleFileChange,
    resetForm,
    validateForm,
    submitForm,
  };
}
