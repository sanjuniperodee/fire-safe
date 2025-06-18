<template>
  <div style="padding-top: 10px">
    <div class="step3__topics">
      <ObjectOwnerInspectModal
        :title="titleModal"
        :comment="commentModal"
        :comment_updated_date="commentUpdatedDate"
        :uuid="uuidModal"
        :inspector_comment="inspectorComment"
        :inspector_comment_updated_date="inspectorCommentDate" 
      />
      <v-btn
        v-if="isPassportCardSelected"
        variant="text"
        style="width: fit-content"
        prepend-icon="mdi-chevron-left"
        @click="() => goBackToCards()"
      >
        <span style="padding-top: 3px">Назад</span>
      </v-btn>
      <div
        v-if="!isPassportCardSelected"
        style="display: flex; width: 100%; align-items: center; flex-direction: column"
      >
        <CircularProgress
          class="circular__progress"
          :percentage="objectInfoStore.calculateGeneralProgress()"
        />
        <v-card-title
          style="font-size: 20px; text-align: center; margin: 0 0 40px 0"
          class="step3__subtitle"
          >Общий рейтинг</v-card-title
        >
      </div>
      <div
        v-if="!isPassportCardSelected"
        class="row"
      >
        <v-card
          elevation="3"
          v-for="(topic, index) in objectInfoStore.objectDocumentsInfo"
          :key="topic.title"
          class="topic-header"
          @click="() => updatePassportCardMap(topic.title)"
        >
          <SemiCircularProgress
            :icon="'mdi-' + PassportSecuritySystemTopicIconMap[topic.title as keyof typeof PassportSecuritySystemTopicIconMap]"
            :percentage="objectInfoStore.progressPercentage[index]"
          />
          <span
            style="
              font-weight: 500;
              font-size: 22px;
              width: 250px;
              text-align: center;
              margin-top: 16px;
            "
            class="step3__subtitle"
            >{{ topic.title }}</span
          >
        </v-card>
      </div>
      <div
        v-for="topic in objectInfoStore.objectDocumentsInfo"
        :key="topic.title"
        class="step3__topic"
      >
        <div
          v-if="topic.keys && passportCardMap[topic.title as keyof typeof passportCardMap]"
          class="step3__table-box"
        >
          <v-table class="table">
            <tbody class="table-body">
              <tr
                @click="openModal(key)"
                :style="{
                  'background-color': key.files.length > 0 ? '#d7ffb8' : '',
                  color: key.files.length > 0 ? '#58A700' : ''
                }"
                v-ripple
                v-for="key in topic.keys"
                :key="key.title"
              >
                <td
                  style="padding: 20px 10px"
                  class="table-body__td"
                >
                  {{ key.title }}
                </td>
                <td
                  class="table-body__td-status"
                  style="width: 200px"
                  :style="{ color: getRowColor(key.files.length) }"
                >
                  {{ key.files.length > 0 ? 'В наличии' : 'Не в наличии' }}
                </td>
              </tr>
            </tbody>
          </v-table>
        </div>
        <div v-if="passportCardMap[topic.title as keyof typeof passportCardMap]">
          <div
            v-if="topic.subParagraphs"
            class="step3__table-box"
          >
            <div
              v-for="subs in topic.subParagraphs"
              :key="subs.title"
            >
              <v-card-title class="step3__table-title">{{ subs.title }}</v-card-title>
              <v-table class="table">
                <tbody class="table-body">
                  <tr
                    @click="openModal(key)"
                    :style="{
                      'background-color': key.files.length > 0 ? '#d7ffb8' : '',
                      color: key.files.length > 0 ? '#58A700' : ''
                    }"
                    v-ripple
                    v-for="key in subs.keys"
                    :key="key.title"
                  >
                    <td
                      style="padding: 20px 10px"
                      class="table-body__td"
                    >
                      {{ key.title }}
                    </td>
                    <td
                      class="table-body__td-status"
                      style="width: 200px"
                      :style="{ color: getRowColor(key.files.length) }"
                    >
                      {{ key.files.length > 0 ? 'В наличии' : 'Не в наличии' }}
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ObjectOwnerInspectModal from '../modal/ObjectOwnerInspectModal.vue'
import { useObjectStore } from '@/stores/ObjectStore'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { useFileStore } from '@/stores/FileStore'
import { passportCardMap, PassportSecuritySystemTopicIconMap } from '@/types/ObjectBuilding'
import SemiCircularProgress from '@/components/progress/semi-circular-progress/SemiCircularProgress.vue'
import { onMounted } from 'vue'
import CircularProgress from '@components/progress/circular-progress/CircularProgress.vue'

