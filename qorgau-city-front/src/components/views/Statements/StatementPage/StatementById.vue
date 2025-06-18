<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useStatementStore } from '@stores/StatementsStore'
import { useRoute, useRouter } from 'vue-router'
import { formatStatementInfoDate } from '@/helpers/formatTime'
// import { noteStatement } from '../utils/noteStatement'
import { useSnackbarStore } from '@stores/SnackbarStore'

const route = useRoute()
const router = useRouter()
const statementStore = useStatementStore()
const snackbarStore = useSnackbarStore()


const goBack = () => {
  router.go(-1)
}

const goToPage = (route: string) => {
  router.push({ name: route })
}

const noteStatement = async (cardId: number) => {
  try {
    const data = await statementStore.noteStatement(cardId)
   
    goToPage('Chat')
   
    snackbarStore.pullSnackbar(
      'Отлик отправлен, заявка добавлена в "Избранные заявки"',
      3000,
      '#5b9271'
    )
  } catch (err) {
    snackbarStore.pullSnackbar('Не удалось отправить отклик!', 3000, '#d20f0d')
    console.error(err)
  }
}

const statement = computed(() => statementStore.statement)

onMounted(async () => {
  await statementStore.getStatementById(Number(route.params.id))
})
</script>

<template>
  <v-container
    fluid
    class="statement-page pa-4"
  >
    <div class="d-flex align-center ga-5">
      <v-btn
        variant="flat"
        style="text-transform: none; color: #333"
        prepend-icon="mdi-chevron-left"
        color="#f5f5f5"
        @click="goBack"
      >Вернуться</v-btn>

      <h1 class="text-h4 font-weight-medium">Заявка №{{ statement?.id }}</h1>
    </div>

    <v-row class="mt-9">
      <v-col
        cols="12"
        md="6"
      >
        <v-card class="statement-media">
          <v-carousel
            v-if="statement?.uploaded_media.length! > 1"
            hide-delimiters
            show-arrows="hover"
            height="400"
          >
            <v-carousel-item
              v-for="media in statement?.uploaded_media"
              :key="media.id"
            >
              <template v-if="media.file_type === 'image'">
                <v-img
                  :src="media.file"
                  :alt="media.file_name"
                  cover
                  height="400"
                ></v-img>
              </template>
              <template v-else-if="media.file_type === 'video'">
                <v-video
                  :src="media.file"
                  controls
                  height="400"
                  class="v-carousel-item__video"
                ></v-video>
              </template>
            </v-carousel-item>
          </v-carousel>

          <template v-else-if="statement?.uploaded_media.length === 1">
            <template v-if="statement.uploaded_media[0].file_type === 'image'">
              <v-img
                :src="statement.uploaded_media[0].file"
                :alt="statement.uploaded_media[0].file_name"
                cover
                height="400"
              ></v-img>
            </template>
            <template v-else-if="statement.uploaded_media[0].file_type === 'video'">
              <video
                :src="statement.uploaded_media[0].file"
                controls
                height="400"
                class="v-carousel-item__video"
              >
                <source
                  :src="statement.uploaded_media[0].file"
                  type="video/mp4"
                >
              </video>
            </template>
          </template>
        </v-card>
      </v-col>


      <v-col
        cols="12"
        md="6"
      >
        <div class="statement-content">
          <v-expansion-panels class="mb-6">
            <v-expansion-panel
              v-for="category in statement?.categories"
              :key="category.id"
            >
              <v-expansion-panel-title>  {{ category.name }} </v-expansion-panel-title>
              <v-expansion-panel-text>
                {{ category.measurement_unit }}
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <p class="statement-text mb-6">{{ statement?.text }}</p>

          <v-list>
            <v-list-item>
              <v-list-item-title>
                Время сервиса: {{ formatStatementInfoDate(statement?.service_time!) }}
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title> Локация: {{ statement?.location }} </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>
                Статус:
                <v-chip
                  :color="statement?.is_active ? 'success' : 'error'"
                  text-color="white"
                >
                  {{ statement?.is_active ? 'Активен' : 'Не активен' }}
                </v-chip>
              </v-list-item-title>
            </v-list-item>
          </v-list>

          <v-card
            class="statement-price my-6"
            color="grey-darken-3"
          >
            <v-card-text class="d-flex justify-space-between align-center">
              <span class="text-h6 white--text">Цена:</span>
              <span class="text-h6 white--text"
              >{{ statement?.min_price }}тг - {{ statement?.max_price }}тг</span
              >
            </v-card-text>
          </v-card>

              <div v-if="statement?.is_called"  block
                size="large"
                class="mt-4">
                <p 
                block
                size="large"
                class="mt-4 statment_text">ВЫ ОТКЛИКНУЛИСЬ</p>
              </div>
              <div v-else>
                <v-btn
                block
                size="large"
                class="mt-4"
                color="primary"
                @click.stop="noteStatement(statement!.id)"
              >
                Откликнуться
              </v-btn>
              </div>


          <!-- <v-btn
            @click.stop="noteStatement(statement!.id)"
            color="primary"
            block
            size="large"
            class="mt-4"
          >
            Откликнуться
          </v-btn> -->
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.statement-page {
  max-width: 1200px;
  margin: 0 auto;
  height: calc(100vh - 56px);
  overflow-y: scroll;
}

.statement-media {
  height: 400px;
}

.statement-text {
  font-size: 16px;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.87);
}

.statment_text{
    color: #50AF50;
    font-family: "Overpass", sans-serif;
    font-size: 14px;
    margin-right: 18px;
    text-align: center;
  }
</style>
