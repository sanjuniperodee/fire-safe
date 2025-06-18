<template>
  <div class="w-100 h-100">
    <div
      class="inspect-step"
      v-show="objectStore.currentStep === 1"
    >
      <ObjectOwnerInspectStep1 />
    </div>
    <div
      class="inspect-step"
      v-show="objectStore.currentStep === 2"
    >
      <ObjectOwnerInspectStep2 />
    </div>
    <div
      class="inspect-step"
      v-show="objectStore.currentStep === 3"
    >
      <ObjectOwnerInspectStep3 />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useObjectStore } from '@/stores/ObjectStore'
import ObjectOwnerInspectStep1 from './steps/ObjectOwnerInspectStep1.vue'
import ObjectOwnerInspectStep2 from './steps/ObjectOwnerInspectStep2.vue'
import ObjectOwnerInspectStep3 from './steps/ObjectOwnerInspectStep3.vue'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useObjectInfoStore } from '@stores/ObjectInfoStore'

const objectStore = useObjectStore()
</script>

<style lang="scss" scoped>
.inspect-step {
  padding: 40px 0;
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;
}

@media only screen and (max-width: 1104px) {
  .inspect-step {
    padding: 20px 0;
  }
}
</style>
