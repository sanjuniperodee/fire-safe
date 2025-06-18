<template>
  <div class="map-parent">
    <LoaderSpinner v-if="isLoading" />
    <div
      v-show="!isLoading"
      class="faq-body"
    >
      <div class="faq-body__title">{{ $t('faqTitle') }}</div>
      <div class="faq-body__row">
        <v-icon
          size="144"
          color="#71717a"
          >mdi-frequently-asked-questions</v-icon
        >
        <div class="faq-body__subtitle">{{ $t('faqSubtitle') }}</div>
      </div>
      <div class="faq-body__object-count">{{ $t('faqLabel') }}</div>

      <div class="faq-body__list">
        <v-expansion-panels>
          <v-expansion-panel
            class="faq-body__question"
            v-for="item in questions"
            :key="item.id"
          >
            <v-expansion-panel-title style="font-size: 24px; font-weight: bold">{{
              item.question
            }}</v-expansion-panel-title>
            <v-expansion-panel-text style="padding: 20px 20px 10px 20px; font-size: 18px">
              <span
                ><b>{{ $t('answerLabel') }}:</b></span
              >
              <br />
              <br />
              {{ item.answer }}
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Question } from '@/types/Question'
import { onMounted, ref } from 'vue'
import { questionService } from '../../../../services/question.service'
import { useUserStore } from '@stores/UserStore'
import { useSnackbarStore } from '@/stores/SnackbarStore'
import LoaderSpinner from '@components/loader/LoaderSpinner.vue'

const isLoading = ref(false)
const userStore = useUserStore()
const questions = ref<Question[]>([])
const snackbarStore = useSnackbarStore()

onMounted(async () => {
  await userStore.getUser()
  try {
    isLoading.value = true
    questions.value = await questionService.getQuestions()
    isLoading.value = false
  } catch (error) {
    snackbarStore.pullSnackbar(
      'Не удалось получить вопросы и ответы. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
    isLoading.value = false
  }
})
</script>

<style lang="scss" scoped>
.faq-body {
  font-family: 'Overpass', sans-serif;
  padding: 50px 70px;
  display: flex;
  flex-direction: column;
  overflow-y: scroll;
  height: 100%;

  &__title {
    font-size: 64px;
    font-weight: 500;
    line-height: 1.4em;
  }

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

  &__object-count {
    font-size: 24px;
    font-weight: 500;
    line-height: 1.4em;
    margin-bottom: 10px;
  }

  &__question {
  }
}

@media only screen and (max-width: 789px) {
  .faq-body {
    padding: 50px 10px;

    &__title {
      font-size: 48px;
    }

    &__object-count {
      font-size: 24px;
    }
  }
}

@media only screen and (max-width: 544px) {
  .faq-body {
    padding: 50px 10px;

    &__title {
      font-size: 32px;
    }

    &__object-count {
      font-size: 16px;
    }
  }
}
</style>
