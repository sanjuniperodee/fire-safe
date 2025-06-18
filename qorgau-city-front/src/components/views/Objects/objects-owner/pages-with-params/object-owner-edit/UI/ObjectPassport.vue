<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useObjectStore } from '@/stores/ObjectStore'

const objectStore = useObjectStore()
const route = useRoute()
const isLoading = ref(false)
const errorMessage = ref('')

const generatePassport = async () => {
  try {
    isLoading.value = true
    await objectStore.getPdfDocument(Number(route.params.id))
    if (!objectStore.pdfDocuments || objectStore.pdfDocuments.length === 0) {
      await objectStore.createGeneratePdf(Number(route.params.id))
      await objectStore.getPdfDocument(Number(route.params.id))
    }
    objectStore.pdfDocuments = [...objectStore.pdfDocuments]
  } catch (error) {
    errorMessage.value = 'Ошибка при генерации паспорта'
    console.error('Error generating passport:', error)
  } finally {
    isLoading.value = false
  }
}

const pdfDocuments = computed(() => objectStore.pdfDocuments)

onMounted( async () => {
  objectStore.pdfDocuments = []
  await objectStore.getPdfDocument(Number(route.params.id))
})
</script>

<template>
  <div block class="passport-container">
    <div v-if="objectStore.pdfDocuments && objectStore.pdfDocuments.length > 0" class="documents-list">
      <div v-for="doc in pdfDocuments" :key="doc.id" class="document-item">
        <div class="document-info">
          <span class="document-date">
            {{ new Date(doc.created_at).toLocaleString() }}
          </span>
          <v-btn
            color="info"
            variant="text"
            :href="doc.download_url"
            target="_blank"
            prepend-icon="mdi-download"
          >
            Скачать паспорт
          </v-btn>
        </div>
      </div>
    </div>
    <v-btn
      color="primary"
      :loading="isLoading"
      @click="generatePassport"
      prepend-icon="mdi-file-document-outline"
      class="generate-btn"
    >
      Сгенерировать паспорт объекта
    </v-btn>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<style scoped lang="scss">
.passport-container {
  padding-top: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 1140px;
  margin: 0 auto;
  display: flex;
  justify-content: end;
  align-items: center;
}

.generate-btn {
  margin-bottom: 20px;
}

.error-message {
  color: #ff5252;
  margin: 10px 0;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}

.documents-list {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.document-item {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;

  &:last-child {
    border-bottom: none;
  }
}

.document-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-date {
  color: #666;
  font-size: 14px;
}
</style>