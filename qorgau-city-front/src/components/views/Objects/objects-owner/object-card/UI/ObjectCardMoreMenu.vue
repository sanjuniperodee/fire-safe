<template>
  <div class="text-center">
    <ObjectCardDeleteModal
      @close="closeModal"
      :id="id"
      :isDeleteDialogOpen="isDeleteDialogOpen"
    />
    <v-menu
      location="start"
      transition="scale-transition"
    >
      <template v-slot:activator="{ props }">
        <v-btn
          class="card__more"
          variant="text"
          v-bind="props"
          icon="mdi-dots-horizontal"
        ></v-btn>
      </template>
      <v-list>
        <v-list-item
          :style="{ color: item.color }"
          class="list"
          v-for="(item, index) in items"
          :key="index"
          :value="index"
        >
          <router-link
            @click="openModal(item.title)"
            :to="item.link"
          >
            <v-list-item-title class="list-item">
              <v-icon>{{ item.icon }}</v-icon>
              <span style="padding-top: 4px">{{ item.title }}</span>
            </v-list-item-title>
          </router-link>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts" setup>
import { useSnackbarStore } from '@/stores/SnackbarStore'
import ObjectCardDeleteModal from './ObjectCardDeleteModal.vue'
import { ref } from 'vue'

const componentProps = defineProps({
  id: Number
})

const items = ref([
  {
    title: 'Смотреть',
    icon: 'mdi-eye',
    link: `/objects/view/${componentProps.id}`,
    color: '#5b9271'
  },
  {
    title: 'Редактировать',
    icon: 'mdi-pencil',
    link: `/objects/edit/${componentProps.id}`,
    color: '#f6c640'
  },
  { title: 'Удалить', icon: 'mdi-delete', link: '/objects', color: '#d20f0d' }
])

const isDeleteDialogOpen = ref(false)

const snackbarStore = useSnackbarStore()

const openModal = (title: string) => {
  if (title === 'Удалить') {
    isDeleteDialogOpen.value = true
  }
}

const closeModal = () => {
  isDeleteDialogOpen.value = false
}
</script>

<style lang="scss" scoped>
.list {
  & a {
    color: inherit !important;

    &:visited {
      color: inherit !important;
    }
  }
}

.list-item {
  font-family: 'Overpass', sans-serif;
  display: flex;
  gap: 0.5em;
  align-items: center;
}
</style>
