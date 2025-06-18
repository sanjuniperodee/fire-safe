import { ref } from 'vue';
import { useSnackbarStore } from '@/stores/SnackbarStore';
import { useExperienceStore } from '@/stores/providerProfileStore/ExperienceStore';

export function useExperienceForm() {
  const snackbarStore = useSnackbarStore();
  const experienceStore = useExperienceStore()

  const isUploadLoading = ref<boolean>(false);
  const uploadedFile = ref<{ name: string; url: string } | null>(null)

  const performingNow = ref<boolean>(false);

  const experience = ref({
    company_name: '',
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
      experience.value.media = file
    }
  }

  const removeFile = () => {
    uploadedFile.value = null
    experience.value.media = new File([], '')
  }

  const resetForm = () => {
    experience.value = {
      company_name: '',
      year_start: new Date().getFullYear(),
      year_end: new Date().getFullYear(),
      media: new File([], '')
    }
    uploadedFile.value = null
    performingNow.value = false;
  }

  const validateForm = () => {
    const errors: string[] = [];

    if (!experience.value.company_name) errors.push('Поле "Название компании" обязательно для заполнения.');
    if (!experience.value.year_start || isNaN(experience.value.year_start) || experience.value.year_start <= 0)
      errors.push('Поле "Год начала" должно быть числом больше нуля.');
    if (!performingNow.value && (!experience.value.year_end || isNaN(experience.value.year_end) || experience.value.year_end <= 0))
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
    formData.append('company_name', experience.value.company_name);
    formData.append('year_start', experience.value.year_start.toString());
    if (!performingNow.value) {
      formData.append('year_end', experience.value.year_end.toString());
    }
    formData.append('media', experience.value.media);
    formData.append('performing_now', performingNow.value.toString());

    try {
      isUploadLoading.value = true;
      await experienceStore.createExperience(formData);
      await experienceStore.getExperiences();
      snackbarStore.pullSnackbar('Запись опыта успешно создана. Обновляем страницу', 3000, '#5b9271');
      isUploadLoading.value = false;
      resetForm();
      toggleModal();
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      snackbarStore.pullSnackbar('Не удалось создать запись об опыте.', 3000, '#d20f0d');
      isUploadLoading.value = false;
    }
  };

  return {
    isUploadLoading,
    uploadedFile,
    experience,
    performingNow,
    removeFile,
    handleFileChange,
    resetForm,
    validateForm,
    submitForm,
  };
}
