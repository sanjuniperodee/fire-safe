<template>
  <ObjectOwnerInspectStepLayout>
    <v-table class="table">
      <thead>
        <tr>
          <th class="text-left"></th>
          <th class="text-left"></th>
        </tr>
      </thead>
      <tbody class="table-body">
        <tr
          v-for="item in objectInfoStore.generalObjectInfo"
          :key="item.key"
        >
          <td>
            <b> {{ item.title }}</b>
          </td>
          <td>{{ item.value }}</td>
        </tr>
      </tbody>
    </v-table>

    <button
      v-if="userStore.acceptedRoles.includes(UserRoleOptions.INSPECTOR)"
      @click="toggleModal"
      class="remark-btn"
      title="Сделать примечание"
    >
      <v-icon>mdi-pen</v-icon>
      Сделать примечание

    </button>

    <RemarkModal :id="route.params.id.toString()" :showModal="showModal" @close="toggleModal"/>
    <ObjectRemarks />
  </ObjectOwnerInspectStepLayout>
</template>

<script setup lang="ts">
import ObjectOwnerInspectStepLayout from '../UI/ObjectOwnerInspectStepLayout.vue'
import { useObjectInfoStore } from '@/stores/ObjectInfoStore'
import RemarkModal from '@components/modal/RemarkModal.vue'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import ObjectAvatar from '@views/Objects/objects-owner/object-card/UI/ObjectAvatar.vue'
import { useObjectStore } from '@stores/ObjectStore'
import ObjectRemarks from '../../../../object-card/UI/ObjectRemarks.vue'
import { useUserStore } from '@/stores/UserStore'
import { UserRoleOptions } from '@/types/User'

const objectInfoStore = useObjectInfoStore()
const objectStore = useObjectStore()
const userStore = useUserStore()
const route = useRoute()


const showModal = ref(false)

const toggleModal = () => {
  showModal.value = !showModal.value
}

onMounted(() => {
  console.log(objectInfoStore.getObjectInfo)
})

</script>

<style lang="scss" scoped>
.thead,
.table {
  width: 100%;
}

.table-body {
  font-size: 18px;
}

.remark-btn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 5px;
  background-color: #5b9170;
  color: white;
  border-radius: 5px;
  margin: 20px 0 0 10px;
  padding: 10px;
  font-size: 18px;
  transition: .2s ease-in-out;

  &:hover {
    background-color: rgb(77, 131, 96);
  }
}

@media only screen and (max-width: 524px) {
  .table-body {
    font-size: 14px;
  }
}
</style>
