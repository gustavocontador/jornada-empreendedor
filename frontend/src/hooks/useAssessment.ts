import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useAssessmentStore } from '@/stores/assessmentStore'
import api from '@/lib/api'
import { Assessment, Question, SaveResponseRequest } from '@/types/assessment'
import { debounce } from '@/lib/utils'

export function useAssessment() {
  const router = useRouter()
  const {
    assessment,
    questions,
    responses,
    currentQuestionIndex,
    setAssessment,
    setQuestions,
    setResponse,
    setCurrentQuestionIndex,
    reset,
    getCurrentQuestion,
    getProgress,
  } = useAssessmentStore()

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startAssessment = async () => {
    try {
      setLoading(true)
      setError(null)

      // Criar novo assessment
      const assessmentResponse = await api.post<Assessment>('/assessments')
      setAssessment(assessmentResponse.data)

      // Carregar perguntas
      const questionsResponse = await api.get<Question[]>('/questions')
      setQuestions(questionsResponse.data)

      return assessmentResponse.data
    } catch (err: any) {
      const message = err.response?.data?.message || 'Erro ao iniciar assessment'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const loadAssessment = async (assessmentId: string) => {
    try {
      setLoading(true)
      setError(null)

      const [assessmentResponse, questionsResponse, responsesResponse] = await Promise.all([
        api.get<Assessment>(`/assessments/${assessmentId}`),
        api.get<Question[]>('/questions'),
        api.get<any[]>(`/assessments/${assessmentId}/responses`),
      ])

      setAssessment(assessmentResponse.data)
      setQuestions(questionsResponse.data)

      // Carregar respostas já salvas
      const savedResponses: Record<string, any> = {}
      responsesResponse.data.forEach((r: any) => {
        savedResponses[r.questionId] = r.response
      })

      responsesResponse.data.forEach((r: any) => {
        setResponse(r.questionId, r.response)
      })

      setCurrentQuestionIndex(assessmentResponse.data.currentQuestionIndex || 0)

      return assessmentResponse.data
    } catch (err: any) {
      const message = err.response?.data?.message || 'Erro ao carregar assessment'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const saveResponse = useCallback(
    debounce(async (questionId: string, response: any) => {
      if (!assessment) return

      try {
        const data: SaveResponseRequest = {
          assessmentId: assessment.id,
          questionId,
          response,
        }
        await api.post('/responses', data)
      } catch (err: any) {
        console.error('Erro ao salvar resposta:', err)
      }
    }, 500),
    [assessment]
  )

  const answerQuestion = (questionId: string, response: any) => {
    setResponse(questionId, response)
    saveResponse(questionId, response)
  }

  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const completeAssessment = async () => {
    if (!assessment) return

    try {
      setLoading(true)
      setError(null)

      const response = await api.post(`/assessments/${assessment.id}/complete`)
      const resultId = response.data.resultId

      // Resetar estado e redirecionar
      reset()
      router.push(`/resultado/${resultId}`)

      return response.data
    } catch (err: any) {
      const message = err.response?.data?.message || 'Erro ao finalizar assessment'
      setError(message)
      throw new Error(message)
    } finally {
      setLoading(false)
    }
  }

  const canGoNext = () => {
    const currentQuestion = getCurrentQuestion()
    if (!currentQuestion) return false
    return !!responses[currentQuestion.id]
  }

  const canGoPrevious = () => {
    return currentQuestionIndex > 0
  }

  const isLastQuestion = () => {
    return currentQuestionIndex === questions.length - 1
  }

  return {
    assessment,
    questions,
    responses,
    currentQuestionIndex,
    currentQuestion: getCurrentQuestion(),
    progress: getProgress(),
    loading,
    error,
    startAssessment,
    loadAssessment,
    answerQuestion,
    nextQuestion,
    previousQuestion,
    completeAssessment,
    canGoNext,
    canGoPrevious,
    isLastQuestion,
  }
}
