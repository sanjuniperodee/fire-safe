import { ref } from 'vue';
import { useSnackbarStore } from '@/stores/SnackbarStore';
import type { DegreeOptionsRussian } from '@/types/ProviderProfile'
import { getEnglishDegreeOptions } from '@/types/ProviderProfile'
import { useEducationStore } from '@/stores/providerProfileStore/EducationStore';

export function useEducationForm() {
  const snackbarStore = useSnackbarStore();
  const educationStore = useEducationStore();

  const isUploadLoading = ref<boolean>(false);
  const degreeOptions = ref<DegreeOptionsRussian[]>([
    'Бакалавр',
    'Магистр',
    'Другое',
    'Не указан'
  ]);
  const selectedDegree = ref<DegreeOptionsRussian>('Не указан');
  const uploadedFile = ref<{ name: string; url: string } | null>(null);

  const showPhotoToClients = ref<boolean>(true);
  const performingNow = ref<boolean>(false);

  const education = ref({
    college_name: '',
    degree: getEnglishDegreeOptions(selectedDegree.value), // По умолчанию
    year_start: 0,
    year_end: 0,
    media: new File([], '')
  });



  const updateDegree = () => {
    education.value.degree = getEnglishDegreeOptions(selectedDegree.value);
  };

  const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      const file = target.files[0];
      uploadedFile.value = {
        name: file.name,
        url: URL.createObjectURL(file)
      };
      education.value.media = file;
    }
  };

  const removeFile = () => {
    uploadedFile.value = null;
    education.value.media = new File([], '');
  };

  const resetForm = () => {
    education.value = {
      college_name: '',
      degree: getEnglishDegreeOptions(selectedDegree.value),
      year_start: new Date().getFullYear(),
      year_end: new Date().getFullYear(),
      media: new File([], '')
    };
    uploadedFile.value = null;
    showPhotoToClients.value = false;
    performingNow.value = false;
  };

  const validateForm = () => {
    const errors: string[] = [];

    if (!education.value.college_name) errors.push('Поле "Название колледжа" обязательно для заполнения.');
    if (!education.value.year_start || isNaN(education.value.year_start) || education.value.year_start <= 0)
      errors.push('Поле "Год начала" должно быть числом больше нуля.');
    if (!performingNow.value && (!education.value.year_end || isNaN(education.value.year_end) || education.value.year_end <= 0))
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
    updateDegree();

    const formData = new FormData();
    formData.append('college_name', education.value.college_name);
    formData.append('degree', education.value.degree);
    formData.append('year_start', education.value.year_start.toString());
    if (!performingNow.value) {
      formData.append('year_end', education.value.year_end.toString());
    }
    formData.append('media', education.value.media);
    formData.append('show_photo_to_clients', showPhotoToClients.value.toString());
    formData.append('performing_now', performingNow.value.toString());

    try {
      isUploadLoading.value = true;
      await educationStore.createEducation(formData);
      await educationStore.getEducations();
      snackbarStore.pullSnackbar('Образование успешно создано. Обновляем страницу', 3000, '#5b9271');
      isUploadLoading.value = false;
      resetForm();
      toggleModal();
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      snackbarStore.pullSnackbar('Не удалось создать запись об образовании.', 3000, '#d20f0d');
      isUploadLoading.value = false;
    }
  };

  return {
    isUploadLoading,
    degreeOptions,
    selectedDegree,
    uploadedFile,
    showPhotoToClients,
    performingNow,
    education,
    removeFile,
    handleFileChange,
    resetForm,
    validateForm,
    submitForm,
  };
}
