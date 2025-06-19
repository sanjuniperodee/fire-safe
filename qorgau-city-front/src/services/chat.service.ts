import axios from 'axios';
import type { ChatLoginValidator, ChatRooms, ChatRoomType, Message, SendMessage, Files, FileContent, PaginatedChatRooms } from '@/types/Chat';
// import type { ComplaintRoomType } from '@/types/Complaint';
import { useChatStore } from '@stores/ChatStore'

// Используем локальный API вместо внешнего
const SOCKET_URL = 'ws://165.22.63.97:2998';
new Map();
// const MAX_CONNECTIONS_PER_INTERVAL = 2;
// const INTERVAL_MS = 600; // 1 минута
// const RECONNECT_TIMEOUT_MS = 100; // 10 секунд

class ChatWebSocketService {
  private socket: WebSocket | null = null;
  private chatUrl: string;
  private chatToken: string | null;
  private setupMessageHandling!: () => void;

  
  constructor(chatUrl: string) {
    this.chatUrl = chatUrl;
    // Используем обычный JWT токен вместо отдельного chat_token
    this.chatToken = localStorage.getItem('token');
  }

  // Упрощаем авторизацию - используем существующий JWT токен
  async loginForChat(body: ChatLoginValidator): Promise<string> {
    // В нашем случае авторизация уже выполнена через основное приложение
    // Просто проверяем наличие токена
    if (this.chatToken) {
      return 'Авторизация прошла успешно.';
    }
    throw new Error('Необходима авторизация');
  }

