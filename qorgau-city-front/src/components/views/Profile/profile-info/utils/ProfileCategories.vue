<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { categories } from '@/utils/categoryList'
import { useProfileStore } from '@/stores/ProfileStore'
import { useUserStore } from '@stores/UserStore'
import { editField, cancelEditing, saveEditing } from '../utils/editFunctions'
import { userService } from '@/services/user.service'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'

const profileStore = useProfileStore()
const userStore = useUserStore()

const isEditing = computed(() => profileStore.items.categories.isEditing)
const isLoading = ref(false)
const tempCategories = ref<number[]>([...profileStore.items.categories.value])

const selectedCategory = ref<number | null>(null)

watch(() => profileStore.items.categories.value, (newCategories) => {
  if (!isEditing.value) {
    tempCategories.value = [...newCategories]
  }
}, { deep: true })

const editCategories = () => {
  editField('categories')
  tempCategories.value = [...profileStore.items.categories.value]
}

const saveCategories = async() => {
  isLoading.value = true
  try {
    await saveEditing('categories')

    const formData = new FormData()
    formData.append('categories', tempCategories.value.toString())
    await userService.updateUser(userStore.user!.id, formData)

    profileStore.items.categories.value = [...tempCategories.value]
    profileStore.items.categories.isEditing = false
  } finally {
    isLoading.value = false
  }
}

const cancelCategoriesEdit = () => {
  cancelEditing('categories')
  tempCategories.value = [...profileStore.items.categories.value]
}

const addCategory = (categoryId: number) => {
  if (!tempCategories.value.includes(categoryId)) {
    tempCategories.value.push(categoryId)
  }
}

const removeCategory = (categoryId: number) => {
  tempCategories.value = tempCategories.value.filter(id => id !== categoryId)
}

const getCategoryById = (id: number) => categories.find(cat => cat.id === id)
</script>

<template>
  <LoaderSpinner v-if="isLoading" />

  <div class="info__block-item">
    <div class="info__block-box">
      <v-card-title class="info__block-title">Категории</v-card-title>
      <v-btn
        v-if="!isEditing"
        @click="editCategories"
        icon="mdi-pencil"
        rounded="lg"
        size="x-small"
        color="#f57c01"
        class="text-white"
      ></v-btn>
      <div v-else class="info__editing-btns">
        <v-btn
          @click="saveCategories"
          icon="mdi-check-bold"
          rounded="lg"
          size="x-small"
          color="#5b9271"
          class="text-white"
        ></v-btn>
        <v-btn
          @click="cancelCategoriesEdit"
          icon="mdi-close"
          rounded="lg"
          size="x-small"
          color="#d20f0d"
          class="text-white"
        ></v-btn>
      </div>
    </div>

    <v-expansion-panels class="mb-6" focusable inset>
      <v-expansion-panel
        v-for="categoryId in (isEditing ? tempCategories : profileStore.items.categories.value)"
        :key="categoryId"
        hide-details
      >
        <v-expansion-panel-title>
          {{ getCategoryById(categoryId)?.name }}
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <div class="category-details">
            <p>{{ getCategoryById(categoryId)?.name }}</p>

            <p v-if="getCategoryById(categoryId)?.measurement_unit">
              ({{getCategoryById(categoryId)?.measurement_unit}})
            </p>
            <v-btn
              v-if="isEditing"
              color="error"
              @click="removeCategory(categoryId)"
              class="delete-btn"
            >
              Удалить категорию
            </v-btn>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-select
      v-if="isEditing"
      v-model="selectedCategory"
      :items="categories.map(cat => ({ title: cat.name, value: cat.id }))"
      label="Добавить категорию"
      @update:model-value="addCategory"
      class="add-category"
      variant="outlined"
    ></v-select>
  </div>
</template>

<style scoped>
.info__block-item {
  width: 100%;
  margin-top: 40px;
  padding: 1em;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info__block-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1em;
}

.info__editing-btns {
  display: flex;
  gap: 0.5em;
}

.v-expansion-panels {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.category-details {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.add-category {
  margin-top: 20px;
  width: 100%;
}

.delete-btn{
  width: 50%;
  margin-top: 10px;
}

@media only screen and (max-width: 768px) {
  .delete-btn{
    width: 100%;
  }
}

</style>
