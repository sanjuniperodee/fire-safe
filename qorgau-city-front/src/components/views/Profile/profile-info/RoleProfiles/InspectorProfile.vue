<script setup lang="ts">
import { ref } from 'vue'
import { useProfileStore } from '@stores/ProfileStore'
import { editField, cancelEditing, saveEditing } from '../utils/editFunctions'
import { rankTypesMapping, positionTypesMapping, roleTypesMapping, rankReverseToRussian, rankMapReverse } from '@/types/User'

const profileStore = useProfileStore()

const inspectorFields = ref([
  profileStore.items.rank,
  profileStore.items.position,
  profileStore.items.certificate_number,
  profileStore.items.inspector_jurisdiction_city,
  profileStore.items.inspector_jurisdiction_district,
])


const russianRank = Object.values(rankTypesMapping)
const russianPosition = Object.values(positionTypesMapping)
</script>

<template>
  <div class="info__block">
    <div
      class="info__block-item"
      v-for="inspectorItem in inspectorFields"
      :key="inspectorItem.name"
    >
      <div class="info__block-box">
        <v-card-title class="info__block-title">{{ inspectorItem.name }}</v-card-title>
        <v-btn
          v-if="!inspectorItem.isEditing"
          @click="editField(inspectorItem.key)"
          icon="mdi-pencil"
          rounded="lg"
          size="x-small"
          color="#f57c01"
          class="text-white"
        ></v-btn>
        <div
          v-if="inspectorItem.isEditing"
          class="info__editing-btns"
        >
          <v-btn
            @click="saveEditing(inspectorItem.key)"
            icon="mdi-check-bold"
            rounded="lg"
            size="x-small"
            color="#5b9271"
            class="text-white"
          ></v-btn>
          <v-btn
            @click="cancelEditing(inspectorItem.key)"
            icon="mdi-close"
            rounded="lg"
            size="x-small"
            color="#d20f0d"
            class="text-white"
          ></v-btn>
        </div>
      </div>
      <v-select
          v-if="inspectorItem.key === 'rank'"
          :rules="inspectorItem.rules"
          v-model="rankTypesMapping[inspectorItem.value as keyof typeof rankTypesMapping]"
          class="rank-select"
          label="Звание"
          :items="russianRank"
          variant="outlined"
          dense
          hide-details="auto"
          :readonly="!inspectorItem.isEditing"
          :disabled="!inspectorItem.isEditing"
        ></v-select>

        <v-select
          v-if="inspectorItem.key === 'position'"
          :rules="inspectorItem.rules"
          v-model="positionTypesMapping[inspectorItem.value as keyof typeof positionTypesMapping]"
          class="rank-select"
          label="Звание"
          :items="russianPosition"
          variant="outlined"
          dense
          hide-details="auto"
          :readonly="!inspectorItem.isEditing"
          :disabled="!inspectorItem.isEditing"
        ></v-select>

      <v-text-field
        v-if="inspectorItem.key === 'certificate_number'"
        :rules="inspectorItem.rules"
        :disabled="!inspectorItem.isEditing"
        v-model="inspectorItem.value"
        :label="inspectorItem.name"
        variant="outlined"
        :readonly="!inspectorItem.isEditing"
      ></v-text-field>
      <v-text-field
        v-if="inspectorItem.key === 'inspector_jurisdiction_city'"
        :rules="inspectorItem.rules"
        :disabled="!inspectorItem.isEditing"
        v-model="inspectorItem.value"
        :label="inspectorItem.name"
        variant="outlined"
        :readonly="!inspectorItem.isEditing"
      ></v-text-field>
      <v-text-field
        v-if="inspectorItem.key === 'inspector_jurisdiction_district'"
        :rules="inspectorItem.rules"
        :disabled="!inspectorItem.isEditing"
        v-model="inspectorItem.value"
        :label="inspectorItem.name"
        variant="outlined"
        :readonly="!inspectorItem.isEditing"
      ></v-text-field>
    </div>
  </div>
</template>

<style scoped lang="scss">
.info {
  margin-top: 10em;
  padding-bottom: 4em;
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: center;

  &__block {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    margin-bottom: 20px;
    background-color: white;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    padding: 20px;
  }

  &__title {
    padding: 0;
    width: 100%;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 1em;
  }

  &__block-item {
    gap: 1em;
    display: flex;
    flex-direction: column;
    width: 49%;
  }

  &__block-box {
    height: 32px;
    justify-content: space-between;
    gap: 1em;
    width: 100%;
    align-items: center;
    display: flex;
  }

  &__block-title {
    font-size: 16px;
    padding: 0;
  }

  &__editing-btns {
    display: flex;
    gap: 0.5em;
  }
}
</style>
