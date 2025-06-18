<script setup lang="ts">
import { ref } from 'vue'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { useObjectStore } from '@stores/ObjectStore'
import type { RemarkContent } from '@/types/ObjectBuilding'

const snackbarStore = useSnackbarStore()
const objectStore = useObjectStore()

const remarkText = ref<string>('')

const props = defineProps<{
  id: string
  showModal: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const toggleModal = () => {
  emit('close')
}

const remark = async () => {
  const body: RemarkContent= {
    content: remarkText.value,
  }
  console.log(remarkText.value, props.id)
  try {
    await objectStore.createRemark(props.id, body)
    snackbarStore.pullSnackbar('Примечание успешно сохранено.', 3000, '#5b9271')
  } catch (error) {
    console.error(error)
    snackbarStore.pullSnackbar('Неудалось сохранить примечание.', 3000, '#d20f0d')
  }
}
</script>

<template>
  <div class="modal-wrapper" v-if="showModal">
    <div class="modal">
      <button
        @click="toggleModal"
        class="close-btn"
      >&times;</button>

      <v-card-title class="title">Примечание</v-card-title>

      <div class="textInputWrapper">
        <input
          v-model="remarkText"
          placeholder="Примечание"
          type="text"
          class="textInput"
          required
        />
      </div>

      <v-btn
        @click="remark"
        variant="elevated"
        class="save-btn"
      >
        Сохранить
      </v-btn>
    </div>
  </div>
</template>

<style scoped lang="scss">
.modal-wrapper{
  position: fixed;
  top: 0;
  left: 0;
  width: 100dvw;
  height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1002;
}

.modal{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 30px;
  position: relative;
  background-color: white;
  padding: 8px 16px;
  border-radius: 5px;
  max-width: 700px;
  width: 600px;
  min-height: 150px;
}

.title {
  padding: 8px 0;
  font-weight: bold;
  font-size: 24px;
}

.close-btn {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 10px;
  right: 10px;
  padding: 3px 5px 0 5px;
  border-radius: 5px;
  background: none;
  border: none;
  font-size: 26px;
  cursor: pointer;
  transition: .2s ease-in-out;

  &:hover{
    background-color: #ececec;
  }
}

.save-btn{
  width: 25%;
  padding: 8px 16px;
  background-color: #5b9170;
  color: white;
  left: 75%;
}

// INPUT

.textInputWrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  width: 100%;
  --accent-color: #ff9800;
}

.textInputWrapper:before,
.textInputWrapper:after {
  content: '';
  left: 0;
  right: 0;
  position: absolute;
  pointer-events: none;
  bottom: -1px;
  z-index: 4;
  width: 100%;
}

.textInputWrapper:before {
  transition: border-bottom-color 200ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  border-bottom: 1px solid rgba(255, 255, 255, 0.42);
}

.textInputWrapper:focus-within:before {
  border-bottom: 1px solid var(--accent-color);
  transform: scaleX(1);
}

.textInputWrapper:after {
  content: '';
  transform: scaleX(0);
  transition: transform 250ms cubic-bezier(0, 0, 0.2, 1) 0ms;
  will-change: transform;
  border-bottom: 2px solid var(--accent-color);
  border-bottom-color: var(--accent-color);
}

.textInputWrapper:focus-within:after {
  border-bottom: 2px solid var(--accent-color);
  transform: scaleX(1);
}

.textInput::placeholder {
  transition: opacity 250ms cubic-bezier(0, 0, 0.2, 1) 0ms;
  opacity: 1;
  user-select: none;
  color: rgba(255, 255, 255, 0.582);
}

.textInputWrapper .textInput {
  border-radius: 5px 5px 0 0;
  box-shadow: 0 2px 5px rgb(35 35 35 / 30%);
  max-height: 36px;
  background-color: #ffffff; /* Белый цвет */
  transition-timing-function: cubic-bezier(0.25, 0.8, 0.25, 1);
  transition-duration: 200ms;
  transition-property: background-color;
  color: #000000; /* Черный цвет текста */
  font-size: 14px;
  font-weight: 500;
  padding: 12px;
  width: 100%;
  border-left: none;
  border-bottom: none;
  border-right: none;
}

.textInputWrapper .textInput:focus,
.textInputWrapper .textInput:active {
  outline: none;
}

.textInputWrapper:focus-within .textInput::placeholder {
  opacity: 0;
}
</style>