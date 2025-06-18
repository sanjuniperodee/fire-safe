<template>
  <div class="card-container">
    <v-card
      v-ripple
      class="card"
      variant="tonal"
    >
      <v-avatar
        class="card__avatar"
        size="70"
        rounded
      >
      <img
      v-if="images && images.length !== 0"
      :src="images[0]?.image"
      class="avatar-img"
      alt="Аватар Обьекта"
      />

        <div v-else>
          <v-icon size="70">mdi-home-city</v-icon>
        </div>
      </v-avatar>
      <div class="card__text">
        <v-card-title
          class="card__loc-adress"
          style="padding: 0"
          >{{ locationAddress }}</v-card-title
        >
        <div class="card__organization-name">
          {{ $t('organizationNameLabel') }} {{ organizationType }} {{ organizationName }}
        </div>
        <div class="card__iin">{{ $t('IINLabel') }} {{ IIN }}</div>
      </div>
      <object-card-more-menu
        :id="id"
        class="card__more"
      />
      <div
        class="card__rating"
        :style="{ color: ratingColor }"
      >
        <v-icon>mdi-star</v-icon>
        <span style="padding-top: 2px">{{ ratingDescription }}</span>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import ObjectCardMoreMenu from './UI/ObjectCardMoreMenu.vue'
import { ratingDescriptionMap, ratingColors } from '@/types/Map'
import {
  type OrganizationTypes,
  type OrganizationTypeObject,
} from '@/types/ObjectBuilding'
import { computed } from 'vue'
import type { Avatar } from '@/types/ObjectBuilding'

const props = defineProps<{
  rating: number
  id: number
  locationAddress: string
  organizationType: OrganizationTypeObject
  organizationName: string
  IIN: string
  images: Avatar[]
}>()

const ratingColor = computed(() => ratingColors[props.rating as keyof typeof ratingColors])
const ratingDescription = computed(
  () => ratingDescriptionMap[props.rating as keyof typeof ratingDescriptionMap]
)

</script>

<style lang="scss" scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;

  .card {
    height: 200px;
    width: 100%;
    position: relative;
    display: flex;
    align-items: center;
    flex-direction: row;

    &__avatar {
      margin: 20px;

      & .avatar-img {
        margin: 20px;
        width: 70px;
        height: 70px;
        border-radius: 5px;
        object-fit: cover;
      }
    }

    &__more {
      position: absolute;
      top: 2px;
      right: 2px;
    }

    &__loc-adress {
      width: 100%;
      white-space: normal;
      line-height: 15px;
      text-overflow: ellipsis;
      font-size: 16px;
      margin-bottom: 10px;
    }

    &__text {
      display: flex;
      flex-direction: column;
      padding: 6px 0;
      gap: 0.33em;
    }

    &__organization-name {
      font-size: 14px;
    }

    &__iin,
    &__object-of-organization {
      font-size: 14px;
    }

    &__rating {
      color: $red;
      font-size: 15px;
      position: absolute;
      bottom: 6px;
      right: 6px;
      display: flex;
      align-items: center;
      gap: 2px;
    }
  }

  @media only screen and (max-width: 544px) {
    .card {
      width: calc(100% - 1rem);
      white-space: normal;
      word-wrap: break-word;

      &__avatar {
        width: 100%;
        height: 200px;
      }

      &__loc-adress {
        font-size: 14px;
      }

      &__organization-name {
        font-size: 14px;
      }

      &__iin,
      &__object-of-organization {
        font-size: 12px;
      }

      &__rating {
        font-size: 10px;
      }

      .v-avatar {
        width: 20px !important;
        height: 20px !important;

        & i {
          font-size: 10px !important;
        }
      }
    }
  }

  @media only screen and (max-width: 281px) {
    .card {
      width: 100%;

      &__loc-adress {
        font-size: 4px;
      }

      &__organization-name {
        font-size: 3px;
      }

      &__iin,
      &__object-of-organization {
        font-size: 3px;
      }

      &__rating {
        font-size: 3px;
      }

      .v-avatar {
        width: 20px !important;
        height: 20px !important;

        & i {
          font-size: 10px !important;
        }
      }
    }
  }
}
</style>
