import { useSnackbarStore } from '@stores/SnackbarStore'
import { useStatementStore } from '@stores/StatementsStore'
import { useChatStore } from '@stores/ChatStore'
import { useRouter } from 'vue-router'

const snackbarStore = useSnackbarStore()
const statementStore = useStatementStore()
const chatStore = useChatStore()
const router = useRouter()

const goToPage = (route: string) => {
  router.push({ name: route })
}

export const noteStatement = async (cardId: number) => {
  try {
    const data = await statementStore.noteStatement(cardId)
   
    goToPage('Chat')
   
    snackbarStore.pullSnackbar(
      'Отлик отправлен, заявка добавлена в "Избранные заявки"',
      3000,
      '#5b9271'
    )
  } catch (err) {
    snackbarStore.pullSnackbar('Не удалось отправить отклик!', 3000, '#d20f0d')
    console.error(err)
  }
}