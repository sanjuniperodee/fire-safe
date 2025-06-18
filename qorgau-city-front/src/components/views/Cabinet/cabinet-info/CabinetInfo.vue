<template>
  <div class="info">
    <div class="info__box">
      <div class="avatar-img">
        <CabinetAvatar />
      </div>
      <div class="info__block-item">
        <div class="info__block-box">
          <v-card-title
            class="info__block-title"
            @click="editProfile"
            style="cursor: pointer"
          >
            ФИО:
            {{ user.last_name }}
            {{ user.first_name }}
            {{ user.middle_name }}
          </v-card-title>

          <div
            class="info__inspector-block-box"
            v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
          >
            <v-card-title
              class="info__block-title"
              @click="editProfile"
              style="cursor: pointer"
            >
              Удостоверение CO №:
              {{ user.certificate_number }}
            </v-card-title>

            <v-card-title
              class="info__block-title"
              @click="editProfile"
              style="cursor: pointer"
            >
              Звание:
              {{ rankTypesMapping[user.rank as keyof typeof rankTypesMapping] }}
            </v-card-title>

            <v-card-title
              class="info__block-title"
              @click="editProfile"
              style="cursor: pointer"
            >
              Должность:
              {{ positionTypesMapping[user.position as keyof typeof positionTypesMapping]  }}
            </v-card-title>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import CabinetAvatar from './CabinetAvatar.vue'
import { useRouter } from 'vue-router'
import { UserRoleOptions,rankTypesMapping, positionTypesMapping, } from '@/types/User'
import { onMounted, computed } from 'vue'

const userStore = useUserStore()

const user = computed(
  () =>
    userStore.user || {
      last_name: '',
      first_name: '',
      middle_name: '',
      rank: 'Полковник(пример)',
      position: 'Участковый(пример)',
      certificate_number: '15935'
    }
)

const router = useRouter()

const editProfile = () => {
  router.push('/profile')
}

onMounted(async () => {
  await userStore.getUser()
})
</script>

<style scoped lang="scss">
.info {
  z-index: 10;
  background-color: white;
  padding: 10px;
  display: flex;
  min-width: 200px;
  height: auto;
  flex-direction: column;
  align-items: center;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);

  &__title {
    padding: 0;
    width: 100%;
    margin-bottom: 1em;
  }

  &__box {
    display: flex;
    gap: 10px;
    width: 100%;
  }

  &__block-item {
    gap: 1em;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
  }

  &__block-box,
  &__inspector-block-box {
    gap: 1em;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
  }

  &__block-title {
    font-size: 16px;
    padding: 0;
    cursor: pointer;
  }

  &__block-text {
    font-size: 14px;
    padding: 0;
  }
}

.avatar-img {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

@media only screen and (max-width: 720px) {
  .info {
    width: 100%;
    max-width: none;
    height: auto;

    &__block-item {
      width: 100%;
    }
  }
}
</style>
