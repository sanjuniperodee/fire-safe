<template>
  <div class="w-100 h-100">
    <div
      class="inspect-step"
      v-show="objectStore.currentStep === 1"
    >
      <ObjectOwnerEditStep1 />
    </div>
    <div
      class="inspect-step"
      v-show="objectStore.currentStep === 2"
    >
      <ObjectOwnerEditStep2 />
    </div>
    <div
      class="inspect-step"
      v-show="objectStore.currentStep === 3"
    >
      <ObjectOwnerEditStep3 />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useObjectStore } from '@/stores/ObjectStore'
import ObjectOwnerEditStep1 from './steps/ObjectOwnerEditStep1.vue'
import ObjectOwnerEditStep2 from './steps/ObjectOwnerEditStep2.vue'
import ObjectOwnerEditStep3 from './steps/ObjectOwnerEditStep3.vue'

const objectStore = useObjectStore()
</script>

<style lang="scss" scoped>
.inspect-step {
  padding: 20px 0 0 0;
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;
}
</style>
