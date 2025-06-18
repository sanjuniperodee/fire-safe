<template>
  <div style="padding-top: 10px">
    <div class="step3__topics">
      <div style="display: flex; width: 100%; align-items: center; flex-direction: column">
        <v-card-title
          style="font-size: 20px; text-align: center; margin: 0 0 40px 0"
          class="step3__subtitle"
        >
          Общий рейтинг
        </v-card-title>
      </div>
      <div class="row">
        <v-card
          elevation="3"
          v-for="(topic, index) in filteredTopics"
          :key="topic.title"
          class="topic-header"
          @click="() => navigateToCard(topic.title)"
        >
          <SemiCircularProgress
            class="semi-progress"
            :icon="'mdi-' + PassportSecuritySystemTopicIconMap[topic.title as keyof typeof PassportSecuritySystemTopicIconMap]"
            :percentage="objectInfoStore.progressPercentage[index]"
          />
          <span
            style="
              font-weight: 500;
              font-size: 18px;
              width: 100%;
              text-align: start;
              margin-top: 24px;
            "
            class="step3__title"
          >
            {{ topic.title }}
          </span>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { PassportSecuritySystemTopicIconMap } from '@/types/ObjectBuilding'
import SemiCircularProgress from '@/components/progress/semi-circular-progress/SemiCircularProgress.vue'

const router = useRouter()
const route = useRoute()
const objectInfoStore = useObjectInfoStore()

const navigateToCard = (cardTitle: string) => {
  // const formattedCardTitle = cardTitle.replace(/\s+/g, '')

  router.push({
    name: 'DocumentPage',
    params: { id: route.params.id, documentTitle: cardTitle }
  })
}

const filteredTopics = computed(() => {
  return objectInfoStore.objectDocumentsInfo.filter((topic) => topic.title.length > 2)
})

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
  grid-template-columns: repeat(auto-fill, minmax(20%, 1fr));
  gap: 10px;
}
.semi-progress {
  width: 100%;
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

  &__td-status {
    max-width: 300px;
    transition: 0.5s ease-in-out;
    cursor: pointer;
  }

  &__td-status:hover {
    background-color: #f5f5f5;
  }
}

.status-wrapper {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}
.status {
  cursor: pointer;
  white-space: nowrap;
}

.orderServiceBtn {
  color: #4d90fe;
  white-space: nowrap;
  cursor: pointer;
  transition: 0.5s ease-in-out;
}

.orderServiceBtn:hover {
  background-color: #f5f5f5;
}

.table {
  margin-left: 30px;
  width: 80%;
}

@media only screen and (max-width: 1104px) {
  .row {
    grid-template-columns: repeat(auto-fill, minmax(30%, 1fr));
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
@media only screen and (max-width: 876px) {
  .row {
    grid-template-columns: repeat(auto-fill, minmax(45%, 1fr));
  }
}
@media only screen and (max-width: 576px) {
  .row {
    grid-template-columns: repeat(auto-fill, minmax(50%, 1fr));
  }
}
</style>
