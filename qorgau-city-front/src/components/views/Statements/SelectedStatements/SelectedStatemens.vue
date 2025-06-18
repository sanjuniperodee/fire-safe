<script setup lang="ts">
import { onActivated, onMounted, ref, watch } from 'vue'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import { useStatementStore } from '@/stores/StatementsStore'
import { useRouter } from 'vue-router'
import { itemsPerPage, getTotalPages } from '@/utils/constants'
import Empty from '@components/empty/EmptyView.vue'

const snackbarStore = useSnackbarStore()
const statementStore = useStatementStore()
const router = useRouter()

const isLoading = ref(false)
const initialPage = ref(1)

watch(initialPage, async () => {
  await fetchData()
})

const goToCard = (cardId: number) => {
  router.push('/statement/view/' + cardId)
}

const fetchData = async () => {
  const page = (initialPage.value - 1) * itemsPerPage
  await statementStore.getSelectedStatements(itemsPerPage, page)
}

const deleteCalledStatement = async (id: number) => {
  const page = (initialPage.value - 1) * itemsPerPage

  try {
    isLoading.value = true
    await statementStore.deleteCalledStatement(id)
    await statementStore.getSelectedStatements(itemsPerPage, page)
    isLoading.value = false
    snackbarStore.pullSnackbar('Заявка успешно удалена.', 3000, '#5b9271')
  } catch (error) {
    console.error(error)
    snackbarStore.pullSnackbar('Неудалось удалить заявку.', 3000, '#d20f0d')
  }
}

onMounted(fetchData)
onActivated(fetchData)
</script>

<template>
  <h1>Вы откликались на эти заявки</h1>

  <div class="empty" v-if="statementStore.selectedStatements?.length === 0">
    <Empty
      message="У вас нет выбранных заявок"
    />
  </div>


  <div class="statement-grid">
    <div
      v-for="statement in statementStore.selectedStatements"
      :key="statement.id"
      class="statement-grid-item"
    >
      <v-card class="statement-card" :color="statement.is_seen ? '#eaeaea' : '#ffffff'">
        <v-card-title class="text-center">{{ `Заявка №${statement.id} (${statement.text})` }}</v-card-title>
        <v-row no-gutters class="px-4 py-4">
          <v-col cols="4">
            <div class="image-container">
              <template v-if="statement.uploaded_media.length > 0">
                <template v-if="statement.uploaded_media[0].file_type === 'video'">
                  <video
                    :src="statement.uploaded_media[0].file"
                    controls
                    class="media"
                  >
                    Ваш браузер не поддерживает тег <code>video</code>.
                  </video>
                </template>
                <template v-else>
                  <v-img
                    :src="statement.uploaded_media[0].file"
                    :alt="statement.uploaded_media[0].file_name"
                    class="media"
                    cover
                  ></v-img>
                </template>
              </template>
            </div>
            <v-card color="grey-darken-3" class="price-card">
              <v-card-text class="text-center white--text">
                {{ statement.min_price }}тг - {{ statement.max_price }}тг
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="8" class="d-flex flex-column justify-space-between ">
            <v-card-text class="py-0 px-0 pl-4">
              <v-expansion-panels>
                <v-expansion-panel
                  v-for="category in statement.categories"
                  :key="category.id"
                >
                  <v-expansion-panel-title> {{ category.name }}</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <!-- {{ category.name }} -->
                    <p v-if="category.measurement_unit">
                      ({{category?.measurement_unit}})
                    </p>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>

            <v-card-actions class="button-container py-0 px-0">
              <v-col cols="9">
                <v-btn
                  class="action-button"
                  color="primary"
                  block
                  @click.stop="goToCard(statement.id)"
                >
                  Подробнее
                </v-btn>
              </v-col>
              <v-col
                cols="3"
                class="d-flex justify-end"
              >
                <v-btn
                  class="action-button"
                  title="Удалить из избранных"
                  icon
                  color="primary"
                  @click.stop="deleteCalledStatement(statement.id)"
                  :loading="isLoading"
                >
                  <v-icon>mdi-star</v-icon>
                </v-btn>
              </v-col>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card>
    </div>
  </div>

  <v-pagination
    v-if="getTotalPages(statementStore.selectedStatementsCount) > 1"
    v-model="initialPage"
    :length="getTotalPages(statementStore.selectedStatementsCount)"
  ></v-pagination>
</template>

<style scoped lang="scss">
h1 {
  color: #212121;
  font-size: 24px;
  font-weight: 600;
  margin: 30px 0 0 30px;
}

.empty{
  height: calc(100vh - 56px);
  overflow-y: scroll;
}

.statement-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  align-items: start;
  gap: 20px;
  // padding: 30px 30px 50px 30px;
  // height: calc(100vh - 56px);
  overflow-y: scroll;

  @media (max-width: 720px) {
    grid-template-columns: 1fr;
  }
}

.statement-grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.statement-card {
  display: flex;
  flex-direction: column;
  height: auto;
  width: 100%;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out;

  &:hover {
    transform: translateY(-5px);
  }

  .v-card-title {
    font-size: 1.25rem;
    font-weight: bold;
    padding: 16px;
    background-color: #ffffff;
  }

  .image-container {
    height: 200px;
    width: 100%;
    overflow: hidden;
  }

  .media {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .price-card {
    margin-top: 10px;
  }

  .v-card-text {
    padding: 16px;
  }

  .button-container {
    display: flex;
    padding: 16px;

    .v-btn {
      flex: 1;
      margin: 0 8px;
    }
  }
}

.v-expansion-panels {
  margin-bottom: 10px;
}

.v-btn {
  border-radius: 5px;
  font-size: 0.875rem;
  font-weight: 500;

  &.primary {
    background-color: #3f51b5;
    color: #ffffff;

    &:hover {
      background-color: #303f9f;
    }
  }

  &.warning {
    background-color: #ff9800;
    color: #ffffff;

    &:hover {
      background-color: #f57c00;
    }
  }
}




.action-button {
  font-size: 14px;
}
</style>