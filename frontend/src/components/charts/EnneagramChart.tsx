'use client'

import { EnneagramResult } from '@/types/result'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface EnneagramChartProps {
  data: EnneagramResult
}

export function EnneagramChart({ data }: EnneagramChartProps) {
  const types = [
    { number: 1, label: 'O Reformador' },
    { number: 2, label: 'O Ajudador' },
    { number: 3, label: 'O Realizador' },
    { number: 4, label: 'O Individualista' },
    { number: 5, label: 'O Investigador' },
    { number: 6, label: 'O Leal' },
    { number: 7, label: 'O Entusiasta' },
    { number: 8, label: 'O Desafiador' },
    { number: 9, label: 'O Pacificador' },
  ]

  const centerX = 150
  const centerY = 150
  const radius = 100

  // Calcular posições dos tipos no círculo
  const angleStep = (2 * Math.PI) / 9
  const positions = types.map((type, index) => {
    const angle = index * angleStep - Math.PI / 2
    const x = centerX + radius * Math.cos(angle)
    const y = centerY + radius * Math.sin(angle)
    return { ...type, x, y }
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Eneagrama</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center">
          <svg width="300" height="300" viewBox="0 0 300 300" className="mb-6">
            {/* Círculo externo */}
            <circle cx={centerX} cy={centerY} r={radius} fill="none" stroke="#e5e7eb" strokeWidth="2" />

            {/* Linhas internas do eneagrama */}
            <line x1={positions[0].x} y1={positions[0].y} x2={positions[3].x} y2={positions[3].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[0].x} y1={positions[0].y} x2={positions[6].x} y2={positions[6].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[3].x} y1={positions[3].y} x2={positions[6].x} y2={positions[6].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[1].x} y1={positions[1].y} x2={positions[4].x} y2={positions[4].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[1].x} y1={positions[1].y} x2={positions[7].x} y2={positions[7].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[4].x} y1={positions[4].y} x2={positions[7].x} y2={positions[7].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[2].x} y1={positions[2].y} x2={positions[5].x} y2={positions[5].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[2].x} y1={positions[2].y} x2={positions[8].x} y2={positions[8].y} stroke="#d1d5db" strokeWidth="1" />
            <line x1={positions[5].x} y1={positions[5].y} x2={positions[8].x} y2={positions[8].y} stroke="#d1d5db" strokeWidth="1" />

            {/* Pontos dos tipos */}
            {positions.map((pos) => {
              const isUserType = pos.number === data.type
              return (
                <g key={pos.number}>
                  <circle
                    cx={pos.x}
                    cy={pos.y}
                    r={isUserType ? 18 : 12}
                    fill={isUserType ? '#6366f1' : '#94a3b8'}
                    stroke="white"
                    strokeWidth="2"
                  />
                  <text
                    x={pos.x}
                    y={pos.y}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="font-bold"
                    fill="white"
                    fontSize={isUserType ? 16 : 12}
                  >
                    {pos.number}
                  </text>
                </g>
              )
            })}
          </svg>

          <div className="space-y-4 w-full">
            <div className="p-4 bg-primary/10 rounded-lg border-2 border-primary">
              <h4 className="font-bold text-lg mb-2">
                Tipo {data.type}: {types[data.type - 1].label}
              </h4>
              {data.wing && <p className="text-sm text-muted-foreground mb-2">Asa: {data.wing}</p>}
              <p className="text-sm">{data.description}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-green-50 rounded-lg">
                <h5 className="font-semibold text-green-800 mb-2">Forças</h5>
                <ul className="text-sm space-y-1">
                  {data.strengths.map((strength, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-green-600">•</span>
                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-4 bg-orange-50 rounded-lg">
                <h5 className="font-semibold text-orange-800 mb-2">Desafios</h5>
                <ul className="text-sm space-y-1">
                  {data.challenges.map((challenge, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-orange-600">•</span>
                      <span>{challenge}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
