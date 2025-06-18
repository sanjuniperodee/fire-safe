<script setup lang="ts">
import { RouterView } from 'vue-router'
import DashboardVue from './components/dashboard/DashboardVue.vue'
import { useUserStore } from '@stores/UserStore'
import SnackbarNotify from './components/snackbar/SnackbarNotify.vue'

const userStore = useUserStore()
</script>

<template>
  <v-app>
    <div class="container">
      <v-locale-provider locale="ru">
        <div
          class="wrapper"
          :style="{ 'min-height': userStore.isAuthenticated ? 'calc(100vh - 56px)' : '100vh' }"
        >
          <SnackbarNotify />
          <RouterView />
        </div>
        <DashboardVue />
      </v-locale-provider>
    </div>
  </v-app>
</template>

<style lang="scss">
html {
  overflow: hidden !important;
}

body {
  overflow: hidden;
}

.container {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 100svh !important;
}

.wrapper {
  min-height: calc(100svh - 56px);
  display: flex;
  flex-direction: column;
  background-color: #fff;
}

::-webkit-scrollbar {
  width: 13px;

  background-color: transparent;

  &-track {
    background-color: transparent;
    margin-block: 0.5em;
  }

  &-thumb {
    background-color: rgba(47, 47, 47, 0.836);
    border-radius: 100vw;
    transition: 0.4s;
    border: 4px solid rgba(0, 0, 0, 0);
    background-clip: padding-box;

    &:hover {
      background-color: rgb(28, 28, 28);
      transition: 0.4s;
    }
  }
}
</style>
