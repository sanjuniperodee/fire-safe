import { chatWebSocketService } from '@/services/chat.service'
import type { ChatLoginValidator, ChatRegisterValidator } from '@/types/Chat'

export async function ChatRegistration(payload: ChatRegisterValidator) {
  const payloadForChat = (({ phone, password1, password2 }) => ({
    phone,
    password1,
    password2,
  }))(payload);

  //await chatWebSocketService.registerForChat(payloadForChat)
}

export async function ChatLogin(payload: ChatLoginValidator) {
  const payloadForChat = (({ phone,password }) => ({
    phone,
    password,
  }))(payload);

  //TODO

  await chatWebSocketService.loginForChat(payloadForChat)
}