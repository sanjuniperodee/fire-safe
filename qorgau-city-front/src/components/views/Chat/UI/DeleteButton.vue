<template>
  <div class="delete-button" @click="handleDelete">
    <button class="delete-btn">Удалить</button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  onDelete: () => void
}>();

const handleDelete = () => {
  props.onDelete();
};
</script>

<style scoped>
.delete-button {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.delete-btn {
  background-color: #ff6f6f;
  border: none;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
}

.delete-btn:hover {
  background-color: #ff4c4c;
}
</style>