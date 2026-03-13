'use client'

import { Button } from '@/components/ui/button'
import { ChevronLeft, ChevronRight, Check } from 'lucide-react'

interface QuestionNavigationProps {
  canGoPrevious: boolean
  canGoNext: boolean
  isLastQuestion: boolean
  onPrevious: () => void
  onNext: () => void
  onComplete: () => void
  loading?: boolean
}

export function QuestionNavigation({
  canGoPrevious,
  canGoNext,
  isLastQuestion,
  onPrevious,
  onNext,
  onComplete,
  loading = false,
}: QuestionNavigationProps) {
  return (
    <div className="w-full max-w-4xl mx-auto mt-8">
      <div className="flex justify-between items-center gap-4">
        <Button variant="outline" onClick={onPrevious} disabled={!canGoPrevious || loading} className="min-w-32">
          <ChevronLeft className="mr-2 h-4 w-4" />
          Anterior
        </Button>

        {isLastQuestion ? (
          <Button onClick={onComplete} disabled={!canGoNext || loading} className="min-w-32" size="lg">
            {loading ? (
              'Processando...'
            ) : (
              <>
                <Check className="mr-2 h-4 w-4" />
                Finalizar
              </>
            )}
          </Button>
        ) : (
          <Button onClick={onNext} disabled={!canGoNext || loading} className="min-w-32">
            Próximo
            <ChevronRight className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>
    </div>
  )
}
