<template>
  <div class="banner">
    <div
      v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
      class="banner__back"
    >
      <GoBack />
    </div>
    <LogoutButton class="banner__logout-button" />
    <ProfileAvatar class="banner__avatar" />
  </div>
</template>

<script setup lang="ts">
import ProfileAvatar from './UI/ProfileAvatar.vue'
import LogoutButton from './UI/LogoutButton.vue'
import GoBack from './UI/GoBack.vue'
import { useUserStore } from '@stores/UserStore'
import { UserRoleOptions } from '@/types/User'

const userStore = useUserStore()
</script>

<style lang="scss" scoped>
.banner {
  background-color: $orange;
  height: 200px;
  position: relative;
  z-index: 998;

  &__avatar {
    left: 50%;
    top: 100px;
    margin-left: -100px;
    position: absolute;
  }

  &__logout-button {
    position: absolute;
    right: 32px;
    top: 32px;
    z-index: 999;
  }

  &__back {
    position: absolute;
    left: 32px;
    top: 32px;
    z-index: 999;
  }
}
</style>
