import type { Author } from './User'

export type CreateComplaint = {
  city: string
  district: string
}

// types/Complaint.ts
export type ComplaintRoomType = {
  id: number;
  unique_id: number;
  author: Person;
  inspector: Person;
  status: string;
  expiration_date: string;
  archive_date: string;
  chat_room_id: number;
  created_at: string;
  updated_at: string;
}

export type Complaint = {
  id: number;
  unique_id: string;
  author: Person;
  inspector: Person;
  status: string;
  expiration_date: string;
  archive_date: string;
  chat_room_id: number;
  created_at: string;
  updated_at: string;
};

export type Person = {
  id: number;
  phone: string;
  last_name: string;
  first_name: string;
  middle_name: string | null;
  iin: string;
  email: string;
};

export type Message = {
  text?: string;
  files?: any[];  // укажите тип для файлов
};

export type User = {
  phone: string;
  first_name?: string;
  last_name?: string;
};

export type Chat = {
  id: number;
  initiator: User | null;
  receiver: User | null;
  last_message?: Message;
};

export type ComplaintUser = {
  id: number
  username: string
  phone: string
  email: string | null
}

// types/Chat.ts
export type SendMessage = {
  conversation_id: number;
  sender: {
    id: number;
    phone: string;
    last_name: string;
    first_name: string;
    middle_name: string;
    iin: string;
    email: string;
  };
  text: string;
  files: Array<any>;
  timestamp: Date;
}