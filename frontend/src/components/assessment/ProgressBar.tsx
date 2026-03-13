'use client'

import { Progress } from '@/components/ui/progress'

interface ProgressBarProps {
  current: number
  total: number
  percentage: number
}

export function ProgressBar({ current, total, percentage }: ProgressBarProps) {
  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      <div className="space-y-2">
        <div className="flex justify-between items-center text-sm">
          <span className="text-muted-foreground">
            Questão {current} de {total}
          </span>
          <span className="font-semibold">{percentage}%</span>
        </div>
        <Progress value={percentage} className="h-2" />
      </div>
    </div>
  )
}
