import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { complaintService } from '@/services/complaint.service'
import type { CreateComplaint, Complaint, ComplaintRoomType} from '@/types/Complaint'
import { chatWebSocketService } from '@/services/chat.service'
import type { ChatRoomType, SendMessage, ChatRooms, Files } from '@/types/Chat'

export const useComplaintStore = defineStore('complaint', () => {
  const complaints = ref<Complaint[]>([])
  const chatRooms = ref<ChatRooms>([])
  const complaintRoom = ref<ComplaintRoomType | null>(null)
  const chatRoom = ref<ChatRoomType | null>(null)

  const createComplaint = async (body: CreateComplaint) => {
    try {
      await complaintService.createComplaint(body)
    } catch (err) {
      return err
    }
  }

  const getComplaints = async (status: string) => {
    try {
      complaints.value = await complaintService.getComplaints(status)
    } catch (err) {
      return err
    }
  }

  const getComplaint = async (id: number) => {
    try {
      chatRoom.value = await chatWebSocketService.getConversationsComplaint(id)
    } catch (err) {
      return err
    }
  }

  const getComplaintById = async (id: number) => {
    try {
      complaintRoom.value = await complaintService.getComplaintsById(id)
    } catch (err) {
      return err
    }
  }

  const createMarkAsAnswered = async (id: number | null) => {
    try {
      await complaintService.createMarkAsAnswered(id)
    } catch (error) {
      return error
    }
  }

  const sendMessage = async (message: SendMessage) => {
    try {
      await chatWebSocketService.sendMessageToSocket(message)
    } catch (error) {
      return error
    }
  }

  const removeComplaint = async (id: number) => {
    try {
      const data =  await complaintService.removeComplaint(id)
      return data
    } catch (error) {
      return error
    }
  }

  const uploadFile = async (fileId: number, body: File) => {
    try {
      const data = await chatWebSocketService.createFile(fileId, body)
      return data
    } catch (error) {
      return error
    }
  }

  const updateChangeStatementStatus = async (id: number | null, status: string) => {
    try {
      await complaintService.updateChangeStatementStatus(id, status)
    } catch (error) {
      return error
    }
  }

  const lastComplaintRoom = computed(() => {
    return complaints.value.length > 0 ? complaints.value[complaints.value.length - 1] : null
  })

  return {
    complaints,
    complaintRoom,
    getComplaints,
    createComplaint,
    getComplaintById,
    lastComplaintRoom,
    chatRoom,
    getComplaint,
    sendMessage,
    uploadFile,
    removeComplaint,
    createMarkAsAnswered,
    updateChangeStatementStatus
  }
})
