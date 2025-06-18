import { defineStore } from 'pinia'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { chatWebSocketService } from '@/services/chat.service'
import type { ChatRoomType, ChatRooms, Message, SendMessage, Files } from '@/types/Chat'

export const useChatStore = defineStore('chat', () => {
  const chatRooms = ref<ChatRooms>([])
  const chatRoom = ref<ChatRoomType | null>(null)
  const uploadedMedia = ref<File | null>(null);
  const message = ref<Message>() // Store messages here


  // Manage WebSocket connection
  let socket: WebSocket | null = null


  onUnmounted(() => {
    if (socket) {
      socket.close() // Clean up on component unmount
      socket = null
    }
  })

  const createChatRoom = async (phone: string) => {
    try {
      const data = await chatWebSocketService.createChatRoom(phone)
      chatRooms.value.push(data)
      return data
    } catch (err) {
      return err
    }
  }

  const getChatRoomById = async (id: number) => {
    try {
      chatRoom.value = await chatWebSocketService.getChatRoomById(id)
    } catch (err) {
      return err
    }
  }

  const getAllChatRooms = async (status: string) => {
    try {
      chatRooms.value = await chatWebSocketService.getAllChatRooms(status)
    } catch (err) {
      return err
    }
  }

  const sendMessage = async (message: SendMessage) => {
    try {
      await chatWebSocketService.sendMessageToSocket(message)
    } catch (error) {
      return error
    }
  }

  // const getMessage = async (id: number): Promise<Message> => {
  //   try {
  //     const data = await chatWebSocketService.connect(id)
  //     return data 
  //   } catch (error) {
  //     console.error('Ошибка при получении сообщения:', error)
  //     throw error
  //   }
  // }

  const uploadFile = async (fileId: number, body: File) => {
    try {
      const data = await chatWebSocketService.createFile(fileId, body)
      return data
    } catch (error) {
      return error
    }
  }

  const lastChatRoom = computed(() => {
    return chatRooms.value.length > 0 ? chatRooms.value[chatRooms.value.length - 1] : null
  })

  return {
    chatRooms,
    chatRoom,
    message, // Expose messages state
    lastChatRoom,
    getAllChatRooms,
    createChatRoom,
    getChatRoomById,
    sendMessage,
    //getMessage,
    uploadFile
  }
})
