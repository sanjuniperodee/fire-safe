<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
import EducationModal from '@components/modal/providerModals/EducationModal.vue'
import ExperienceModal from '@components/modal/providerModals/ExperienceModal.vue'
import AchievementModal from '@/components/modal/providerModals/AchievementModal.vue'
import OtherAchievementsModal from '@/components/modal/providerModals/OtherAchievementsModal.vue'

import EducationEditModal from '@components/modal/providerModals/edit/EducationEditModal.vue'
import ExperienceEditModal from '@components/modal/providerModals/edit/ExperienceEditModal.vue'
import AchievementEditModal from '@/components/modal/providerModals/edit/AchievementEditModal.vue'
import OtherAchievementsEditModal from '@/components/modal/providerModals/edit/OtherAchievementsEditModal.vue'

import { useEducationStore } from '@stores/providerProfileStore/EducationStore'
import { useExperienceStore } from '@stores/providerProfileStore/ExperienceStore'
import { useAchievementStore } from '@stores/providerProfileStore/AchievementStore'
import { useOtherAchievementsStore } from '@stores/providerProfileStore/OtherAchievementsStore'

const educationStore = useEducationStore()
const experienceStore = useExperienceStore()
const achievementStore = useAchievementStore()
const otherAchievementsStore = useOtherAchievementsStore()

type ModalKeys =
  'Education' | 'Experience' | 'Achievement' | 'OtherAchievements'
  | 'EditEducation' | 'EditExperience' | 'EditAchievement' | 'EditOtherAchievements';

const selectedEducationId = ref<number | null>(null)
const selectedExperienceId = ref<number | null>(null)
const selectedAchievementId = ref<number | null>(null)
const selectedOtherAchievementId = ref<number | null>(null)

const openEditModal = (id: number, key: ModalKeys) => {
  switch (key) {
    case 'EditEducation':
      selectedEducationId.value = id
      break
    case 'EditExperience':
      selectedExperienceId.value = id
      break
    case 'EditAchievement':
      selectedAchievementId.value = id
      break
    case 'EditOtherAchievements':
      selectedOtherAchievementId.value = id
      break
  }
  modals.value[key] = !modals.value[key]
}

const modals = ref<Record<ModalKeys, boolean>>({
  Education: false,
  Experience: false,
  Achievement: false,
  OtherAchievements: false,
  EditEducation: false,
  EditExperience: false,
  EditAchievement: false,
  EditOtherAchievements: false,
})

const toggleModal = (key: ModalKeys) => {
  modals.value[key] = !modals.value[key]
}

const getMediaUrl = (media: File | Blob | string): string => {
  if (typeof media === 'string') {
    return media; // Если это уже строка (URL), возвращаем как есть
  } else if (media instanceof File || media instanceof Blob) {
    return URL.createObjectURL(media); // Создаем URL для объекта File или Blob
  } else {
    return ''; // На случай, если тип не подходит
  }
}

onMounted(() => {
  educationStore.getEducations()
  experienceStore.getExperiences()
  achievementStore.getAchievements()
  otherAchievementsStore.getOtherAchievements()
})

</script>

