'use client'

import { PAEIResult, PAEI_COLORS } from '@/types/result'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface PAEIChartProps {
  data: PAEIResult
}

export function PAEIChart({ data }: PAEIChartProps) {
  const roles = [
    { key: 'P', label: 'Produtor', value: data.P, color: PAEI_COLORS.P },
    { key: 'A', label: 'Administrador', value: data.A, color: PAEI_COLORS.A },
    { key: 'E', label: 'Empreendedor', value: data.E, color: PAEI_COLORS.E },
    { key: 'I', label: 'Integrador', value: data.I, color: PAEI_COLORS.I },
  ]

  // Criar pontos do radar (4 pontos)
  const centerX = 150
  const centerY = 150
  const maxRadius = 120
  const angleStep = (2 * Math.PI) / 4

  const points = roles.map((role, index) => {
    const angle = index * angleStep - Math.PI / 2
    const radius = (role.value / 100) * maxRadius
    const x = centerX + radius * Math.cos(angle)
    const y = centerY + radius * Math.sin(angle)
    return { x, y, ...role }
  })

  const pathData = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z'

  // Linhas de grade
  const gridLevels = [25, 50, 75, 100]
  const gridPaths = gridLevels.map((level) => {
    const radius = (level / 100) * maxRadius
    return roles.map((_, index) => {
      const angle = index * angleStep - Math.PI / 2
      const x = centerX + radius * Math.cos(angle)
      const y = centerY + radius * Math.sin(angle)
      return { x, y }
    })
  })

  // Linhas dos eixos
  const axisLines = roles.map((_, index) => {
    const angle = index * angleStep - Math.PI / 2
    const x = centerX + maxRadius * Math.cos(angle)
    const y = centerY + maxRadius * Math.sin(angle)
    return { x, y }
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Papéis PAEI</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center">
          <svg width="300" height="300" viewBox="0 0 300 300" className="mb-4">
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

            {/* Área preenchida */}
            <defs>
              <radialGradient id="paeiGradient">
                <stop offset="0%" stopColor="rgba(139, 92, 246, 0.3)" />
                <stop offset="100%" stopColor="rgba(139, 92, 246, 0.1)" />
              </radialGradient>
            </defs>

            <path d={pathData} fill="url(#paeiGradient)" stroke="#8b5cf6" strokeWidth="2" />

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
                  className="text-sm font-semibold"
                  fill="#374151"
                >
                  {point.key}
                </text>
              )
            })}
          </svg>

          {/* Legenda */}
          <div className="grid grid-cols-2 gap-3 w-full mb-4">
            {roles.map((role) => (
              <div key={role.key} className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: role.color }} />
                <span className="text-sm">{role.label}</span>
                <span className="text-sm font-bold ml-auto">{role.value}%</span>
              </div>
            ))}
          </div>

          <div className="p-4 bg-muted rounded-lg w-full">
            <h4 className="font-semibold mb-2">Seu Código PAEI: {data.code}</h4>
            <p className="text-sm text-muted-foreground">{data.description}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
