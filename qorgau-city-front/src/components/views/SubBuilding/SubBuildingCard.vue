<script setup lang="ts">
import { useSubBuildingStore } from '@/stores/SubBuildingStore'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@stores/UserStore'
import { UserRoleOptions } from '@/types/User'
import Empty from '@components/empty/EmptyView.vue'

const subBuildingStore = useSubBuildingStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const objectId = route.params.id as string

console.log(subBuildingStore.subBuildings)

onMounted(() => {
  subBuildingStore.getSubBuildings(objectId)
})

const navigateToSubBuilding = (subBuildingId: number) => {
  if (userStore.acceptedRoles.includes(UserRoleOptions.OBJECT_OWNER)) {
    router.push({
      name: 'SubBuildingEditInfo',
      params: {
        id: route.params.id,
        subBuilding: subBuildingId
      }
    })
  } else {
    router.push({
      name: 'SubBuildingInfo',
      params: {
        id: route.params.id,
        subBuilding: subBuildingId
      }
    })
  }
}
</script>

<template>
  <v-container
    fluid
    class="pt-5"
  >
    <h1>
      Подздания:
      <Empty
        v-if="subBuildingStore.subBuildings.length === 0"
        message="Отсутствуют подздания"
      />
    </h1>

    <v-row
      v-if="subBuildingStore.subBuildings.length > 0"
      class="d-flex justify-space-between mt-3"
    >
      <v-col
        v-for="subBuilding in subBuildingStore.subBuildings"
        :key="subBuilding.id"
        cols="12"
        sm="12"
        md="6"
      >
        <v-card class="sub-building-card w-100">
          <v-avatar
            class="card__avatar"
            size="130"
            rounded
          >
          <img
            v-if="subBuilding.images && subBuilding.images.length > 0"
            :src="subBuilding.images[0].image"
            class="avatar-img"
            alt="Аватар профиля"
          />

            <div v-else>
              <v-icon size="70">mdi-warehouse</v-icon>
            </div>
          </v-avatar>

          <div class="info-block">
            <v-card-title class="title">Название: {{ subBuilding.title }}</v-card-title>
            <v-card-text class="text"
            >Предназначение: {{ subBuilding.functional_purpose }}</v-card-text
            >
            <v-card-text class="text"
            >Основание подздания: {{ subBuilding.building_foundation }}</v-card-text
            >
            <v-card-actions>
              <v-btn
                variant="elevated"
                @click="navigateToSubBuilding(subBuilding.id!)"
              >
                Полная информация
              </v-btn>
            </v-card-actions>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped lang="scss">
h1 {
  padding-left: 15px;
  font-weight: 600;
  font-size: 20px;
}

.card__avatar{
  width: 30%;
  margin: 10px;
  height: 130px;
  border-radius: 5px;
  object-fit: cover;
}

.info-block{
  width: 100%;
}

.sub-building-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f5f5f5;
  border-radius: 5px;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  }

  .title {
    font-weight: 500;
    font-size: 18px;
    color: #333;
    margin-top: 15px;
  }

  .avatar-img{
    width: 85%;
    object-fit: contain;
    border-radius: 5px;
  }

  .text {
    font-size: 16px;
    font-weight: 400;
    color: #666;
  }

  .v-card-actions {
    display: flex;
    justify-content: flex-end;
    padding: 16px;
  }

  .v-btn {
    background-color: #f37b01;
    color: #fff;

    &:hover {
      background-color: #d76c01;
    }
  }
}
</style>
