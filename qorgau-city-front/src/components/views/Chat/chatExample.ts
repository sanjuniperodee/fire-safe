import { ref } from 'vue'
import type { ChatRooms } from '@/types/Chat'

// export const ChatRoomsList = ref<ChatRooms>([
//     {
//       id: 1,
//       initiator: {
//         id: 3,
//         phone: "+77058054272",
//         username: "usr 1",
//         email: null
//       },
//       receiver: {
//         id: 3,
//         phone: "+77074563210",
//         username: "user 2",
//         email: null
//       },
//       last_message: {
//         id: 18,
//         sender: 3,
//         text: 'text with photo',
//         files: [
//           {
//             id: 8,
//             file: "https://minio.qorgau-city.kz/isec/avatars/avatars/13._%D0%9A%D0%B0%D0%BC%D0%BD%D0%B8.jpg?AWSAccessKeyId=minioadmin&Signature=P7gFpTCO6Xmxm55jlrORJWuhb%2BE%3D&Expires=1725456372",
//             uploaded_at: new Date("2024-09-02T18:05:03.456018+06:00")
//           },
//         ],
//         conversation_id: 1,
//         timestamp: new Date("2024-09-02T18:05:03.456018+06:00")
//       }
//     },
//     {
//       id: 2,
//       initiator: {
//         id: 3,
//         phone: "+77058054272",
//         username: "qazaq",
//         email: null
//       },
//       receiver: {
//         id: 5,
//         phone: "+77065481033",
//         username: "qwwq",
//         email: null
//       },
//       last_message: {
//         id: 50,
//         sender: 3,
//         text: 'позвоню вечером',
//         conversation_id: 2,
//         timestamp: new Date("2024-09-02T18:05:03.456018+06:00")
//       }
//     }
//   ]
// );

// export const roomItems = ref<any>({
//     id: 1,
//     initiator: {
//       id: 3,
//       phone: "+77058054272",
//       username: "+77058054272",
//       email: null
//     },
//     receiver: {
//       id: 3,
//       phone: "+77058054272",
//       username: "+77058054272",
//       email: null
//     },
//     message_set: [
//       {
//         id: 18,
//         sender: 3,
//         files: [
//           {
//             id: 8,
//             file: "https://minio.qorgau-city.kz/isec/avatars/avatars/13._%D0%9A%D0%B0%D0%BC%D0%BD%D0%B8.jpg?AWSAccessKeyId=minioadmin&Signature=P7gFpTCO6Xmxm55jlrORJWuhb%2BE%3D&Expires=1725456372",
//             uploaded_at: "2024-09-02T15:06:54.196183+06:00"
//           },
//           {
//             id: 9,
//             file: "https://minio.qorgau-city.kz/isec/avatars/avatars/13._%D0%9A%D0%B0%D0%BC%D0%BD%D0%B8.jpg?AWSAccessKeyId=minioadmin&Signature=P7gFpTCO6Xmxm55jlrORJWuhb%2BE%3D&Expires=1725456372",
//             uploaded_at: "2024-09-02T15:06:54.330807+06:00"
//           }
//         ],
//         conversation_id: 1,
//         timestamp: "2024-09-02T15:06:54.023683+06:00"
//       },
//       {
//         id: 17,
//         sender: 4,
//         files: [
//           {
//             id: 7,
//             file: "https://minio.qorgau-city.kz/isec/avatars/avatars/13._%D0%9A%D0%B0%D0%BC%D0%BD%D0%B8.jpg?AWSAccessKeyId=minioadmin&Signature=P7gFpTCO6Xmxm55jlrORJWuhb%2BE%3D&Expires=1725456372",
//             uploaded_at: "2024-09-02T14:07:19.627205+06:00"
//           }
//         ],
//         conversation_id: 1,
//         timestamp: "2024-09-02T14:07:19.426520+06:00"
//       },
//       {
//         id: 17,
//         sender: 4,
//         text: 'wassup',
//         conversation_id: 1,
//         timestamp: "2024-09-02T14:07:19.426520+06:00"
//       },
//       {
//         id: 17,
//         sender: 4,
//         text: 'text with photo',
//         files: [
//           {
//             id: 7,
//             file: "https://minio.qorgau-city.kz/isec/avatars/avatars/13._%D0%9A%D0%B0%D0%BC%D0%BD%D0%B8.jpg?AWSAccessKeyId=minioadmin&Signature=P7gFpTCO6Xmxm55jlrORJWuhb%2BE%3D&Expires=1725456372",
//             uploaded_at: "2024-09-02T14:07:19.627205+06:00"
//           }
//         ],
//         conversation_id: 1,
//         timestamp: "2024-09-02T14:07:19.426520+06:00"
//       },
//     ]
//   }
// );