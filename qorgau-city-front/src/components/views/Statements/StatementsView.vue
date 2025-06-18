<script setup lang="ts">
import { onMounted, ref } from 'vue'
import AllStatements from './AllStatements.vue'
import FilterStatements from '@views/Statements/utils/FilterStatements.vue'
import { itemsPerPage } from '@/utils/constants'
import { useStatementStore } from '@/stores/StatementsStore'
import { useUserStore } from '@stores/UserStore'
import { UserRoleOptions } from '@/types/User'

const userStore = useUserStore()
const statementStore = useStatementStore()
const initialPage = ref(1)
const pageForFilter = ref(0)

const fetchData = async () => {
  const page = (initialPage.value - 1) * itemsPerPage
  await statementStore.getAllStatements(itemsPerPage, page)

  pageForFilter.value = page
}

onMounted(async () => {
  await fetchData();
})
</script>

<template>
  <div class="statements-wrapper" v-if="userStore.acceptedRoles.includes(UserRoleOptions.PROVIDER)">
    <FilterStatements :offset="pageForFilter" :limit="itemsPerPage"/>
    <AllStatements/>
  </div>
  <div v-else class="not-provider">
    Вы не являетесь Поставщиком :(
  </div>
</template>

<style scoped lang="scss">
.statements-wrapper, .not-provider {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  gap: 30px;
  height: calc(100vh - 56px);
  width: 100%;
  background-color: #f2f3f6;
  overflow-y: hidden;
}

.not-provider{
  font-size: 30px;
  font-weight: 500;
}

@media only screen and (max-width: 920px) {
  .statements-wrapper {
    flex-direction: column;
    align-items: center;
    gap: 20px;
    height: calc(100vh - 56px);
    overflow-y: auto;
    padding: 20px 0;
  }
}
</style>