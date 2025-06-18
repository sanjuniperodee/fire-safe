import { computed } from 'vue'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { UserRoleOptions, type User, type UserRoles } from '@/types/User'
import { type Provider, type AllProvider } from '@/types/Provider'
import { useRouter } from 'vue-router'
import { authService } from '@/services/auth.service'
import { useSnackbarStore } from './SnackbarStore'
import { userService } from '@/services/user.service'

export const useUserStore = defineStore('userStore', () => {
  const user = ref<User | null>(null)
  const checkUser = ref<User | null>(null)

  const acceptedRoles = computed(
    () =>
      user.value?.role.filter((role) => role.status === 'ACCEPTED').map((role) => role.role) || []
  )
  const notAcceptedRoles = computed(
    () =>
      user.value?.role.filter((role) => role.status === 'NOT_ACCEPTED').map((role) => role.role) ||
      []
  )

  const provider = ref<Provider | null>(null)
  const allProviders = computed(
    () => allUsers.value.filter(user =>
      user.role.some(role => role.role === UserRoleOptions.PROVIDER && role.status === 'ACCEPTED')
    )
  )

  const isLogoutLoading = ref<boolean>(false)
  const allUsers = ref<User[]>([])
  const allInsProviders = ref<AllProvider[]>([])

  const router = useRouter()
  const snackbarStore = useSnackbarStore()

  const codeVerificationPhoneNumber = ref<string>('+77')
  const codeSended = ref<boolean>(false)

  const isAuthenticated = ref(false)
  const isInspector = computed(() => acceptedRoles.value.includes(UserRoleOptions.INSPECTOR))

  const isRedirecting = ref(false);

const getUser = async () => {
  // Проверяем наличие токена
  if (!localStorage.getItem('token')) {
    // Если токен отсутствует и редирект еще не выполнялся
    if (!isRedirecting.value) {
      isRedirecting.value = true;
      await router.push({ name: 'Login' });
    }
    return;
  }

  try {
    user.value = await authService.getUser();
    isAuthenticated.value = true;
    checkForAdmin();
  } catch (error) {
    // Если произошла ошибка авторизации
    localStorage.removeItem('token');

    // Проверяем, что редирект уже не был выполнен
    if (!isRedirecting.value) {
      isRedirecting.value = true;
      await router.push({ name: 'Login' });
    }
    throw new Error('Unauthorized 401');
  } finally {
    // После завершения сбрасываем флаг
    isRedirecting.value = false;
  }
};

  const getUserById = async (userId: number) => {
    try {
      checkUser.value = await userService.getUserById(userId)
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }

  const addRole = async (role: UserRoles) => {
    try {
      return await userService.updateUserRole({
        role: role
      })
    } catch (error) {
      console.log('error => ', error)
      throw new Error('Не удалось обновить роли пользователя')
    }
  }

  const deleteRole = async (role: UserRoles) => {
    try {
      return await userService.deleteUserRole({
        role: role
      })
    } catch (error) {
      console.log('error => ', error)
      throw new Error('Не удалось удалить роли пользователя')
    }
  }

  const getAllUsers = async () => {
    try {
      allUsers.value = await userService.getAllUser()
    } catch (error) {
      console.error('Failed to fetch users:', error)
    }
  }



  const getProvider = async (userId: number) => {
    try {
      provider.value = await userService.getProvider(userId)
    } catch (error) {
      console.error('Failed to fetch provider:', error)
    }
  }

  const getAllInsProvider = async () => {
    try {
      allInsProviders.value = await userService.getAllInspProviders()
    } catch (error) {
      console.error('Failed to fetch provider:', error)
    }
  }

  // const getAllProviders = async () => {
  //   try {
  //     allProviders.value = await userService.getAllProviders()
  //   } catch (error) {
  //     console.error('Failed to fetch users:', error)
  //   }
  // }

  const logout = async () => {
    try {
      isLogoutLoading.value = true
      await authService.logout()
      snackbarStore.pullSnackbar('Выход из вашего аккаунта произведен успешно.', 2000, '#5b9271')
      isLogoutLoading.value = false
      isAuthenticated.value = false
      await router.push('/login')
    } catch (error) {
      snackbarStore.pullSnackbar('Не удалось выйти из вашего аккаунта.', 2000, '#d20f0d')
      isLogoutLoading.value = false
    }
  }

  const checkForAdmin = () => {
    const isAllowedForAdmin =
      window.location.pathname === '/admin-building' ||
      window.location.pathname.split('/')[1] + '/' + window.location.pathname.split('/')[2] ===
        'objects/view' ||
      window.location.pathname.split('/')[1] + '/' + window.location.pathname.split('/')[2] ===
        'objects/edit'
    if (acceptedRoles.value.includes(UserRoleOptions.ADMIN) && !isAllowedForAdmin) {
      router.push({ name: 'AdminObject' })
    }
  }

  return {
    isAuthenticated,
    isInspector,
    acceptedRoles,
    notAcceptedRoles,
    user,
    checkUser,
    allUsers,
    provider,
    allProviders,
    getProvider,
    getUser,
    getUserById,
    getAllUsers,
    logout,
    addRole,
    deleteRole,
    isLogoutLoading,
    codeVerificationPhoneNumber,
    codeSended,
    getAllInsProvider,
    allInsProviders,
  }
})
