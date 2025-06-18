<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useStatementStore } from '@/stores/StatementsStore'
import { itemsPerPage, getTotalPages } from '@/utils/constants'
import Empty from '@components/empty/EmptyView.vue'

const router = useRouter()
const statementStore = useStatementStore()

const initialPage = ref(1)
const isLoading = ref(false)

const fetchData = async () => {
  const page = (initialPage.value - 1) * itemsPerPage
  await statementStore.getMyStatements(itemsPerPage, page)
}

const editCard = (cardId: number) => {
  router.push('/statement/edit/' + cardId)
}

watch(initialPage, async () => {
  await fetchData()
})

onMounted(async () => {
  await fetchData()
})
</script>

<template>
  <h1>Мои Заявки</h1>

  <Empty
    v-if="statementStore.myStatements?.length === 0"
    message="У вас нет созданных заявок"
  />

  <div class="statement-grid">
    <div
      v-for="statement in statementStore.myStatements"
      :key="statement.id"
      class="statement-grid-item"
    >
      <v-card class="statement-card">
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
          <v-col cols="8" class="d-flex flex-column justify-space-between">
            <v-card-text class="py-0 px-0 pl-4">
              <v-expansion-panels>
                <v-expansion-panel
                  v-for="category in statement.categories"
                  :key="category.id"
                >
                  <v-expansion-panel-title>{{category.name }}</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    {{ category.name }}
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
                  color="warning"
                  block
                  @click.stop="editCard(statement.id)"
                >
                  Редактировать
                </v-btn>
              </v-col>
<!--              <v-col-->
<!--                cols="3"-->
<!--                class="d-flex justify-end"-->
<!--              >-->
<!--                <v-btn-->
<!--                  class="action-button"-->
<!--                  title="Количество людей которые откликнулись"-->
<!--                  icon-->
<!--                  color="primary"-->
<!--                  @click.stop-->
<!--                  :loading="isLoading"-->
<!--                >-->
<!--                  <v-icon>mdi-message</v-icon>-->
<!--                  <span class="message-count">{{ 7 }}</span>-->
<!--                </v-btn>-->
<!--              </v-col>-->
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card>
    </div>
  </div>

  <v-pagination
    v-if="getTotalPages(statementStore.myStatementsCount) > 1"
    v-model="initialPage"
    :length="getTotalPages(statementStore.myStatementsCount)"
  ></v-pagination>
</template>

<style scoped lang="scss">
h1 {
  color: #212121;
  font-size: 24px;
  font-weight: 600;
  margin: 30px 0 0 30px;
}

.statement-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  align-items: start;
  gap: 20px;
  padding: 30px 30px 50px 30px;
  height: calc(100vh - 56px);
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

.message-count {
  position: absolute;
  top: -2px;
  right: 10px;
  background-color: #ff4040;
  color: white;
  border-radius: 50%;
  padding: 5px;
  font-size: 12px;
}
</style>