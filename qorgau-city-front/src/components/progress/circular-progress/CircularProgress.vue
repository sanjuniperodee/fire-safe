<template>
  <div style="width: fit-content">
    <div
      class="circular-progress"
      :style="progressStyle"
      v-ripple
    >
      <span class="progress-value">{{ percentage }}%</span>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

const props = defineProps({
  percentage: {
    type: Number,
    required: true,
    default: 0
  }
})

const progressStyle = computed(() => ({
  background: `conic-gradient(#5b9271 ${props.percentage}%, #d20f0d 0deg)`
}))
</script>

<style scoped>
.circular-progress {
  position: relative;
  height: 140px;
  width: 140px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.circular-progress::before {
  content: '';
  position: absolute;
  height: 120px;
  width: 120px;
  border-radius: 50%;
  background-color: #fff;
}

.progress-value {
  position: relative;
  font-size: 18px;
  font-weight: 600;
  color: #000;
}
</style>
