<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal-content" @click.stop>
      <button @click="closeModal" class="close-btn">
        <span v-html="closeIcon"></span>
      </button>
      <img :src="imageUrl" alt="full-screen image" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { close as closeIcon } from '@/assets/svg';

defineProps<{
  visible: boolean;
  imageUrl: string;
}>();

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1010;
}

.modal-content img {
  max-width: 80dvw;
  max-height: 80dvh;
  object-fit: cover;
  border-radius: 10px;
}

.close-btn {
  position: absolute;
  color: white;
  top: 30px;
  right: 60px;
  font-weight: 400;
  cursor: pointer;
}
</style>