'use client'

import { DISCResult, DISC_COLORS } from '@/types/result'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface DISCChartProps {
  data: DISCResult
}

export function DISCChart({ data }: DISCChartProps) {
  const maxValue = 100
  const dimensions = [
    { key: 'D', label: 'Dominância', value: data.D, color: DISC_COLORS.D },
    { key: 'I', label: 'Influência', value: data.I, color: DISC_COLORS.I },
    { key: 'S', label: 'Estabilidade', value: data.S, color: DISC_COLORS.S },
    { key: 'C', label: 'Conformidade', value: data.C, color: DISC_COLORS.C },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Perfil DISC</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {dimensions.map((dim) => (
            <div key={dim.key} className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">{dim.label}</span>
                <span className="text-sm font-bold">{dim.value}%</span>
              </div>
              <div className="h-8 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full transition-all duration-500 flex items-center justify-center text-white text-xs font-bold"
                  style={{
                    width: `${(dim.value / maxValue) * 100}%`,
                    backgroundColor: dim.color,
                  }}
                >
                  {dim.value > 15 && `${dim.value}%`}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-muted rounded-lg">
          <h4 className="font-semibold mb-2">Seu Perfil: {data.profile}</h4>
          <p className="text-sm text-muted-foreground">{data.description}</p>
        </div>
      </CardContent>
    </Card>
  )
}
