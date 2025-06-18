<template>
  <v-btn
    icon="mdi-download"
    size="large"
    class="download-btn"
    @click="downloadZip"
  >
    ZIP
  </v-btn>
</template>

<script setup lang="ts">
const props = defineProps<{
  organizationName: string
}>()

const downloadZip = () => {
  if (props.organizationName === 'ТОО АЗКО') {
    const link = document.createElement('a')
    link.href = '/zip/АЗКО.zip' // Путь к ZIP-файлу
    link.download = 'АЗКО.zip' // Имя файла для скачивания
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } else {
    console.log('Organization ZIP not found.')
  }
}
</script>

<style scoped lang="scss">
.download-btn {
  position: fixed;
  z-index: 999;
  bottom: 150px;
  right: 30px;
  background-color: #5b9271;
  color: white;
  padding: 5px;
}
</style>
