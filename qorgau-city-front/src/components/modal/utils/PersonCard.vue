<template>
  <v-card
    class="inspector-card ma-2"
    elevation="2"
    @click=""
  >
    <v-row
      no-gutters
      align="center"
    >
      <v-col cols="auto">
        <v-avatar
          class="ma-3"
          size="64"
          rounded="lg"
        >
          <v-img
            :src="displayAvatar"
            alt="Avatar"
            cover
          />
        </v-avatar>
      </v-col>
      <v-col>
        <v-card-text>
          <v-list-item
            :title="fullName"
            :subtitle="email"
          >
            <template v-slot:subtitle>
              <div class="text-body-2">{{ email }}</div>
              <div class="text-caption">{{ phone }}</div>
            </template>
          </v-list-item>
          <v-chip
            class="mt-2"
            color="primary"
            size="small"
            variant="outlined"
            prepend-icon="mdi-account"
          >
            ИИН:
            {{ iin }}
          </v-chip>
        </v-card-text>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import { useComplaintStore } from '@/stores/ComplaintStore'
import { useRouter } from 'vue-router'
import { useSnackbarStore } from '@stores/SnackbarStore'

const complaintStore = useComplaintStore
const router = useRouter()
const snackbarStore = useSnackbarStore()

const props = defineProps<{
  id: number
  first_name: string
  last_name: string
  middle_name: string
  iin: string
  email: string
  phone: string
  avatar_url: string
}>()

const goToPage = (route: string) => {
  router.push({ name: route })
}

// const noteComplaint = async (cardId: number) => {
//   try {


//     const chatData = await complaintStore.createComplaint()
//     // await chatStore.getChatRoomById(chatData.id);
   
//     goToPage('Faq')
   
//     snackbarStore.pullSnackbar(
//       'Отлик отправлен, заявка добавлена в "Избранные заявки"',
//       3000,
//       '#5b9271'
//     )
//   } catch (err) {
//     snackbarStore.pullSnackbar('Не удалось отправить отклик!', 3000, '#d20f0d')
//     console.error(err)
//   }
// }

const fullName = `${props.last_name} ${props.first_name} ${props.middle_name}`
const displayAvatar = props.avatar_url || '/user.png'
</script>

<style scoped>
.inspector-card {
  transition: transform 0.2s;
}
.inspector-card:hover {
  transform: translateY(-2px);
}
</style>
