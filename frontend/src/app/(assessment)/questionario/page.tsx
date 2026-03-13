'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { useAssessment } from '@/hooks/useAssessment'
import { QuestionCard } from '@/components/assessment/QuestionCard'
import { ProgressBar } from '@/components/assessment/ProgressBar'
import { QuestionNavigation } from '@/components/assessment/QuestionNavigation'
import { Button } from '@/components/ui/button'
import { LogOut } from 'lucide-react'

export default function QuestionarioPage() {
  const router = useRouter()
  const { user, isAuthenticated, logout } = useAuth()
  const {
    assessment,
    currentQuestion,
    responses,
    progress,
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
  } = useAssessment()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    // Iniciar ou carregar assessment existente
    const initAssessment = async () => {
      try {
        // Verificar se há assessment em progresso via API
        // Por enquanto, sempre inicia novo
        await startAssessment()
      } catch (err) {
        console.error('Erro ao iniciar assessment:', err)
      }
    }

    if (!assessment) {
      initAssessment()
    }
  }, [isAuthenticated, assessment, router])

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Redirecionando...</p>
      </div>
    )
  }

  if (loading && !currentQuestion) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Carregando questionário...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center space-y-4 max-w-md">
          <p className="text-destructive">{error}</p>
          <Button onClick={() => router.push('/')}>Voltar para Início</Button>
        </div>
      </div>
    )
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Carregando pergunta...</p>
      </div>
    )
  }

  const handleAnswer = (value: any) => {
    answerQuestion(currentQuestion.id, value)
  }

  const handleNext = () => {
    nextQuestion()
  }

  const handlePrevious = () => {
    previousQuestion()
  }

  const handleComplete = async () => {
    try {
      await completeAssessment()
    } catch (err) {
      console.error('Erro ao completar assessment:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-lg font-bold text-primary">Jornada do Empreendedor</h1>
            {user && <p className="text-sm text-muted-foreground">Olá, {user.name}</p>}
          </div>
          <Button variant="ghost" size="sm" onClick={logout}>
            <LogOut className="mr-2 h-4 w-4" />
            Sair
          </Button>
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-4 py-8">
        <ProgressBar current={progress.current} total={progress.total} percentage={progress.percentage} />

        <QuestionCard question={currentQuestion} value={responses[currentQuestion.id]} onChange={handleAnswer} />

        <QuestionNavigation
          canGoPrevious={canGoPrevious()}
          canGoNext={canGoNext()}
          isLastQuestion={isLastQuestion()}
          onPrevious={handlePrevious}
          onNext={handleNext}
          onComplete={handleComplete}
          loading={loading}
        />
      </main>
    </div>
  )
}
