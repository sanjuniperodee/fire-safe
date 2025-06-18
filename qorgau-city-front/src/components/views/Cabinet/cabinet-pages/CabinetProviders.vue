<script setup lang="ts">
import { onMounted } from 'vue'
import CabinetInspectorLayout from '@/layouts/CabinetInspectorLayout.vue'
import { useUserStore } from '@/stores/UserStore'
import type { Category } from '@/types/Provider'
import { useRouter } from 'vue-router'
import { organizationTypesReverseMapping, getLocalOrganizationType, type OrganizationTypes } from '@/types/ObjectBuilding'
import CabinetInfo from '@views/Cabinet/cabinet-info/CabinetInfo.vue'

const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  await userStore.getAllInsProvider()
})

const limitCategories = (categories: Category[]) => {
  if (categories.length <= 3) return categories
  return categories.slice(0, 3)
}

const hasMoreCategories = (categories: Category[]) => categories.length > 3

const goToCard = (cardId: number) => {
  router.push('/providers/view/' + cardId)
}
</script>

<template>
   <div class="cabinet-info"><CabinetInfo /></div>
  <v-container class="profile-container">
    <div class="provider-container">
      <h2>Поставщики</h2>
      <div class="product-block">
      <v-col v-for="provider in userStore.allInsProviders" :key="provider.id"
        class="provider-col">
        <v-card outlined elevation="2" @click="goToCard(provider.id)"
          class="pa-4 d-flex align-items-center provider-card">
          <div class="provider-avatar">
            <img src="/user.png" alt="">
          </div>
          <div>
            <v-card-title class="headline">
              {{ provider.company_name ? getLocalOrganizationType(provider.company_name.split(" ").slice(0, -1).join(" ") as OrganizationTypes) : '' }}
              {{ provider.company_name?.split(" ").pop() || '' }}
            </v-card-title>
            <v-card-subtitle>
              <strong>ФИО:</strong> {{ provider.last_name }} {{ provider.first_name }} {{ provider.middle_name }}
            </v-card-subtitle>
            <v-card-subtitle>
              <strong>Email:</strong> {{ provider.email }}
            </v-card-subtitle>
            <v-card-text class="flex-grow-1">
              <p><strong>Телефон:</strong> {{ provider.phone }}</p>
              <p><strong>БИН:</strong> {{ provider.bin_field }}</p>

              <!-- <v-expansion-panels class="mt-4">
                <v-expansion-panel
                  v-for="category in limitCategories(provider.categories)"
                  :key="category.id"
                  @click.stop
                >
                  <v-expansion-panel-title>
                    Категория {{ category.id }}
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    {{ category.name }}
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
              <p
                v-if="hasMoreCategories(provider.categories)"
                @click="goToCard(provider.id)"
                class="text-right mt-2"
                title="Посмотреть все категории"
              >
                <v-icon>mdi-dots-horizontal</v-icon>
              </p> -->
            </v-card-text>
          </div>
        </v-card>
      </v-col>
    </div>
    </div>
  </v-container>
</template>

<style scoped>
.v-card-title {
  font-weight: 400;
  font-size: 1.2rem;
}

.v-card-subtitle {
  padding-top: 10px;
  margin-top: -8px;
  color: #6c757d;
}

.v-card-text {
  padding-top: 16px;
}

.v-expansion-panel-title {
  font-weight: 500;
}

.provider-container {
  max-width: 1000px;
  margin: auto;
}

.provider-container h2 {
  font-size: 38px;
  font-weight: 500;
  line-height: 1.4em;
  margin: 30px 0;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
}

/* .product-block{
  overflow-x: scroll;
  height: 40rem;
} */

.provider-col {
  display: flex;
  align-items: center;
  min-width: 100%;
  /* Adjust this value as needed */
}

.provider-card {
  width: 100%;
  display: flex;

}

.provider-avatar {
  width: 65px;
  height: 65px;
  border-radius: 50%;
}

.provider-avatar img {
  width: 100%;
  border-radius: 50%;
}

.profile-container {
  height: calc(100vh - 56px);
  overflow-y: auto;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.cabinet-info {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

@media (max-width: 600px) {
  .provider-col {
    min-width: 100%;
  }
  .cabinet-info {
    display: none;
  }
}
</style>