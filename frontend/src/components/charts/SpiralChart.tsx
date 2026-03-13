'use client'

import { SpiralDynamicsResult, SPIRAL_COLORS } from '@/types/result'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface SpiralChartProps {
  data: SpiralDynamicsResult
}

export function SpiralChart({ data }: SpiralChartProps) {
  const colors = [
    { key: 'beige', label: 'Bege (Sobrevivência)', value: data.beige, color: SPIRAL_COLORS.beige },
    { key: 'purple', label: 'Roxo (Tribal)', value: data.purple, color: SPIRAL_COLORS.purple },
    { key: 'red', label: 'Vermelho (Poder)', value: data.red, color: SPIRAL_COLORS.red },
    { key: 'blue', label: 'Azul (Ordem)', value: data.blue, color: SPIRAL_COLORS.blue },
    { key: 'orange', label: 'Laranja (Sucesso)', value: data.orange, color: SPIRAL_COLORS.orange },
    { key: 'green', label: 'Verde (Comunidade)', value: data.green, color: SPIRAL_COLORS.green },
    { key: 'yellow', label: 'Amarelo (Integração)', value: data.yellow, color: SPIRAL_COLORS.yellow },
    { key: 'turquoise', label: 'Turquesa (Holístico)', value: data.turquoise, color: SPIRAL_COLORS.turquoise },
  ]

  // Criar pontos do radar
  const centerX = 200
  const centerY = 200
  const maxRadius = 150
  const angleStep = (2 * Math.PI) / 8

  const points = colors.map((color, index) => {
    const angle = index * angleStep - Math.PI / 2
    const radius = (color.value / 100) * maxRadius
    const x = centerX + radius * Math.cos(angle)
    const y = centerY + radius * Math.sin(angle)
    return { x, y, ...color }
  })

  const pathData = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z'

  // Linhas de grade
  const gridLevels = [25, 50, 75, 100]
  const gridPaths = gridLevels.map((level) => {
    const radius = (level / 100) * maxRadius
    return colors.map((_, index) => {
      const angle = index * angleStep - Math.PI / 2
      const x = centerX + radius * Math.cos(angle)
      const y = centerY + radius * Math.sin(angle)
      return { x, y }
    })
  })

  // Linhas dos eixos
  const axisLines = colors.map((_, index) => {
    const angle = index * angleStep - Math.PI / 2
    const x = centerX + maxRadius * Math.cos(angle)
    const y = centerY + maxRadius * Math.sin(angle)
    return { x, y }
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Espiral Dinâmica</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center">
          <svg width="400" height="400" viewBox="0 0 400 400" className="mb-4">
            {/* Linhas de grade */}
            {gridPaths.map((gridPath, i) => (
              <polygon
                key={`grid-${i}`}
                points={gridPath.map((p) => `${p.x},${p.y}`).join(' ')}
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="1"
              />
            ))}

            {/* Linhas dos eixos */}
            {axisLines.map((point, i) => (
              <line
                key={`axis-${i}`}
                x1={centerX}
                y1={centerY}
                x2={point.x}
                y2={point.y}
                stroke="#d1d5db"
                strokeWidth="1"
              />
            ))}

            {/* Área preenchida com gradiente */}
            <defs>
              <radialGradient id="spiralGradient">
                <stop offset="0%" stopColor="rgba(99, 102, 241, 0.3)" />
                <stop offset="100%" stopColor="rgba(99, 102, 241, 0.1)" />
              </radialGradient>
            </defs>

            <path d={pathData} fill="url(#spiralGradient)" stroke="#6366f1" strokeWidth="2" />

            {/* Pontos */}
            {points.map((point, i) => (
              <circle key={`point-${i}`} cx={point.x} cy={point.y} r="5" fill={point.color} stroke="white" strokeWidth="2" />
            ))}

            {/* Labels */}
            {points.map((point, i) => {
              const angle = i * angleStep - Math.PI / 2
              const labelRadius = maxRadius + 20
              const labelX = centerX + labelRadius * Math.cos(angle)
              const labelY = centerY + labelRadius * Math.sin(angle)
              return (
                <text
                  key={`label-${i}`}
                  x={labelX}
                  y={labelY}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className="text-xs font-medium"
                  fill="#374151"
                >
                  {point.label.split(' ')[0]}
                </text>
              )
            })}
          </svg>

          {/* Legenda */}
          <div className="grid grid-cols-2 gap-3 w-full">
            {colors.map((color) => (
              <div key={color.key} className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: color.color }} />
                <span className="text-xs">{color.label}</span>
                <span className="text-xs font-bold ml-auto">{color.value}%</span>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-muted rounded-lg w-full">
            <h4 className="font-semibold mb-2">
              Cor Dominante: {data.dominant_color.charAt(0).toUpperCase() + data.dominant_color.slice(1)}
            </h4>
            <p className="text-sm text-muted-foreground">{data.description}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
