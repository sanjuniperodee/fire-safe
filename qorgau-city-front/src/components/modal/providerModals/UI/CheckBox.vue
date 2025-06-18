<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  label: string;
  showPhotoToClients: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:showPhotoToClients', value: boolean): void;
}>();

const isChecked = ref(props.showPhotoToClients);

watch(() => props.showPhotoToClients, (newVal) => {
  isChecked.value = newVal;
});

const toggleSwitch = () => {
  isChecked.value = !isChecked.value;
  emit('update:showPhotoToClients', isChecked.value);
};
</script>

<template>
  <label class="switch">
    <label>{{ label }}</label>
    <input type="checkbox" class="checkbox" :checked="isChecked" @change="toggleSwitch" />
    <div class="slider"></div>
  </label>
</template>

<style scoped lang="scss">
.switch{
  margin-top: 20px;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.checkbox {
  display: none;
}

.slider {
  width: 60px;
  height: 30px;
  background-color: lightgray;
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  align-items: center;
  border: 4px solid transparent;
  transition: .3s;
  box-shadow: 0 0 10px 0 rgb(0, 0, 0, 0.25) inset;
  cursor: pointer;
}

.slider::before {
  content: '';
  display: block;
  width: 100%;
  height: 100%;
  background-color: #fff;
  transform: translateX(-30px);
  border-radius: 20px;
  transition: .3s;
  box-shadow: 0 0 10px 3px rgb(0, 0, 0, 0.25);
}

.checkbox:checked ~ .slider::before {
  transform: translateX(30px);
  box-shadow: 0 0 10px 3px rgb(0, 0, 0, 0.25);
}

.checkbox:checked ~ .slider {
  background-color: #2196F3;
}

.checkbox:active ~ .slider::before {
  transform: translate(0);
}
</style>