const objectStore = useObjectStore()
const objectInfoStore = useObjectInfoStore()
const fileStore = useFileStore()

const titleModal = ref('')
const commentModal = ref('')
const commentUpdatedDate = ref<Date>()
const uuidModal = ref<number>(0)
const inspectorComment = ref('')
const inspectorCommentDate = ref<Date>()

const isPassportCardSelected = ref(false)

const updatePassportCardMap = (selectedTitle: string) => {
  isPassportCardSelected.value = true
  const updatedMap = Object.keys(passportCardMap.value).reduce((map, title) => {
    ;(map[title as keyof typeof map] as boolean) = false
    return map
  }, {})

  ;(updatedMap[selectedTitle as keyof typeof updatedMap] as boolean) = true
  passportCardMap.value = updatedMap as any
}

const goBackToCards = () => {
  isPassportCardSelected.value = false
  const updatedMap = Object.keys(passportCardMap.value).reduce((map, title) => {
    ;(map[title as keyof typeof map] as boolean) = false
    return map
  }, {})
  passportCardMap.value = updatedMap as any
}

const openModal = async (key: any) => {
  titleModal.value = key.title
  uuidModal.value = key.id
  commentModal.value = key.comment
  inspectorComment.value = key.inspector_comment
  inspectorCommentDate.value = key.inspector_comment_updated_date
  commentUpdatedDate.value = key.comment_updated_date
  objectStore.isKeyDialogOpen = true
  await fileStore.getFiles(key.files)
}

const getRowColor = (filesLength: number) => {
  return filesLength > 0 ? '#58A700' : '#d20f0d'
}

onMounted(() => {
  objectInfoStore.calculateProgressForEachTopic()
})
</script>

<style lang="scss" scoped>
.topic-header {
  padding: 30px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  flex-direction: column;
}

.topic-content {
  display: none;
}

.topic-content.active {
  display: block;
}

.row {
  display: grid;
  gap: 40px;
  justify-content: center;
  grid-template-columns: repeat(4, 1fr);
}

.step3 {
  width: 100%;

  &__topics {
    display: flex;
    flex-direction: column;
    padding-bottom: 5em;

    .circular__progress {
      margin-bottom: 40px;
    }
  }

  &__expansion-table-title {
    font-size: 18px;
  }

  &__table-box {
    display: flex;
    flex-direction: column;
    gap: 1em;
    margin-bottom: 2em;
    margin-top: 2em;
  }
}

.table-body {
  font-size: 16px;
}

.table {
  margin-left: 30px;
  width: 80%;
}

@media only screen and (max-width: 1104px) {
  .row {
    grid-template-columns: repeat(3, 1fr);
  }

  .table-body {
    &__td {
      min-width: auto;
      font-size: 12px;

      &-status {
        font-size: 12px;
      }
    }
  }

  .table {
    width: 100%;
    margin-left: 0;
  }

  .step3__table-title {
    font-size: 14px !important;
    hyphens: none !important;
    text-overflow: initial !important;
    white-space: initial;
  }

  .step3 {
    &__title {
      font-size: 16px !important;
      hyphens: none !important;
      text-overflow: initial !important;
      white-space: initial;
    }

    &__subtitle {
      font-size: 14px !important;
      hyphens: none !important;
      text-overflow: initial !important;
      white-space: initial;
    }

    &__expansion-tables {
      font-size: 14px !important;
    }

    &__expansion-table-title {
      font-size: 14px !important;
    }
  }
}

@media (max-width: 900px) {
  .row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .row {
    grid-template-columns: 1fr;
  }
}
</style>
