'use client'

import { Question } from '@/types/assessment'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Input } from '@/components/ui/input'

interface QuestionCardProps {
  question: Question
  value: any
  onChange: (value: any) => void
}

export function QuestionCard({ question, value, onChange }: QuestionCardProps) {
  const renderLikert5 = () => {
    const options = [
      { value: '1', label: 'Discordo Totalmente' },
      { value: '2', label: 'Discordo' },
      { value: '3', label: 'Neutro' },
      { value: '4', label: 'Concordo' },
      { value: '5', label: 'Concordo Totalmente' },
    ]

    return (
      <RadioGroup value={value?.toString()} onValueChange={(v) => onChange(parseInt(v))}>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {options.map((option) => (
            <div
              key={option.value}
              className="flex flex-col items-center space-y-2 p-4 border rounded-lg hover:bg-accent cursor-pointer transition-colors"
            >
              <RadioGroupItem value={option.value} id={`option-${option.value}`} className="mx-auto" />
              <Label htmlFor={`option-${option.value}`} className="text-center cursor-pointer text-xs">
                {option.label}
              </Label>
            </div>
          ))}
        </div>
      </RadioGroup>
    )
  }

  const renderMultipleChoice = () => {
    if (!question.options) return null

    return (
      <RadioGroup value={value} onValueChange={onChange}>
        <div className="space-y-3">
          {question.options.map((option, index) => (
            <div
              key={index}
              className="flex items-center space-x-3 p-4 border rounded-lg hover:bg-accent cursor-pointer transition-colors"
            >
              <RadioGroupItem value={option} id={`option-${index}`} />
              <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                {option}
              </Label>
            </div>
          ))}
        </div>
      </RadioGroup>
    )
  }

  const renderRanking = () => {
    if (!question.options) return null

    const rankings = value || {}

    return (
      <div className="space-y-4">
        <p className="text-sm text-muted-foreground">
          Classifique cada opção de 1 (menos importante) a 5 (mais importante)
        </p>
        {question.options.map((option, index) => (
          <div key={index} className="space-y-2">
            <Label>{option}</Label>
            <RadioGroup
              value={rankings[option]?.toString()}
              onValueChange={(v) =>
                onChange({
                  ...rankings,
                  [option]: parseInt(v),
                })
              }
            >
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((rank) => (
                  <div key={rank} className="flex items-center space-x-1">
                    <RadioGroupItem value={rank.toString()} id={`${index}-${rank}`} />
                    <Label htmlFor={`${index}-${rank}`} className="cursor-pointer">
                      {rank}
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          </div>
        ))}
      </div>
    )
  }

  const renderText = () => {
    return (
      <div className="space-y-2">
        <Label htmlFor="text-response">Sua resposta</Label>
        <Input
          id="text-response"
          type="text"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Digite sua resposta aqui..."
          className="w-full"
        />
      </div>
    )
  }

  const renderQuestion = () => {
    switch (question.type) {
      case 'likert_5':
        return renderLikert5()
      case 'multiple_choice':
        return renderMultipleChoice()
      case 'ranking':
        return renderRanking()
      case 'text':
        return renderText()
      default:
        return <p>Tipo de pergunta não suportado</p>
    }
  }

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardContent className="pt-8 pb-8 px-6 md:px-12">
        <div className="space-y-8">
          <div>
            <h2 className="text-2xl md:text-3xl font-semibold text-center mb-2">{question.text}</h2>
            {question.category && (
              <p className="text-sm text-muted-foreground text-center">Categoria: {question.category}</p>
            )}
          </div>

          <div className="mt-8">{renderQuestion()}</div>
        </div>
      </CardContent>
    </Card>
  )
}
