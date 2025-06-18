<template>
  <ObjectOwnerEditStepLayout>
    <v-tabs
      v-model="tab"
      color="#f57c01"
      style="font-family: 'Montserrat', sans-serif"
      align-tabs="center"
    >
      <v-tab
        density="compact"
        value="passport"
        class="tab"
      >
        <v-icon style="margin-right: 4px">mdi-domain</v-icon>
        <span>Система обеспечения ПБ</span>
      </v-tab>
      <v-tab
        density="compact"
        value="history"
        class="tab"
      >
        <v-icon style="margin-right: 4px">mdi-history</v-icon>
        <span>История</span>
      </v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item value="passport">
        <PasspostSecuritySystem />
      </v-window-item>
      <v-window-item value="history">
        <PassportHistory />
      </v-window-item>
    </v-window>
  </ObjectOwnerEditStepLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ObjectOwnerEditStepLayout from '../UI/ObjectOwnerInspectStepLayout.vue'
import PasspostSecuritySystem from './passport/PassportSecuritySystem.vue'
import PassportHistory from './passport/PassportHistory.vue'

const tab = ref('passport')
</script>

<style lang="scss" scoped>
.tab {
  text-transform: none;
  font-weight: 700 !important;
  width: 300px;
  display: flex;
  align-items: center;

  & span {
    margin-bottom: -4px;
  }
}

@media only screen and (max-width: 1110px) {
  .tab {
    width: 160px;
    font-weight: 500 !important;
    font-size: 10px;
  }
}

@media only screen and (max-width: 634px) {
  .tab {
    width: 130px;
    font-weight: 500 !important;
    font-size: 8px;
  }
}
</style>
