export type QuestionType = 'likert_5' | 'multiple_choice' | 'ranking' | 'text'

export interface Question {
  id: string
  text: string
  type: QuestionType
  options?: string[]
  category: string
  order: number
  frameworks: string[]
}

export interface Assessment {
  id: string
  userId: string
  status: 'in_progress' | 'completed'
  currentQuestionIndex: number
  totalQuestions: number
  startedAt: string
  completedAt?: string
  createdAt: string
  updatedAt: string
}

export interface Response {
  id: string
  assessmentId: string
  questionId: string
  response: any
  createdAt: string
  updatedAt: string
}

export interface SaveResponseRequest {
  assessmentId: string
  questionId: string
  response: any
}

export interface AssessmentProgress {
  current: number
  total: number
  percentage: number
}
