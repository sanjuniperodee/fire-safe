<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { statementService } from '@/services/statement.service'
import type { Media } from '@/types/Statement'
import { useRoute } from 'vue-router'
import { useStatementStore } from '@/stores/StatementsStore'
import LoaderInModal from '@/components/loader/LoaderInModal.vue'
import ConfirmationModal from '@components/modal/confirm/StatementDeleteConfirmation.vue'
import { categories as allCategories } from '@/utils/categoryList'
import GoBack from '@views/ProviderCabinet/UI/GoBack.vue'
import { useSnackbarStore } from '@stores/SnackbarStore'

const statementStore = useStatementStore()
const snackbarStore = useSnackbarStore()
const route = useRoute()

const uploadedFiles = ref<Media[]>([])
const filesToDelete = ref<number[]>([])
const newFiles = ref<File[]>([])

const loading = ref(false)
const isDeleteDialogOpen = ref(false)
const isAddCategoryDialogOpen = ref(false)

const toggleModal = () => {
  isDeleteDialogOpen.value = !isDeleteDialogOpen.value
}

const toggleAddCategoryDialog = () => {
  isAddCategoryDialogOpen.value = !isAddCategoryDialogOpen.value
}

onMounted(async () => {
  await statementStore.getMyStatementById(Number(route.params.id))
  if (statementStore.myStatement) {
    uploadedFiles.value = statementStore.myStatement.uploaded_media || []
  }
})

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    newFiles.value = Array.from(target.files)
  }
}

const removeFile = (id: number) => {
  uploadedFiles.value = uploadedFiles.value.filter((file) => file.id !== id)
  filesToDelete.value.push(id)
}

const categoryIds = computed(
  () => statementStore.myStatement?.categories.map((category) => category.id) || []
)

const addCategory = (categoryId: number) => {
  const categoryToAdd = allCategories.find((cat: any) => cat.id === categoryId)
  if (
    categoryToAdd &&
    !statementStore.myStatement?.categories.some((cat) => cat.id === categoryId)
  ) {
    statementStore.myStatement?.categories.push(categoryToAdd)
  }
  isAddCategoryDialogOpen.value = false
}

const removeCategory = (categoryId: number) => {
  if (statementStore.myStatement) {
    statementStore.myStatement.categories = statementStore.myStatement.categories.filter(
      (cat) => cat.id !== categoryId
    )
  }
}

const saveStatement = async () => {
  if (!statementStore.myStatement) return

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('text', statementStore.myStatement.text)
    formData.append('service_time', new Date(statementStore.myStatement.service_time).toISOString())
    formData.append('location', statementStore.myStatement.location)
    formData.append('min_price', statementStore.myStatement.min_price.toString())
    formData.append('max_price', statementStore.myStatement.max_price.toString())
    formData.append('categories', categoryIds.value.toString())
    formData.append('is_active', statementStore.myStatement.is_active.toString())
    formData.append('files_to_delete', filesToDelete.value.toString())

    // Add new files
    newFiles.value.forEach((file) => {
      formData.append('uploaded_media', file)
    })

    await statementService.editMyStatement(statementStore.myStatement.id, formData)
    snackbarStore.pullSnackbar('Заявка успешно обновлена!', 3000, '#5b9271')
  } catch (error) {
    console.error('Error saving statement:', error)
    snackbarStore.pullSnackbar('Не удалось обновить заявку!', 3000, '#d20f0d')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <LoaderInModal v-if="loading" />

  <v-container>
    <GoBack />

    <h1 class="text-h4 mb-6">Редактирование заявки №{{ statementStore.myStatement?.id }}</h1>

    <ConfirmationModal
      @close="toggleModal"
      :id="statementStore.myStatement?.id"
      :isDeleteDialogOpen="isDeleteDialogOpen"
    />

    <v-form
      @submit.prevent="saveStatement"
      v-if="statementStore.myStatement"
    >
      <v-text-field
        v-model="statementStore.myStatement.text"
        label="Описание"
        required
      ></v-text-field>

      <v-text-field
        v-model="statementStore.myStatement.location"
        label="Локация"
        required
      ></v-text-field>

      <v-text-field
        v-model="statementStore.myStatement.service_time"
        label="Время услуги"
        type="datetime-local"
        required
      ></v-text-field>

      <v-text-field
        v-model.number="statementStore.myStatement.min_price"
        label="Минимальная цена(тг)"
        type="number"
        required
      ></v-text-field>

      <v-text-field
        v-model.number="statementStore.myStatement.max_price"
        label="Максимальная цена(тг)"
        type="number"
        required
      ></v-text-field>

      <h2 class="text-h5 mt-6 mb-3">Категории</h2>
      <v-expansion-panels>
        <v-expansion-panel
          v-for="category in statementStore.myStatement.categories"
          :key="category.id"
        >
          <v-expansion-panel-title> Категория {{ category.id }} </v-expansion-panel-title>
          <v-expansion-panel-text>
            <p>{{ category.name }}</p>
            <p v-if="category.measurement_unit">
              Единица измерения: {{ category.measurement_unit }}
            </p>
            <v-btn
              color="error"
              @click="removeCategory(category.id)"
              class="mt-2"
            >
              Удалить категорию
            </v-btn>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>

      <v-btn
        color="primary"
        @click="toggleAddCategoryDialog"
        class="mt-4"
      >
        Добавить категорию
      </v-btn>

      <v-dialog
        v-model="isAddCategoryDialogOpen"
        max-width="500px"
      >
        <v-card>
          <v-card-title>Добавить категорию</v-card-title>
          <v-card-text>
            <v-select
              :items="allCategories"
              item-title="name"
              item-value="id"
              label="Выберите категорию"
              @update:model-value="addCategory"
            ></v-select>
          </v-card-text>
        </v-card>
      </v-dialog>

      <h2 class="text-h5 mt-6 mb-3">Медиа файлы</h2>

      <v-row class="mt-2">
        <v-col
          v-for="file in uploadedFiles"
          :key="file.id"
          cols="4"
        >
          <v-card>
            <v-img
              v-if="file.file_type === 'image'"
              :src="file.file"
              height="200"
              cover
            ></v-img>
            <video
              v-else-if="file.file_type === 'video'"
              :src="file.file"
              height="200"
              controls
            ></video>
            <v-card-title class="text-subtitle-2">{{ file.file_name }}</v-card-title>
            <v-card-actions>
              <v-btn
                color="error"
                @click="removeFile(file.id!)"
                >Удалить</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-file-input
        label="Загрузите фото/видео"
        multiple
        accept="image/png, image/jpeg, video/mp4, video/quicktime, video/avi"
        @change="handleFileChange"
        hide-input
        class="mt-4"
      ></v-file-input>

      <v-checkbox
        v-model="statementStore.myStatement.is_active"
        label="Активен"
      ></v-checkbox>

      <v-btn
        type="submit"
        color="primary"
        class="mr-4"
        :loading="loading"
      >
        Сохранить изменения
      </v-btn>

      <v-btn
        color="error"
        @click="toggleModal"
        :loading="loading"
      >
        Удалить заявку
      </v-btn>
    </v-form>
  </v-container>
</template>

<style scoped lang="scss">
.v-form {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