  connect(roomId: number) {
    return new Promise((resolve, reject) => {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      resolve(true);
      return;
    }

    const tryConnection = (tokenFormat: string, description: string) => {
      return new Promise<boolean>((resolveAttempt) => {
        console.log(`${description}: ${tokenFormat.substring(0, 100)}...`);
        
        this.socket = new WebSocket(tokenFormat);

        const timeout = setTimeout(() => {
          if (this.socket?.readyState === WebSocket.CONNECTING) {
            console.log(`${description} - Connection timeout`);
            this.socket.close();
            resolveAttempt(false);
          }
        }, 5000);

        this.socket.onopen = () => {
          clearTimeout(timeout);
          console.log(`Connected to WebSocket with ${description}`);
          this.setupMessageHandling();
          resolveAttempt(true);
        };

        this.socket.onerror = (error) => {
          clearTimeout(timeout);
          console.error(`WebSocket Error with ${description}:`, error);
          resolveAttempt(false);
        };

        this.socket.onclose = (event) => {
          clearTimeout(timeout);
          console.log(`WebSocket closed with ${description}:`, event.code, event.reason);
          resolveAttempt(false);
        };
      });
    };

    const setupMessageHandling = () => {
      if (this.socket) {
        this.socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          const chatStore = useChatStore()
          if (data.attachments && data.attachments.length > 0) {
            chatStore.message = {
              ...data,
              attachments: data.attachments
            };
          } else {
            chatStore.message = data;
          }
        };
      }
    };

    this.setupMessageHandling = setupMessageHandling;

    // Попробуем разные форматы токенов
    const connectionAttempts = [
      {
        url: `${SOCKET_URL}/ws/chat/${roomId}/?token=${this.chatToken}`,
        desc: "Direct token"
      },
      {
        url: `${SOCKET_URL}/ws/chat/${roomId}/?token=Bearer%20${this.chatToken}`,
        desc: "Bearer token (URL encoded)"
      },
      {
        url: `${SOCKET_URL}/ws/chat/${roomId}/?token=Bearer ${this.chatToken}`,
        desc: "Bearer token"
      },
      {
        url: `${SOCKET_URL}/ws/chat/${roomId}/?authorization=${this.chatToken}`,
        desc: "Authorization parameter"
      }
    ];

    // Попробуем подключения последовательно
    const tryConnections = async () => {
      for (const attempt of connectionAttempts) {
        const success = await tryConnection(attempt.url, attempt.desc);
        if (success) {
          resolve(true);
          return;
        }
        
        // Небольшая пауза между попытками
        await new Promise(r => setTimeout(r, 500));
      }
      
      console.error("All WebSocket connection attempts failed");
      resolve(false);
    };

    tryConnections();
  });
  }

  

  sendMessageToSocket(message: SendMessage) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      return;
    }
  
    const socketMessagePayload = {
      message: message.text,
      attachments: message.files?.map(uploadResponse => 
        uploadResponse.files.map(file => ({
          file: file.file,        // URL файла
          filename: file.filename, // Имя файла
          file_size: file.file_size // Размер файла
        }))
      ).flat()
    };
  
    try {
      this.socket.send(JSON.stringify(socketMessagePayload));
    } catch (error) {
      console.error('Error sending message:', error);
    }
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  private handleMessage(message: Message): void {
    console.log('New message received:', message);
  }

  async chatLogout() {
    // Просто удаляем основной токен
    localStorage.removeItem('token');
  }

  async getAllConversations(): Promise<ChatRooms> {
    try {
      const { data }: { data: PaginatedChatRooms } = await axios.get(`${this.chatUrl}/api/v1/conversations/statement/`, {
        headers: {
          Authorization: `Bearer ${this.chatToken}`,
          'Content-Type': 'application/json'
        }
      });
      // Return only the results array from the paginated response
      return data.results;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  }

  async getConversation(roomId: number): Promise<ChatRoomType> {
    const { data } = await axios.get(`${this.chatUrl}/api/v1/conversations/${roomId}/`, {
      headers: {
        Authorization: `Bearer ${this.chatToken}`,
        'Content-Type': 'application/json'
      }
    });
    return data;
  }

  async startConversation(phone: string): Promise<ChatRoomType> {
    const { data } = await axios.post(
      `${this.chatUrl}/api/v1/conversations/statement/start/`,
      { phone },
      {
        headers: {
          Authorization: `Bearer ${this.chatToken}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return data;
  }

  async createChatRoom(phone: string) {
    try {
      const { data } = await axios.post(
        `${this.chatUrl}/api/v1/conversations/statement/start/`,
        { phone },
        {
          headers: {
            Authorization: `Bearer ${this.chatToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      console.log('Chat Room Created:', data);
      return data;
    } catch (error) {
      console.error('Error creating chat room:', error);
      throw error;
    }
  }

  // async getMessageById(id: number) {
  //   return new Promise((resolve) => {
  //   //this.socket = new WebSocket(`${SOCKET_URL}/ws/chat/${id}/?token=Token ${this.chatToken}`);
  //   if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
  //     return;
  //   }
  //   this.socket.onmessage = (event) => {
  //     const data = JSON.parse(event.data);
  //     // console.log("Received message:", data);
  //     resolve(data);
  //   };
  //   });
  // }

  async getChatRoomById(id: number) {
    const { data } = await axios.get(`${this.chatUrl}/api/v1/conversations/${id}/`, {
      headers: {
        Authorization: `Bearer ${this.chatToken}`,
        'Content-Type': 'application/json'
      }
    });
    return data;
  }

  async getAllChatRooms(status: string): Promise<ChatRooms> {
    try {
      const { data }: { data: PaginatedChatRooms } = await axios.get(`${this.chatUrl}/api/v1/conversations/?statement_status=${status}`, {
        headers: {
          Authorization: `Bearer ${this.chatToken}`,
          'Content-Type': 'application/json'
        }
      });
      // Return only the results array from the paginated response
      return data.results;
    } catch (error) {
      console.error('Error fetching chat rooms:', error);
      throw error;
    }
  }

  async getConversationsComplaint(roomId: number): Promise<ChatRoomType> {
    const { data } = await axios.get(`${this.chatUrl}/api/v1/conversations/${roomId}/complaint/`, {
      headers: {
        Authorization: `Bearer ${this.chatToken}`,
        'Content-Type': 'application/json'
      }
    });
    return data;
  }

  // async createFile(conversationId: number, file: File): Promise<FileContent | null> {
  //   const formData = new FormData();
  //   formData.append('file', file);
  
  //   try {
  //     const response = await axios.post(`${this.chatUrl}/api/v1/conversations/send_files/${conversationId}/`, formData, {
  //       headers: {
  //         Authorization: `Token ${this.chatToken}`,
  //         'Content-Type': 'application/json'
  //       }
  //     });
  //     const uploadedFile = response.data.files[0];
  //     return {
  //       id: uploadedFile.id,
  //       file: uploadedFile.file,
  //       filename: uploadedFile.filename,
  //       file_size: uploadedFile.file_size,
  //       uploaded_at: uploadedFile.uploaded_at // добавляем uploaded_at
  //     };
  //   } catch (error) {
  //     console.error("Ошибка при загрузке файла:", error);
  //     return null;
  //   }
  // };
  

  async createFile(fileId: number, body: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', body);
    
    try {
      const { data } = await axios.post(
        `${this.chatUrl}/api/v1/files/${fileId}/`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${this.chatToken}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      return data;
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    }
  } 
}



export const chatWebSocketService = new ChatWebSocketService('http://165.22.63.97:2999');