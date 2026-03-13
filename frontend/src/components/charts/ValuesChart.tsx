'use client'

import { ValuesResult } from '@/types/result'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface ValuesChartProps {
  data: ValuesResult
}

export function ValuesChart({ data }: ValuesChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Seus Valores Principais</CardTitle>
        <CardDescription>Os valores que mais guiam suas decisões e comportamentos</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {data.top_values.map((value, index) => (
            <div key={index} className="p-4 bg-muted rounded-lg border-l-4 border-primary">
              <div className="flex items-center gap-3 mb-2">
                <span className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-bold">
                  {index + 1}
                </span>
                <h4 className="font-semibold text-lg">{value}</h4>
              </div>
              <p className="text-sm text-muted-foreground ml-11">{data.descriptions[value]}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
