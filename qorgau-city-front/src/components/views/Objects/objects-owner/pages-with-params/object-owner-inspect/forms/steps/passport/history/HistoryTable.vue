<template>
  <div>
    <v-btn
      style="margin-left: 20px; margin-bottom: 20px"
      @click="() => refreshHistory()"
      prepend-icon="mdi-refresh"
      color="#f57c01"
      variant="tonal"
    >
      <span style="padding-top: 4px"> Обновить </span>
    </v-btn>
    <!-- @vue-ignore -->
    <v-data-table
      :loading="isLoading"
      :items="items"
      :headers="headers"
    ></v-data-table>
  </div>
</template>

<script setup lang="ts">
import { formatDate } from '@/helpers/formatTime'
import { objectService } from '@/services/object.service'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

export type TableHistoryAction = {
  id: number
  action: string
  remark: string
  created_at: string
  updated_at: string
}

const snackbarStore = useSnackbarStore()

const headers = [
  {
    title: 'Дата создания',
    align: 'start',
    key: 'created_at'
  },
  { title: 'Действие', key: 'action', align: 'start', sortable: false },
  { title: 'Примечание', key: 'remark', align: 'start', sortable: false }
]

const items = ref<TableHistoryAction[]>([])

const isLoading = ref<boolean>(false)
const route = useRoute()

const refreshHistory = async () => await getObjectHistory()

const getObjectHistory = async () => {
  try {
    isLoading.value = true
    const data = await objectService.getHistories(route.params.id as string)
    const formattedData = data.map((item) => ({
      ...item,
      created_at: formatDate(new Date(item.created_at))!,
      updated_at: formatDate(new Date(item.updated_at))!
    }))
    // on success
    items.value = formattedData
    isLoading.value = false
  } catch (error) {
    isLoading.value = false
    snackbarStore.pullSnackbar('Не удалось получить доступ к этому паспорту ПБО.', 3000, '#d20f0d')
  }
}

onMounted(() => {
  getObjectHistory()
})
</script>

<style scoped></style>
