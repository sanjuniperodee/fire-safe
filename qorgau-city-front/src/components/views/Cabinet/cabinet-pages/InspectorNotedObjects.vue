<template>
  <div class="cabinet-info"><CabinetInfo /></div>
    <LoaderSpinner v-if="isLoading" />
    <div
      class="inspector"
      v-show="!isLoading"
    >
      <div class="inspector__title">Мои Объекты</div>
      <div class="inspector__row">
        <v-icon
          size="144"
          color="#71717a"
          >mdi-domain</v-icon
        >
        <div class="inspector__subtitle">
          На этой странице, вы как инспектор видите список закрепленных к вам Паспортов Пожарной
          Безопасности Объекта. Если на этой странице не имеется никаких паспортов, означает что к
          вам еще не прикрепили никакие объекты. Если у вас появились вопросы обратитесь к секции
          "FAQ" или обратить по контактному номеру +77474461966
        </div>
      </div>
      <div class="inspector__filter">
        <v-text-field
          label="Поиск"
          v-model="search"
          style="width: 400px"
          class="inspector__filter-input"
          variant="solo-filled"
          clearable
          append-icon="mdi-magnify"
        ></v-text-field>
      </div>
      <!-- @vue-ignore -->
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :search="search"
        :items="objectStore.myObjects"
        item-value="id"
        class="elevation-1"
      >
        <!-- eslint-disable-next-line vue/valid-v-slot -->
        <template v-slot:item.rating="{ item }">
          <v-chip
            style="min-width: 100px; justify-content: center"
            :color="getColor(item.rating)"
          >
            {{ ratingDescriptionMap[parseInt(item.rating) as keyof typeof ratingDescriptionMap] }}
          </v-chip>
        </template>

        <!-- eslint-disable-next-line vue/valid-v-slot -->
        <template v-slot:item.owner="{ item }">
          {{ getFullName(item) }}
        </template>

        <!-- eslint-disable-next-line vue/valid-v-slot -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex align-center ga-5">
            <v-btn
              @click="goTo(item.id)"
              class="text-white"
              style="padding: 4px 20px 0 20px"
              color="#f57c01"
            >
              Перейти
            </v-btn>
            <v-btn
              class="custom-btn"
              @click="deleteObject(item.id.toString())"
              title="Удалить с моих обьектов"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </div>
</template>

<script setup lang="ts">
import CabinetInspectorLayout from '@/layouts/CabinetInspectorLayout.vue'
import { ref } from 'vue'
import { useObjectStore } from '@stores/ObjectStore'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'
import { getColor } from '@/types/Map'
import { ratingDescriptionMap } from '@/types/Map'
import CabinetInfo from '@views/Cabinet/cabinet-info/CabinetInfo.vue'

const router = useRouter()

const objectStore = useObjectStore()
const isLoading = ref(false)

const getFullName = (item: any) => {
  if (item.owner) {
    return `${item.owner.last_name || ''} ${item.owner.first_name || ''} ${
      item.owner.middle_name || ''
    }`.trim()
  }
  return ''
}

const itemsPerPage = ref(10)
const headers = ref([
  { title: '№', align: 'start', sortable: false, key: 'id' },
  { title: 'Адрес местонахождения', align: 'start', key: 'address' },
  { title: 'Собственник объекта защиты', align: 'start', key: 'owner' },
  { title: 'ИИН / БИН', align: 'start', key: 'iin' },
  { title: 'Наименования организaции', align: 'start', key: 'organization_name' },
  { title: 'Безопасность', align: 'start', key: 'rating' },
  { title: '', key: 'actions', sortable: false }
])

const search = ref('')
const snackbarStore = useSnackbarStore()

const changeText = () => {
  const container = document.querySelector('.v-data-table-footer')
  const spans = container?.getElementsByTagName('span')
  for (let i = 0; i < spans!.length; i++) {
    const span = spans![i]

    if (span.textContent === 'Items per page:') {
      span.textContent = 'Количество объектов на страницу'
    } else if (span.textContent === 'All') {
      span.textContent = 'Всё'
    }
  }
}

const goTo = (objectId: number) => {
  router.push('/objects/view/' + objectId)
}

const deleteObject = async (id: string) => {
  try {
    isLoading.value = true
    await objectStore.deleteMyObjects(id)
    await objectStore.getMyObjects()
    isLoading.value = false
    snackbarStore.pullSnackbar('Обьект успешно удален.', 3000, '#5b9271')
  } catch (error) {
    console.error(error)
    snackbarStore.pullSnackbar('Неудалось удалить ваш обьект.', 3000, '#d20f0d')
  }
}

onMounted(async () => {
  try {
    isLoading.value = true
    await objectStore.getMyObjects()
    isLoading.value = false
  } catch (error) {
    snackbarStore.pullSnackbar(
      'Не удалось получить ваши паспорты ПБО. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
    isLoading.value = false
  }
  changeText()
})
</script>

<style lang="scss" scoped>
.inspector {
  font-family: 'Overpass', sans-serif;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow-y: scroll;
  height: calc(100vh - 56px);

  &__subtitle {
    color: #71717a;
    font-size: 18px;
    width: 70%;
    text-align: center;
  }

  &__row {
    display: flex;
    gap: 15px;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 30px;
  }

  &__title {
    font-size: 64px;
    font-weight: 500;
    line-height: 1.4em;
  }
}

.custom-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30px;
  height: 35px;
  color: #f15656;
}

@media only screen and (max-width: 1128px) {
  .inspector {
    padding: 50px 10px;
  }
}
@media only screen and (max-width: 789px) {
  .inspector {
    left: 0;
    padding: 0 10px;
  }

  .cabinet-info {
    display: none;
  }
}

@media only screen and (max-width: 528px) {
  .inspector {
    &__title {
      font-size: 32px;
    }

    &__filter-input {
      width: 250px !important;
    }
  }
}

.cabinet-info {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}
</style>
