import { userService } from '@/services/user.service'
import { useProfileStore } from '@/stores/ProfileStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import type { AxiosError } from 'axios';

const profileStore = useProfileStore()
const userStore = useUserStore()
const snackbarStore = useSnackbarStore()
const isEditingLoading = ref(false)

export const editField = (key: string) => {
  profileStore.editField(key as any)
}

export const cancelEditing = (key: string) => {
  profileStore.cancelEditing(key as any)
}

export const saveEditing = async (key: string) => {
  try {
    await profileStore.updateFieldValue(key as any)
    await save(key)
  } catch(error) {
    console.error(error)

    snackbarStore.pullSnackbar(
      'Не удалось обновить ваши поля. Убедитесь, что все поля введены корректно.',
      3000,
      '#d20f0d'
    )
  }

}

export const save = async (key?: string) => {
  try {
    isEditingLoading.value = true;
    // @ts-ignore
    const message = await userService.updateUser(userStore.user?.id!, userStore.user!);
    snackbarStore.pullSnackbar(message, 3000, '#5b9271');
    isEditingLoading.value = false;
  } catch (error) {
    const axiosError = error as AxiosError;
    console.log('ошибка при сохранении', axiosError);

    if (axiosError.response) {
      console.log('Данные перед отправкой:', userStore.user);
      console.log('Статус ошибки:', axiosError.response.status);
      console.log('Ответ от сервера:', axiosError.response.data);  // Сообщение или детали от сервера
    }

    snackbarStore.pullSnackbar('Не удалось обновить ваши данные.', 3000, '#d20f0d');
    if (key) {
      profileStore.cancelEditing(key as any);
    }
    isEditingLoading.value = false;
  }
};