<script setup lang="ts">
import { onMounted, onActivated, ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStatementStore } from '@stores/StatementsStore'
import { itemsPerPage, getTotalPages } from '@/utils/constants'
// import { noteStatement } from './utils/noteStatement'
import { initDB } from '@/utils/idbUtils'
import { useSnackbarStore } from '@stores/SnackbarStore'
import { useChatStore } from '@stores/ChatStore'

const statementStore = useStatementStore()
const router = useRouter()
const initialPage = ref(1)
const pageForFilter = ref(0)
const search = ref('')

// 
const snackbarStore = useSnackbarStore()
const chatStore = useChatStore()

const goToPage = (route: string) => {
  router.push({ name: route })
}

const emit = defineEmits<{
  (e: 'sendMessage', text: string): void
}>();

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



const fetchData = async () => {
  const page = (initialPage.value - 1) * itemsPerPage
  await statementStore.getAllStatements(itemsPerPage, page)
  pageForFilter.value = page
}

const goToCard = (cardId: number) => {
  router.push('/statement/view/' + cardId)
}

const filteredStatements = computed(() => {
  return statementStore.statements.filter(statement =>
    statement.text.toLowerCase().includes(search.value.toLowerCase()) ||
    statement.id.toString().includes(search.value)
  )
})

watch(initialPage, fetchData)

onMounted(async () => {
  await initDB()
  await fetchData()
})
onActivated(fetchData)
</script>

<template>
  <div class="allStatements-wrapper">
    <div class="group">
      <svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><g><path d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"></path></g></svg><svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><g><path d="M21.53 20.47l-3.66-3.66C19.195 15.24 20 13.214 20 11c0-4.97-4.03-9-9-9s-9 4.03-9 9 4.03 9 9 9c2.215 0 4.24-.804 5.808-2.13l3.66 3.66c.147.146.34.22.53.22s.385-.073.53-.22c.295-.293.295-.767.002-1.06zM3.5 11c0-4.135 3.365-7.5 7.5-7.5s7.5 3.365 7.5 7.5-3.365 7.5-7.5 7.5-7.5-3.365-7.5-7.5z"></path></g></svg>
      <input placeholder="Поиск заявок" type="search" v-model="search" class="input">
    </div>

    <v-col
      v-for="statement in filteredStatements"
      :key="statement.id"
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
                  <v-expansion-panel-title>{{ category.name }}</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <p>{{ category.name }}</p>
                    <p v-if="category.measurement_unit">
                      ({{ category?.measurement_unit }})
                    </p>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-text>

            <v-card-actions class="button-container py-0 px-0">
              <v-btn
                color="primary"
                class="flex-grow-1"
                @click.stop="goToCard(statement.id)"
              >
                Подробнее
              </v-btn>
              <div v-if="statement.is_called">
                <p  class="statment_text">ВЫ ОТКЛИКНУЛИСЬ</p>
              </div>
              <div v-else>
                <v-btn
                color="warning"
                class="flex-grow-1"
                @click.stop="noteStatement(statement.id)"
              >
                Откликнуться
              </v-btn>
              </div>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card>
    </v-col>

    <v-pagination
      v-if="getTotalPages(statementStore.statementsCount) > 1"
      v-model="initialPage"
      :length="getTotalPages(statementStore.statementsCount)"
    ></v-pagination>
  </div>
</template>

<style scoped lang="scss">
.allStatements-wrapper {
  display: flex;
  flex-direction: column;
  width: 50%;
  margin-top: 50px;
  height: calc(100vh - 56px);
  overflow-y: auto;
  padding: 0;
  border-radius: 10px;
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

  .statment_text{
    color: #50AF50;
    font-family: "Overpass", sans-serif;
    font-size: 14px;
    margin-right: 18px;
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

//SEARCH STYLE
.group {
  display: flex;
  line-height: 28px;
  align-items: center;
  position: relative;
  width: 100%;
  padding: 0 12px;
}

.input {
  width: 100%;
  height: 40px;
  line-height: 28px;
  padding: 0 1rem 0 2.5rem;
  border: 2px solid transparent;
  border-radius: 8px;
  outline: none;
  background-color: white;
  color: #0d0c22;
  transition: .3s ease;
}

.input::placeholder {
  color: #9e9ea7;
}

.input:focus, input:hover {
  outline: none;
  border-color: rgb(224, 224, 224);
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(147, 147, 147, 0.1);
}

.icon {
  position: absolute;
  left: 1rem;
  fill: #9e9ea7;
  width: 1rem;
  height: 1rem;
}

.searchGlass{
  width: 24px;
}

@media only screen and (max-width: 920px) {
  .allStatements-wrapper {
    width: 90%;
    margin: 0;
    overflow: visible;
  }
}
</style>