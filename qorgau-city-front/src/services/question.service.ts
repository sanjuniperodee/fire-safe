import axios from 'axios'
import type { Question } from '@/types/Question'

class QuestionService {
  baseUrl: string
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async getQuestions(): Promise<Question[]> {
    const token = localStorage.getItem('token')!
    const { data } = await axios.get(`${this.baseUrl}/api/v1/faq/`, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })

    return data.results
    // return [
    //   {
    //     id: 1,
    //     question: 'Question 1?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   },
    //   {
    //     id: 2,
    //     question: 'Question 2?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   },
    //   {
    //     id: 3,
    //     question: 'Question 3?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   },
    //   {
    //     id: 4,
    //     question: 'Question 4?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   },
    //   {
    //     id: 5,
    //     question: 'Question 5?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   },
    //   {
    //     id: 6,
    //     question: 'Question 6?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   },
    //   {
    //     id: 7,
    //     question: 'Question 7?',
    //     answer:
    //       'Lorem ipsum dolor sit amet consectetur adipisicing elit. A aut voluptas dolores ad velit hic odio quod quidem molestiae delectus.'
    //   }
    // ]
  }
}

export const questionService = new QuestionService(import.meta.env.VITE_BACKEND_URL)
