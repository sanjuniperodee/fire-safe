export type ChatRoomType = {
  id: number
  initiator: ChatUser
  receiver: ChatUser
  message_set: Message[]
  location: string
  provider_name: string
  categories: []
  conversation_type: string
  author_name: string
  is_statement_owner: boolean
  statement: Statement
}

export type Statement = {
  id: number,
  status: string,
  created_at: Date,
  updated_at: Date
}

export type ChatRooms = {
  id: number
  initiator: ChatUser
  receiver: ChatUser
  last_message: Message
  location: string
  provider_name: string
  categories: []
  conversation_type: string
  author_name: string
  is_statement_owner: boolean
}[]

export type Message = {
  id?: number
  sender: number
  text?: string
  attachments?: File[]
  conversation_id: number
  timestamp: Date
}

export type File = {
  id: number
  file: string
  file_size: number
  filename: string
}

export type SendMessage = {
  id?: number
  sender: number
  text?: string
  files?: Files[]
  conversation_id: number
  timestamp: Date
}

// AUTH TYPES

export type ChatRegisterValidator = {
  phone: string
  password1: string
  password2: string
}

export type ChatLoginValidator = {
  phone: string
  password: string
}

// UTIL TYPES

export type ChatUser = {
  id: number
  phone: string
  username: string
  email: null
}

export type Files = {
  message: string
  files: FileContent[]
  total_files: number
  total_size: number
}

export type FileContent = {
  id?: number
  file: string
  filename: string
  file_size: number
  uploaded_at: Date
}

export type  Phone = {
  phone: string;
}


