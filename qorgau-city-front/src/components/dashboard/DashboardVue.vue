<template>
  <div>
    <v-bottom-navigation
      color="#f57c01"
      absolute
      grow
      :elevation="5"
      v-model="link"
    >
      <!--ALL-->
      <v-btn
        @click="goToPage"
        value="Map"
        prepend-icon="mdi-map-search"
        :active="link === 'Map'"
        stacked
        variant="text"
      >
        <span v-text="$t('map')"></span>
      </v-btn>
      <v-btn
        @click="goToPage"
        value="Faq"
        prepend-icon="mdi-frequently-asked-questions"
        :active="link === 'Faq'"
        stacked
        variant="text"
      >
        <span v-text="$t('faq')"></span>
      </v-btn>
      <v-btn
        v-if="!userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR) && !userStore.acceptedRoles.includes(UserRoleOptions.CITIZEN) || userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER) ||userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER)"
        value="Chat"
        :active="link === 'Chat'"
        @click="goToPage"
        stacked
        variant="text"
      >
        <span v-html="people"></span>
        <span v-text="$t('chats')"></span>
      </v-btn>
      <!--CITIZEN-->
      <v-btn
        @click="toggleModal"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.CITIZEN)
        && !userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        prepend-icon="mdi-account-search"
        stacked
        variant="text"
      >
        <span v-text="$t('connectInspector')"></span>
      </v-btn>

      <!--OBJECT_OWNER-->
      <v-btn
        :active="link === 'Objects'"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER)"
        value="Objects"
        @click="goToPage"
        prepend-icon="mdi-domain"
        stacked
        variant="text"
      >
        <span v-text="$t('objects')"></span>
      </v-btn>
      <v-btn
        :active="link === 'MyStatements'"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER)"
        value="MyStatements"
        @click="goToPage"
        stacked
        variant="text"
      >
        <span v-html="documentIcon2"></span>
        <span v-text="$t('myStatements')"></span>
      </v-btn>
      <!--PROVIDER-->
      <v-btn
        value="Statements"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER)"
        :active="link === 'Statements'"
        @click="goToPage"
        stacked
        variant="text"
      >
        <span v-html="documentIcon"></span>
        <span v-text="$t('statements')"></span>
      </v-btn>
      <v-btn
        value="SelectedStatements"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER)"
        :active="link === 'SelectedStatements'"
        @click="goToPage"
        stacked
        variant="text"
      >
        <span v-html="documentIcon2"></span>
        <span v-text="$t('selectedStatements')"></span>
      </v-btn>
      <!-- INSPECTOR -->
      <!-- <v-btn
        value="Citizens"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        :active="link === 'Citizens'"
        @click="goToPage"
        prepend-icon="mdi-account-group-outline"
        stacked
        variant="text"
      >
        <span v-text="$t('сitizens')"></span>
      </v-btn> -->
      <v-btn
        value="Providers"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        :active="link === 'Providers'"
        @click="goToPage"
        prepend-icon="mdi-tools"
        stacked
        variant="text"
      >
        <span v-text="$t('providers')"></span>
      </v-btn>
      <v-btn
        value="InspectorAllObjects"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        :active="link === 'InspectorAllObjects'"
        @click="goToPage"
        prepend-icon="mdi-domain"
        stacked
        variant="text"
      >
        <span v-text="$t('inspectorAllObjects')"></span>
      </v-btn>
      <v-btn
        value="InspectorNotedObjects"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        :active="link === 'InspectorNotedObjects'"
        @click="goToPage"
        prepend-icon="mdi-domain"
        stacked
        variant="text"
      >
        <span v-text="$t('inspectorNotedObjects')"></span>
      </v-btn>
      <v-btn
        value="Profile"
        v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        :active="link === 'Profile'"
        @click="goToPage"
        prepend-icon="mdi-account"
        stacked
        variant="text"
      >
        <span v-text="$t('profile')"></span>
      </v-btn>
      <!--PROFILE-->
      <v-btn
        value="Profile"
        v-if="!userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
        :active="link === 'Profile'"
        @click="goToPage"
        prepend-icon="mdi-account"
        stacked
        variant="text"
      >
        <span v-text="$t('profile')"></span>
      </v-btn>
    </v-bottom-navigation>

    <!-- Модальное окно -->
    <ConnectInspectorModal
      :showModal="showModal"
      @close="toggleModal"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref, watch } from 'vue'
import { useUserStore } from '@/stores/UserStore'
import { UserRoleOptions } from '@/types/User'
import { useI18n } from 'vue-i18n'
import ConnectInspectorModal from '@components/modal/ConnectInspectorModal.vue'
import { documentIcon, documentIcon2, people } from '@/assets/svg'

const { t } = useI18n()

const router = useRouter()
const userStore = useUserStore()
const currentUrl = window.location.pathname.split('/')[1]

const link = ref(currentUrl ? currentUrl[0].toUpperCase() + currentUrl.substring(1) : '')
const goToPage = () => {
  router.push({ name: link.value })
}

const showModal = ref(false)

const toggleModal = () => {
  showModal.value = !showModal.value
}


onMounted(async () => {
  await userStore.getUser()
  link.value = currentUrl ? currentUrl[0].toUpperCase() + currentUrl.substring(1) : ''
})
</script>

<style lang="scss" scoped>
.dashboard {
  z-index: -1;
  height: 56px;
}
</style>
