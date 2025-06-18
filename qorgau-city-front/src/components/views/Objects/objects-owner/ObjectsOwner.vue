<template>
  <div class="owner">
    <LoaderSpinner v-if="isLoading" />
    <div
      v-show="!isLoading"
      class="owner__content"
    >
      <ObjectAddForm />
      <div class="owner__title">{{ $t('pageTitle') }}</div>
      <div class="owner__row">
        <v-icon
          size="144"
          color="#71717a"
          >mdi-domain</v-icon
        >
        <div class="owner__subtitle">{{ $t('pageSubtitle') }}</div>
      </div>
      <div class="owner__object-count">
        {{ $t('objectCountLabel') }} {{ objectStore.objects.length }}
      </div>
      <transition-group
        tag="ul"
        name="list"
        class="owner__card-list"
        appear
      >
        <ObjectCard
          v-for="object in objectStore.objects"
          @click="(e) => goToCard(e, object.id)"
          :id="object.id"
          :rating="parseInt(object.rating)"
          :locationAddress="object.address"
          :IIN="object.iin"
          :organization-type="object.organization_type"
          :organization-name="object.organization_name"
          :key="object.id"
          :images="object.images"
        />
      </transition-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import ObjectAddForm from './object-add/ObjectAddForm.vue'
import { useObjectStore } from '@/stores/ObjectStore'
import ObjectCard from './object-card/ObjectCard.vue'
import { useRouter } from 'vue-router'
import LoaderSpinner from '@/components/loader/LoaderSpinner.vue'
import { onMounted, ref, watch } from 'vue'
import { useSnackbarStore } from '@/stores/SnackbarStore'

const objectStore = useObjectStore()
const router = useRouter()
const isLoading = ref(false)
const snackbarStore = useSnackbarStore()

const goToCard = (e: any, cardId: number) => {
  if (e.target.className.split(' ')[0] !== 'mdi-dots-horizontal') {
    router.push('/objects/edit/' + cardId)
  }
}

onMounted(async () => {
  try {
    isLoading.value = true
    await objectStore.getObjects()
    isLoading.value = false
  } catch (error) {
    snackbarStore.pullSnackbar(
      'Не удалось получить ваши паспорты ПБО. Попробуйте позже.',
      3000,
      '#d20f0d'
    )
    isLoading.value = false
  }
})

watch(
  () => objectStore.objects,
  async () => {
    // await objectStore.getObjects()
  },
  { deep: true }
)
</script>

<style lang="scss" scoped>
.owner {
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
    font-size: 32px;
    font-weight: 500;
    line-height: 1.4em;
  }

  &__card-list {
    margin-top: 3em;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
    gap: 16px;
  }
}

@media only screen and (max-width: 789px) {
  .owner {
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
}

// Animations

.list {
  &-enter-from {
    opacity: 0;
    transform: scale(0.6);
  }

  &-enter-to {
    opacity: 1;
    transform: scale(1);
  }

  &-enter-active {
    transition: all 0.4s ease;
  }

  &-leave-from {
    opacity: 1;
    transform: scale(1);
  }

  &-leave-to {
    opacity: 0;
    transform: scale(0.6);
  }

  &-leave-active {
    position: absolute;

    transition: all 0.4s ease;
  }

  &-move {
    transition: all 0.4s ease;
  }
}
</style>
