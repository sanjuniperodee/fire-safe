import type { Statement } from '@/types/Statement'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { statementService } from '@/services/statement.service'

export const useStatementStore = defineStore('StatementStore', () => {
  const statement = ref<Statement | null>(null)
  const myStatement = ref<Statement | null>(null)

  const selectedStatements = ref<Statement[] | null>(null)
  const calledStatements = ref<Statement[] | null>(null)

  const statements = ref<Statement[]>([])
  const myStatements = ref<Statement[]>([])

  const statementsCount = ref(0)
  const selectedStatementsCount = ref(0)
  const myStatementsCount = ref(0)
  const isLoading = ref<boolean>(false)

  const getAllStatements = async (limit: number, offset: number) => {
    isLoading.value = true
    try {
      const data = await statementService.getAllStatements(limit, offset)
      statements.value = data.results
      statementsCount.value = data.count
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const getAllStatementsFiltered = async (
    limit: number, offset: number,
    min_price: number, max_price: number,
    seen: boolean
  ) => {
    isLoading.value = true
    try {
      const data = await statementService.
      getAllStatementsFiltered(limit, offset, min_price, max_price, seen)
      statements.value = data.results
      statementsCount.value = data.count
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const getStatementById = async (id: number) => {
    isLoading.value = true
    try {
      statement.value = await statementService.getStatementById(id)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const createStatement = async (formData: FormData) => {
    isLoading.value = true
    try {
      await statementService.createStatement(formData)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const getMyStatementById = async (id: number) => {
    isLoading.value = true
    try {
      myStatement.value = await statementService.getMyStatementById(id)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const noteStatement = async (id: number) => {
    isLoading.value = true
    try {
      const data = await statementService.noteStatement(id)
      return data
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const getSelectedStatements = async (limit: number, offset: number) => {
    isLoading.value = true
    try {
      const data = await statementService.getSelectedStatements(limit, offset)
      selectedStatements.value = data.results
      selectedStatementsCount.value = data.count
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const getCalledStatements = async (limit: number, offset: number) => {
    isLoading.value = true
    try {
      calledStatements.value = await statementService.getCalledStatements(limit, offset)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const deleteCalledStatement = async (id: number) => {
    isLoading.value = true
    try {
      await statementService.deleteCalledStatement(id)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const getMyStatements = async (limit: number, offset: number) => {
    isLoading.value = true
    try {
      const data = await statementService.getMyStatements(limit, offset)
      myStatements.value = data.results
      myStatementsCount.value = data.count
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const editMyStatement = async (id: number, formData: FormData) => {
    isLoading.value = true
    try {
      myStatement.value = await statementService.editMyStatement(id, formData)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const deleteMyStatement = async (id: number) => {
    isLoading.value = true
    try {
      await statementService.deleteMyStatement(id)
      myStatements.value = myStatements.value.filter((statement) => statement.id !== id)
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  return {
    statement,
    myStatement,
    selectedStatements,
    calledStatements,
    statements,
    myStatements,
    statementsCount,
    selectedStatementsCount,
    myStatementsCount,
    isLoading,
    createStatement,
    getAllStatements,
    getAllStatementsFiltered,
    getStatementById,
    getMyStatementById,
    noteStatement,
    getSelectedStatements,
    getCalledStatements,
    deleteCalledStatement,
    getMyStatements,
    editMyStatement,
    deleteMyStatement
  }
})
