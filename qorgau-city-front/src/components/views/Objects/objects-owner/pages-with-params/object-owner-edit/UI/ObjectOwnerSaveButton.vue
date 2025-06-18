<template>
  <v-btn
    @click="save"
    icon="mdi-content-save-all"
    :loading="objectInfoStore.isSaveLoading"
    size="large"
    class="text-white add-button"
    color="#5b9271"
  >
  </v-btn>
</template>

<script lang="ts" setup>
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { useRoute } from 'vue-router'

const route = useRoute()

const objectInfoStore = useObjectInfoStore()
const save = () => {
  objectInfoStore.saveObjectInfo(route.params.id as string)
}
</script>

<style lang="scss" scoped>
.add-button {
  position: fixed;
  z-index: 999;
  bottom: 71px;
  right: 30px;
}
</style>
