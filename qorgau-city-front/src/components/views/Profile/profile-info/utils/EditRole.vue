<template>
  <div class="role_wrapper">
    <LoaderSpinner v-if="isLoading" />

      <v-card-title class="info__title">
        Роль:
      </v-card-title>

      <div class="info__role">
        <div class="acceptedRoles">
          <p>
            Ваша роль(и): {{ userAcceptedRoles }}
          </p>
        </div>

        <div
          class="notAcceptedRoles"
          v-if="userStore.notAcceptedRoles.length > 0"
        >
          <p>
            Ваша заявка на роль(и): {{ userNotAcceptedRoles }} еще в рассмотрении
          </p>
        </div>

        <div>
          <v-select
            :disabled="!roleEditting"
            :rules="roleRules"
            v-model="selectedRussianRole"
            class="role_selector"
            label="Роль"
            :items="russianRoles"
            variant="outlined"
          ></v-select>

          <v-btn
            v-if="!roleEditting"
            @click="roleEditting = true"
            class="add-role-btn"
            color="#f57c01"
          >
            <v-icon style="margin-right: 10px;">mdi-pencil</v-icon>
            Редактировать Роль
          </v-btn>
        </div>

        <div
          v-if="roleEditting"
          class="w-50"
          style="display: flex; gap: 8px"
        >
          <v-btn
            prepend-icon="mdi-plus"
            class="role-edit-btn"
            @click="addRole()"
            color="#5b9271"
          >
            <span style="padding-top: 4px">Добавить роль</span>
          </v-btn>

          <v-btn
            prepend-icon="mdi-minus"
            v-if="roleEditting"
            @click="deleteRole()"
            class="role-edit-btn"
            color="#d20f0d"
          >
            Удалить Роль
          </v-btn>

          <v-btn
            prepend-icon="mdi-cancel"
            @click="roleEditting = false"
            class="role-edit-btn"
            color="#f57c01"
            variant="tonal"
          >
            <span style="padding-top: 4px">Отмена</span>
          </v-btn>
        </div>
      </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { roleRules } from '@views/Register/Rules'
import { roleMapReverse, russianRoles, roleReverseToRussian } from '@/types/User'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'

const isLoading = ref(false)
const userStore = useUserStore()
const snackbarStore = useSnackbarStore()
const roleEditting = ref(false)

const selectedRussianRole = ref()
const userAcceptedRoles = ref('')
const userNotAcceptedRoles = ref('')

const refresh = async () => {
  isLoading.value = true
  await userStore.getUser()
  userAcceptedRoles.value = userStore.acceptedRoles
    .map((role) => roleReverseToRussian[role])
    .join(', ')
  userNotAcceptedRoles.value = userStore.notAcceptedRoles
    .map((role) => roleReverseToRussian[role])
    .join(', ')
  isLoading.value = false
  roleEditting.value = false
}

const addRole = async () => {
  const selectedRole = roleMapReverse[selectedRussianRole.value]
  const russianRole = roleReverseToRussian[selectedRole]

  // tests start
  if (!selectedRole) {
    snackbarStore.pullSnackbar('Неверная роль', 3000, '#d20f0d')
    return
  }
  if (userStore.acceptedRoles.includes(selectedRole)) {
    snackbarStore.pullSnackbar(`Вы уже имеете роль ${russianRole}`, 3000, '#d38f44')
    return
  }
  if (userStore.notAcceptedRoles.includes(selectedRole)) {
    snackbarStore.pullSnackbar(`Вы уже подали заявку на роль ${russianRole}`, 3000, '#d38f44')
    return
  }
  // tests end

  try {
    await userStore.addRole(selectedRole)
    await refresh()
    snackbarStore.pullSnackbar(`Роль ${russianRole} успешно добавлена`, 3000, '#5b9271')
  } catch (error) {
    console.error('Error changing role:', error)
    isLoading.value = false
    snackbarStore.pullSnackbar(`Не удалось добавить роль ${russianRole}`, 3000, '#d20f0d')
  }
}

const deleteRole = async () => {
  const selectedRole = roleMapReverse[selectedRussianRole.value]
  const russianRole = roleReverseToRussian[selectedRole]

  try {
    await userStore.deleteRole(selectedRole)
    await refresh()
    snackbarStore.pullSnackbar(`Роль ${russianRole} успешно удалена`, 3000, '#5b9271')
  } catch (error) {
    console.error('Error deleting role:', error)
    isLoading.value = false
    snackbarStore.pullSnackbar(`Не удалось удалить роль ${russianRole}`, 3000, '#d20f0d')
  }
}

onMounted(async () => {
  await userStore.getUser()
  userAcceptedRoles.value = userStore.acceptedRoles
    .map((role) => roleReverseToRussian[role])
    .join(', ')
  userNotAcceptedRoles.value = userStore.notAcceptedRoles
    .map((role) => roleReverseToRussian[role])
    .join(', ')
})
</script>

<style lang="scss" scoped>
.role_wrapper{
  flex: 1;
}

.info__title {
  padding: 0;
  font-size: 20px;
  font-weight: 600;
  width: 100%;
  margin-top: 20px;
  margin-bottom: 1em;
}

.info__role {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 18px;
  margin-bottom: 1em;
  background-color: white;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 20px;
}

.role_selector {
  width: 100%;
  height: auto;
  margin-top: 20px;
}

.role-edit-btn {
  width: calc((100% - 8px) / (3/2));
}

.add-role-btn {
  width: 100%;
  display: flex;
  gap: 20px;
}
.notAcceptedRoles, .acceptedRoles {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  border-radius: 5px;
  margin: 10px 0;
  padding: 20px 10px;
  color: white;
}

.acceptedRoles{
  background-color: #5a9b5a;
}

.notAcceptedRoles{
  background-color: #cc5757;
}

.role-card {
  width: 100%;
  background-color: #f5f5f5;
  color: #333;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}

.role-card:hover {
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}


@media only screen and (max-width: 720px) {
  .object-btn {
    width: 70% !important;
    font-size: 12px !important;
  }
}

@media only screen and (max-width: 440px) {
  .object-btn {
    width: 100% !important;
    font-size: 10px !important;
  }
}
</style>
