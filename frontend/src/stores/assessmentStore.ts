import { create } from 'zustand'
import { Assessment, Question, Response } from '@/types/assessment'

interface AssessmentState {
  assessment: Assessment | null
  questions: Question[]
  responses: Record<string, any>
  currentQuestionIndex: number
  setAssessment: (assessment: Assessment) => void
  setQuestions: (questions: Question[]) => void
  setResponse: (questionId: string, response: any) => void
  setCurrentQuestionIndex: (index: number) => void
  reset: () => void
  getCurrentQuestion: () => Question | null
  getProgress: () => { current: number; total: number; percentage: number }
}

export const useAssessmentStore = create<AssessmentState>((set, get) => ({
  assessment: null,
  questions: [],
  responses: {},
  currentQuestionIndex: 0,

  setAssessment: (assessment: Assessment) => set({ assessment }),

  setQuestions: (questions: Question[]) => set({ questions }),

  setResponse: (questionId: string, response: any) =>
    set((state) => ({
      responses: { ...state.responses, [questionId]: response },
    })),

  setCurrentQuestionIndex: (index: number) => set({ currentQuestionIndex: index }),

  reset: () =>
    set({
      assessment: null,
      questions: [],
      responses: {},
      currentQuestionIndex: 0,
    }),

  getCurrentQuestion: () => {
    const { questions, currentQuestionIndex } = get()
    return questions[currentQuestionIndex] || null
  },

  getProgress: () => {
    const { currentQuestionIndex, questions } = get()
    const total = questions.length
    const current = currentQuestionIndex + 1
    const percentage = total > 0 ? Math.round((current / total) * 100) : 0
    return { current, total, percentage }
  },
}))
