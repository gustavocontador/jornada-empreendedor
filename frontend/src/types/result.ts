export interface DISCResult {
  D: number
  I: number
  S: number
  C: number
  profile: string
  description: string
}

export interface SpiralDynamicsResult {
  beige: number
  purple: number
  red: number
  blue: number
  orange: number
  green: number
  yellow: number
  turquoise: number
  dominant_color: string
  description: string
}

export interface PAEIResult {
  P: number
  A: number
  E: number
  I: number
  code: string
  description: string
}

export interface EnneagramResult {
  type: number
  wing?: string
  description: string
  strengths: string[]
  challenges: string[]
}

export interface ValuesResult {
  top_values: string[]
  descriptions: Record<string, string>
}

export interface AssessmentResult {
  id: string
  assessmentId: string
  userId: string
  disc: DISCResult
  spiral_dynamics: SpiralDynamicsResult
  paei: PAEIResult
  enneagram: EnneagramResult
  values: ValuesResult
  overall_summary: string
  recommendations: string[]
  createdAt: string
  updatedAt: string
}

export const SPIRAL_COLORS = {
  beige: '#F5DEB3',
  purple: '#9370DB',
  red: '#DC143C',
  blue: '#4169E1',
  orange: '#FF8C00',
  green: '#32CD32',
  yellow: '#FFD700',
  turquoise: '#40E0D0'
} as const

export const DISC_COLORS = {
  D: '#FF4444',
  I: '#FFD700',
  S: '#4CAF50',
  C: '#2196F3'
} as const

export const PAEI_COLORS = {
  P: '#8B4513',
  A: '#2F4F4F',
  E: '#FF6347',
  I: '#4682B4'
} as const
