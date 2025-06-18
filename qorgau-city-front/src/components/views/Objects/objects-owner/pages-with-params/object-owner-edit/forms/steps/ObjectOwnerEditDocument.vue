<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { useObjectStore } from '@/stores/ObjectStore'
import { useFileStore } from '@/stores/FileStore'
import StatementModal from '@components/modal/StatementModal.vue'
import ObjectOwnerEditModal from '@views/Objects/objects-owner/pages-with-params/object-owner-edit/forms/steps/modal/ObjectOwnerEditModal.vue'

const route = useRoute()
const router = useRouter()
const objectInfoStore = useObjectInfoStore()
const objectStore = useObjectStore()
const fileStore = useFileStore()

const modal = ref(false)
const titleModal = ref('')
const commentModal = ref('')
const uuidModal = ref(0)
const inspectorCommentModal = ref('')
const inspectorCommentUpdDate = ref<Date>()

const cardTitle = computed(() => decodeURIComponent(route.params.documentTitle as string))

const currentTopic = computed(() =>
  objectInfoStore.objectDocumentsInfo.find((topic) => topic.title === cardTitle.value)
)

const goBack = () => {
  router.push({ name: 'ObjectOwnerEdit', params: { id: route.params.id } })
}

const getRowColor = (filesLength: number) => {
  return filesLength > 0 ? '#58A700' : '#d20f0d'
}

const openModal = async (key: any) => {
  titleModal.value = key.title
  uuidModal.value = key.id
  commentModal.value = key.comment
  inspectorCommentModal.value = key.inspector_comment
  inspectorCommentUpdDate.value = key.inspector_comment_updated_date
  objectStore.isKeyDialogOpen = true
  await fileStore.getFiles(key.files)
}

const toggleModal = () => {
  modal.value = !modal.value
}

onMounted(() => {
  objectInfoStore.calculateProgressForEachTopic()
})
</script>

<template>
  <div class="card-detail">
    <v-btn
      variant="text"
      style="width: fit-content"
      prepend-icon="mdi-chevron-left"
      class="back-btn"
      @click="goBack"
    >
      <p>Назад</p>
      <h2 class="card-title">{{ cardTitle }}</h2>
    </v-btn>

    <div
      v-if="currentTopic"
      class="step3__table-box"
    >
      <v-table class="table">
        <tbody class="table-body">
          <tr
            v-for="(key, index) in currentTopic.keys"
            :key="key.title"
            :style="{
              'background-color': key.files && key.files.length > 0 ? '#d7ffb8' : '',
              color: key.files && key.files.length > 0 ? '#58A700' : ''
            }"
            v-ripple
          >
            <td
              style="padding: 10px 0"
              class="table-body__td"
            >
              {{ index + 1 }}
            </td>
            <td
              style="padding: 20px 10px"
              class="table-body__td"
            >
              {{ key.title }}
            </td>
            <td
              v-if="key.files && key.files.length"
              @click="openModal(key)"
              class="table-body__td-status"
              :style="{ color: getRowColor(key.files ? key.files.length : 0) }"
            >
              В наличии
            </td>
            <td
              v-if="!key.files || !key.files.length"
              class="table-body__td-status-not"
              @click="openModal(key)"
            >
              <p>Не в наличии</p>
            </td>
            <td
              v-if="!key.files || !key.files.length"
              class="table-body__td-status-not"
              @click="toggleModal"
            >
              <button class="orderServiceBtn">Заказать услугу</button>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <div
      v-if="currentTopic.subParagraphs"
      class="step3__table-box"
    >
      <div
        v-for="subs in currentTopic.subParagraphs"
        :key="subs.title"
      >
        <v-card-title class="step3__table-title">{{ subs.title }}</v-card-title>
        <v-table class="table">
          <tbody class="table-body">
            <tr
              v-for="(key, index) in subs.keys"
              :style="{
                'background-color': key.files.length > 0 ? '#d7ffb8' : '',
                color: key.files.length > 0 ? '#58A700' : ''
              }"
              v-ripple
              :key="key.title"
            >
            <td
              style="padding: 10px 0"
              class="table-body__td"
            >
              {{ index + 1 }}
            </td>
              <td class="table-body__td">
                {{ key.title }}
              </td>
              <td
                v-if="key.files && key.files.length"
                @click="openModal(key)"
                class="table-body__td-status"
                :style="{ color: getRowColor(key.files ? key.files.length : 0) }"
              >
                В наличии
              </td>
              <td
                v-if="!key.files || !key.files.length"
                class="table-body__td-status-not"
                @click="openModal(key)"
              >
                <p>Не в наличии</p>
              </td>
              <td
                v-if="!key.files || !key.files.length"
                class="table-body__td-status-not"
                @click="toggleModal"
              >
                <button class="orderServiceBtn">Заказать услугу</button>
              </td>
            </tr>
          </tbody>
        </v-table>
      </div>
    </div>

    <ObjectOwnerEditModal
      :title="titleModal"
      :comment="commentModal"
      :uuid="uuidModal"
      :inspector_comment="inspectorCommentModal"
      :inspector_comment_updated_date="inspectorCommentUpdDate"
    />
    <StatementModal
      :show-modal="modal"
      @close="toggleModal"
    />
  </div>
</template>

<style lang="scss" scoped>
.card-detail {
  padding: 20px 50px;
  height: calc(100vh - 56px);
  overflow-y: scroll;
}

.back-btn p {
  padding-top: 3px;
}

.back-btn h2 {
  padding-top: 3px;
  margin-left: 20px;
}

.card-title {
  height: 100%;
}

.step3__table-box {
  margin-top: 20px;
}

.table {
  width: 100%;
}

.table-body {
  &__td {
    max-width: 300px;
    padding: 20px 10px;
  }

  &__td-status {
    width: 200px;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #bde88c;
    }
  }
  &__td-status-not {
    width: 200px;
    color: #d20f0d;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #f5f5f5;
    }
  }
}

.orderServiceBtn {
  color: #4d90fe;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #f5f5f5;
  }
}

@media only screen and (max-width: 1104px) {
  .table-body {
    &__td,
    &__td-status {
      font-size: 12px;
    }
  }
}
@media only screen and (max-width: 767px) {
  .card-detail {
    padding: 10px 20px;
  }
}
</style>
