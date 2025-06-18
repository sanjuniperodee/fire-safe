<template>
  <div class="admin-object-parent">
    <v-form
      ref="codeVerificationForm"
      class="admin-object"
    >
      <div class="back-button">
        <v-btn
          @click="() => userStore.logout()"
          prepend-icon="mdi-exit-to-app"
          variant="text"
          style="text-transform: none; margin-bottom: 10px"
        >
          <span style="padding: 3px 0 0 0">Выход</span>
        </v-btn>
      </div>
      <v-card class="admin-object__box">
        <v-card-title>Перейти к объекту</v-card-title>
        <v-card-text style="color: #000"
          >Введите идентификатор паспорта ПБО в который вы хотите перейти или прямо сейчас повторно
          нажмите кнопку <b>"Перейти к Паспорту ПБО" в Административной панели</b>
        </v-card-text>

        <v-text-field
          :rules="commonRules"
          :loading="isLoading"
          class="admin-object__input"
          label="Идентификатор паспорта ПБО"
          v-model="objectId"
          clearable
          variant="outlined"
          hide-details="auto"
          type="text"
        ></v-text-field>
        <div style="display: flex; align-items: end; flex-direction: column">
          <v-btn
            :loading="isLoading"
            color="#f57c01"
            @click.prevent="
              async () => {
                if (await isValid()) {
                  router.push(`/objects/view/${objectId}`)
                }
              }
            "
            class="text-white admin-object__button"
            type="submit"
            append-icon="mdi-chevron-right"
          >
            <span style="padding-top: 2px">Перейти на страницу объекта</span>
          </v-btn>
          <v-btn
            :loading="isLoading"
            color="#f57c01"
            @click.prevent="
              async () => {
                if (await isValid()) {
                  await router.push(`/objects/edit/${objectId}`)
                }
              }
            "
            class="text-white admin-object__button"
            append-icon="mdi-chevron-right"
          >
            <span style="padding-top: 2px">Редактировать объект</span>
          </v-btn>
        </div>
      </v-card>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { useUserStore } from '@/stores/UserStore'
import { UserRoleOptions } from '@/types/User'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
const userStore = useUserStore()
const isLoading = ref<boolean>(false)
const snackbarStore = useSnackbarStore()
const router = useRouter()
const codeVerificationForm = ref(null)
const objectId = ref<string>('')
const commonRules = ref([(v: any) => !!v || 'Идентификатор паспорта ПБО обязателен'])

const isValid = async () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  const { valid } = await codeVerificationForm.value!.validate()
  return valid
}

const resetForm = () => {
  //@ts-expect-error registerForm type gives automaticcaly in vuetify
  codeVerificationForm.value?.reset()
}

onMounted(async () => {
  await userStore.getUser()
  if (userStore.acceptedRoles.includes(UserRoleOptions.ADMIN)) {
    await router.push({ name: 'Map' })
    return
  }
})
</script>

<style lang="scss" scoped>
.admin-object-parent {
  height: 100vh;
  overflow-y: scroll;
}

.admin-object {
  padding: 40px 0;
  background-color: $white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100%;

  &__box {
    border-radius: 1em;
    padding: 10px;
    background-color: #fff;
    display: flex;
    flex-direction: column;
    color: #000;
    width: 500px;
  }

  &__input {
    margin: 10px 15px;
  }

  &__button {
    margin: 5px 15px;
    width: fit-content;
    padding: 0 10px;
    text-transform: none;
  }
}

::-webkit-scrollbar {
  width: 13px;

  background-color: $white;

  &-track {
    background-color: $white;
    margin-block: 0.5em;
  }

  &-thumb {
    background-color: rgba(47, 47, 47, 0.836);
    border-radius: 100vw;
    transition: 0.4s;
    border: 4px solid $white;
    background-clip: padding-box;

    &:hover {
      background-color: rgb(28, 28, 28);
      transition: 0.4s;
    }
  }
}

@media only screen and (max-width: 550px) {
  .back-button {
    width: 80%;
  }
}
</style>