<template>
  <v-card-title class="info__title">Образование и опыт:</v-card-title>

  <div class="info__block">
    <div class="info__block-item">
      <strong>Образование</strong>
      <div class="plus" @click="toggleModal('Education')">
        <v-icon>mdi-plus</v-icon>
      </div>
    </div>
    <div v-if="educationStore.educations?.length !== 0" class="info__data">
      <div
        v-for="edu in educationStore.educations"
        :key="edu.id" class="info__data-item"
        @click="openEditModal(edu.id!, 'EditEducation')"
      >
        <img :src="getMediaUrl(edu.media)" alt="Education" class="info__data-image">
        <div class="info__data-text">
          <p>{{ edu.college_name }}</p>
          <p>{{ edu.year_start }} — {{ edu.year_end || 'н.в' }}</p>
        </div>
      </div>
    </div>

    <div class="info__block-item">
      <strong>Опыт работы</strong>
      <div class="plus" @click="toggleModal('Experience')">
        <v-icon>mdi-plus</v-icon>
      </div>
    </div>
    <div v-if="experienceStore.experiences?.length !== 0" class="info__data">
      <div
        v-for="exp in experienceStore.experiences"
        :key="exp.id" class="info__data-item"
        @click="openEditModal(exp.id!, 'EditExperience')"
      >
        <img :src="getMediaUrl(exp.media!)" alt="Experience" class="info__data-image">
        <div class="info__data-text">
          <p>{{ exp.company_name }}</p>
          <p>{{ exp.year_start }} — {{ exp.year_end || 'н.в' }}</p>
        </div>
      </div>
    </div>

    <div class="info__block-item">
      <strong>Достижения и грамоты</strong>
      <div class="plus" @click="toggleModal('Achievement')">
        <v-icon>mdi-plus</v-icon>
      </div>
    </div>
    <div v-if="achievementStore.achievements?.length !== 0" class="info__data">
      <div
        v-for="ach in achievementStore.achievements"
        :key="ach.id" class="info__data-item"
        @click="openEditModal(ach.id!, 'EditAchievement')"
      >
        <img :src="getMediaUrl(ach.media)" alt="Achievement" class="info__data-image">
        <div class="info__data-text">
          <p>{{ ach.certificate_name }}</p>
          <p>{{ ach.year_received }}</p>
        </div>
      </div>
    </div>

    <div class="info__block-item">
      <strong>Другие заслуги</strong>
      <div class="plus" @click="toggleModal('OtherAchievements')">
        <v-icon>mdi-plus</v-icon>
      </div>
    </div>
    <div v-if="otherAchievementsStore.otherAchievements?.length !== 0" class="info__data">
      <div
        v-for="other in otherAchievementsStore.otherAchievements"
        :key="other.id" class="info__data-item"
        @click="openEditModal(other.id!, 'EditOtherAchievements')"
      >
        <img :src="getMediaUrl(other.media)" alt="Other Achievement" class="info__data-image">
        <div class="info__data-text">
          <p>{{ other.name }}</p>
          <p>{{ other.year_start }} - {{ other.year_end || 'н.в' }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- CreateModals -->
  <EducationModal
    :show-modal="modals.Education"
    @close="toggleModal('Education')"
  />
<!--  @refresh="refresh('Education')"-->
  <ExperienceModal
    :show-modal="modals.Experience"
    @close="toggleModal('Experience')"
  />
  <AchievementModal
    :show-modal="modals.Achievement"
    @close="toggleModal('Achievement')"
  />
  <OtherAchievementsModal
    :show-modal="modals.OtherAchievements"
    @close="toggleModal('OtherAchievements')"
  />

  <!-- EditModals -->
  <EducationEditModal
    :id="selectedEducationId!"
    :show-modal="modals.EditEducation"
    @close="toggleModal('EditEducation')"
  />
  <ExperienceEditModal
    :id="selectedExperienceId!"
    :show-modal="modals.EditExperience"
    @close="toggleModal('EditExperience')"
  />
  <AchievementEditModal
    :id="selectedAchievementId!"
    :show-modal="modals.EditAchievement"
    @close="toggleModal('EditAchievement')"
  />
  <OtherAchievementsEditModal
    :id="selectedOtherAchievementId!"
    :show-modal="modals.EditOtherAchievements"
    @close="toggleModal('EditOtherAchievements')"
  />
</template>

<style scoped lang="scss">
.info {
  margin-top: 10em;
  padding-bottom: 4em;
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;

  &__title {
    padding: 0;
    width: 100%;
    font-size: 20px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 1em;
  }

  &__block {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    background-color: white;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 20px;
  }

  &__block-item {
    gap: 1em;
    display: flex;
    justify-content: space-between;
    width: 100%;

    & strong{
      font-size: 18px;
    }
  }

  &__data {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  &__data-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem;
    border-radius: 5px;
    background-color: white;
    cursor: pointer;
    transition: .2s ease-in-out;

    &:hover{
      background-color: #f5f5f5;
    }
  }

  &__data-image {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 5px;
  }

  &__data-text {
    display: flex;
    flex-direction: column;

    p:first-child {
      font-weight: bold;
    }

    p:last-child {
      color: #666;
    }
  }
}

.plus{
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  transition: .2s ease-in-out;
  cursor: pointer;

  &:hover{
    background-color: #e1e1e1;
  }
}

</style>