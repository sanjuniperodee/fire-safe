<template>
  <v-menu
    :close-on-content-click="false"
    style="padding: 0 !important"
    location="end top"
    transition="scale-transition"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        :loading="loadingRef"
        :disabled="disabledRef"
        style="width: 100%"
        color="#f57c01"
        append-icon="mdi-calendar-range"
        v-bind="props"
      >
        <span style="padding-top: 3px">
          {{ formatDateWithoutTime(value!) }}
        </span>
      </v-btn>
    </template>
    <v-list style="padding: 0 !important">
      <v-list-item style="width: 100%; padding: 0 !important">
        <v-date-picker
          :max="new Date()"
          style="width: 100%"
          v-model="valueRef"
          show-adjacent-months
          color="#f57c01"
        ></v-date-picker>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
import { formatDateWithoutTime } from '@/helpers/formatTime'
import { toRefs } from 'vue'
import { ref, watch } from 'vue'

const props = defineProps<{
  value: Date
  loading?: boolean
  disabled?: boolean
}>()

const { loading: loadingRef, disabled: disabledRef } = toRefs(props)

const valueRef = ref<Date>(props.value!)
const emit = defineEmits(['update:valueRef'])
watch(valueRef, (newValue) => {
  emit('update:valueRef', newValue)
})
</script>

<style scoped>
input[type='date'] {
  display: block;
  position: relative;
  padding: 1rem 3.5rem 1rem 0.75rem;
  width: 100%;
  font-size: 1rem;
  font-family: 'Overpass', sans-serif;

  color: #a5a5a5;
  border-radius: 0.25rem;
  background: #f6f6f6 url(./calendar-svg.svg) right 1rem center no-repeat;

  cursor: pointer;
}

input[type='date']::-webkit-input-placeholder {
  font-family: 'Overpass', sans-serif;
}

::-webkit-datetime-edit-fields-wrapper {
}

::-webkit-datetime-edit-month-field:hover,
::-webkit-datetime-edit-day-field:hover,
::-webkit-datetime-edit-year-field:hover {
  background: #d7d7d7;
}

::-webkit-datetime-edit-text {
  opacity: 0;
}

::-webkit-clear-button,
::-webkit-inner-spin-button {
  display: none;
}

::-webkit-calendar-picker-indicator {
  position: absolute;
  width: 3rem;
  height: 100%;
  top: 0;
  right: 0;
  bottom: 0;

  opacity: 0;
  cursor: pointer;

  color: #f6f6f6;
  background: #f6f6f6;
}

input[type='date']:hover::-webkit-calendar-picker-indicator {
  opacity: 0.05;
}

input[type='date']:hover::-webkit-calendar-picker-indicator:hover {
  opacity: 0.15;
}
</style>
