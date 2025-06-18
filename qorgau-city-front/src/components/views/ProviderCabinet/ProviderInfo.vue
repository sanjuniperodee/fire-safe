<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/UserStore'
import GoBack from './UI/GoBack.vue'
import { organizationTypesReverseMapping, getLocalOrganizationType, type OrganizationTypes } from '@/types/ObjectBuilding'

const userStore = useUserStore()
const route = useRoute()

onMounted(async () => {
  await userStore.getProvider(Number(route.params.id))
})

// Helper function to format phone number
const formatPhoneNumber = (phone: string) => {
  return phone.replace(/(\d{1})(\d{3})(\d{3})(\d{4})/, '+$1 ($2) $3-$4')
}
</script>

<template>
  <v-container class="profile-container">
    <v-row>
      <v-col cols="12">
        <GoBack />
      </v-col>
    </v-row>

    <v-card class="provider-main-card elevation-3 mb-6">
      <v-card-item>
        <div class="provider-avatar">
          <img src="/user.png" alt="">
        </div>
        <v-card-title class="text-h4 font-weight-bold">
          {{ userStore.provider?.last_name }} 
          {{ userStore.provider?.first_name }} 
          {{ userStore.provider?.middle_name }}
        </v-card-title>
        <v-card-subtitle class="text-h6 mt-2 ">
          {{ organizationTypesReverseMapping[userStore.provider?.organization_type!] }} 
        </v-card-subtitle>
        <v-card-subtitle class="text-h6 mt-2 ">
          {{ userStore.provider?.company_name ? getLocalOrganizationType(userStore.provider?.company_name.split(" ").slice(0, -1).join(" ") as OrganizationTypes) : '' }}
        </v-card-subtitle>
        <v-card-subtitle class="text-h6 mt-2">
          {{ userStore.provider?.company_name?.split(" ").pop() || '' }}
        </v-card-subtitle>
      </v-card-item>

      <v-divider></v-divider>

      <v-card-text>
        <v-row>
          <v-col cols="12" sm="4">
            <v-list-item prepend-icon="mdi-phone" class="contact-item">
              <v-list-item-title class="font-weight-medium">
                {{ formatPhoneNumber(userStore.provider?.phone || '') }}
              </v-list-item-title>
              <v-list-item-subtitle>Телефон</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12" sm="4">
            <v-list-item prepend-icon="mdi-email" class="contact-item">
              <v-list-item-title class="font-weight-medium">
                {{ userStore.provider?.email }}
              </v-list-item-title>
              <v-list-item-subtitle>Email</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12" sm="4">
            <v-list-item prepend-icon="mdi-identifier" class="contact-item">
              <v-list-item-title class="font-weight-medium">
                {{ userStore.provider?.bin_field }}
              </v-list-item-title>
              <v-list-item-subtitle>БИН</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card class="addresses-card elevation-3 mb-6">
      <v-card-title class="text-h5 pa-4">
        Адреса
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <v-list-item prepend-icon="mdi-map-marker" class="address-item">
              <v-list-item-title class="font-weight-medium">
                {{ userStore.provider?.actual_residence_address }}
              </v-list-item-title>
              <v-list-item-subtitle>Фактический адрес</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          
          <v-col cols="12" sm="6">
            <v-list-item prepend-icon="mdi-home" class="address-item">
              <v-list-item-title class="font-weight-medium">
                {{ userStore.provider?.residence_address }}
              </v-list-item-title>
              <v-list-item-subtitle>Адрес проживания</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card class="categories-card elevation-3">
      <v-card-title class="text-h5 pa-4">
        Категории
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col 
            v-for="category in userStore.provider?.categories" 
            :key="category.id"
            cols="12"
            sm="6"
          >
            <v-expansion-panels variant="accordion">
              <v-expansion-panel>
                <v-expansion-panel-title class="font-weight-medium">
                  Категория {{ category.id }}
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <div class="category-details">
                    <p class="text-body-1">{{ category.name }}</p>
                    <p class="text-caption text-secondary mt-2">
                      Единица измерения: {{ category.measurement_unit }}
                    </p>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card v-if="userStore.provider?.role" class="roles-card elevation-3 mt-6">
      <v-card-title class="text-h5 pa-4">
        Роли
      </v-card-title>
      <v-card-text>
        <v-chip-group>
          <v-chip 
            v-for="role in userStore.provider?.role" 
            :key="role" 
            color="primary" 
            variant="outlined"
            class="ma-2"
          >
            {{ role }}
          </v-chip>
        </v-chip-group>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped>
.profile-container {
  height: calc(100vh - 56px);
  overflow-y: auto;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.provider-main-card,
.categories-card,
.roles-card,
.addresses-card {
  background-color: white;
  border-radius: 12px;
  margin-top: 50px;
}

.contact-item,
.address-item {
  transition: background-color 0.3s ease;
}

.contact-item:hover,
.address-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.category-details {
  padding: 8px 0;
}

.provider-avatar{
  width: 90px;
  height: 90px;
  border-radius: 50%;
  margin: 10px 0;
}

.provider-avatar img{ 
  width: 100%;
  border-radius: 50%;
}
</style>