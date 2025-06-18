<script setup lang="ts">
defineProps<{
  title: string
  handleFileChange: any
}>()

</script>

<template>
  <div class="file-upload-section">
    <strong>{{ title }}</strong>
    <label class="file-input-wrapper">
      <input
        type="file"
        accept="image/png, image/jpeg"
        @change="handleFileChange"
        class="hidden-file-input"
      >
      <div class="custom-input">
        <div class="plus-icon"></div>
      </div>
    </label>

  </div>
</template>

<style scoped lang="scss">
.file-upload-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
}

.file-input-wrapper {
  display: inline-block;
  width: 100px;
  height: 100px;
  cursor: pointer;
}

.hidden-file-input {
  display: none;
}

.custom-input {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #ccc;
  border-radius: 4px;
}

.plus-icon {
  width: 20px;
  height: 20px;
  position: relative;
}

.plus-icon::before,
.plus-icon::after {
  content: '';
  position: absolute;
  background-color: #ccc;
}

.plus-icon::before {
  width: 100%;
  height: 2px;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.plus-icon::after {
  width: 2px;
  height: 100%;
  left: 50%;
  top: 0;
  transform: translateX(-50%);
}

.file-preview {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-thumbnail {
  width: 80px;
  height: 60px;
  object-fit: cover;
  margin-right: 10px;
}

.delete-btn {
  color: #d54d5b;
}
</style>