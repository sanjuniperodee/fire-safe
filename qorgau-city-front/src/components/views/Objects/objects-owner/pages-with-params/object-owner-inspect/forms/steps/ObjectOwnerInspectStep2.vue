<template>
  <ObjectOwnerInspectStepLayout>
    <!--    <v-table class="table">-->
    <!--      <thead>-->
    <!--        <tr>-->
    <!--          <th class="text-left"></th>-->
    <!--          <th class="text-left"></th>-->
    <!--        </tr>-->
    <!--      </thead>-->
    <!--      <tbody class="table-body">-->
    <!--        <tr-->
    <!--          v-for="item in objectInfoStore.subBuildingInfo"-->
    <!--          :key="item.key"-->
    <!--        >-->
    <!--          <td>-->
    <!--            <b>{{ item.title }}</b>-->
    <!--          </td>-->
    <!--          <td v-if="item.type === 'metrics'">{{ item.value + ' ' + item.metricType }}</td>-->
    <!--          <td v-else-if="item.type === 'date'">{{ formatDateWithoutTime(item.value as Date) }}</td>-->
    <!--          <td v-else>{{ item.value }}</td>-->
    <!--        </tr>-->
    <!--      </tbody>-->
    <!--    </v-table>-->
    <SubBuildingCard />
  </ObjectOwnerInspectStepLayout>
</template>

<script setup lang="ts">
import ObjectOwnerInspectStepLayout from '../UI/ObjectOwnerInspectStepLayout.vue'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import { formatDateWithoutTime } from '@/helpers/formatTime'
import SubBuildingCard from '@views/SubBuilding/SubBuildingCard.vue'

const objectInfoStore = useObjectInfoStore()
</script>

<style lang="scss" scoped>
.thead,
.table {
  width: 100%;
}

.table-body {
  font-size: 18px;
}

@media only screen and (max-width: 524px) {
  .table-body {
    font-size: 14px;
  }
}
</style>
