<template>
  <v-card
    v-ripple
    class="card"
    variant="tonal"
  >
    <v-avatar
      class="ma-1"
      size="42"
      rounded="5"
    >
      <div v-if="true">
        <v-icon size="25">mdi-home-city</v-icon>
      </div>
    </v-avatar>
    <div class="card__text">
      <v-card-title
        class="card__loc-adress"
        style="padding: 0"
        >{{ advertisement.title }}</v-card-title
      >
      <div class="card__organization-name">Контактное лицо: {{ advertisement.contract_name }}</div>
      <div class="card__iin">Телефон: {{ advertisement.phone }}</div>
      <div class="card__object-of-organization">Адрес: {{ advertisement.address }}</div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { type Advertisement } from '@/types/Advertisements'

defineProps<{
  advertisement: Advertisement
}>()
</script>

<style lang="scss" scoped>
.card {
  display: flex;
  align-items: center;
  flex-direction: row;
  margin: 10px;
  padding: 10px;
  width: 100%;

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

  &__organization-name,
  &__iin,
  &__object-of-organization {
    font-size: 14px;
  }

  @media only screen and (max-width: 544px) {
    width: calc(50% - 1rem);

    &__loc-adress {
      font-size: 6px;
    }

    &__organization-name,
    &__iin,
    &__object-of-organization {
      font-size: 4px;
    }

    .v-avatar {
      width: 20px !important;
      height: 20px !important;

      & i {
        font-size: 10px !important;
      }
    }
  }

  @media only screen and (max-width: 281px) {
    width: 100%;

    &__loc-adress {
      font-size: 4px;
    }

    &__organization-name,
    &__iin,
    &__object-of-organization {
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
</style>
