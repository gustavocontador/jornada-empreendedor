'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import api from '@/lib/api'
import { AssessmentResult } from '@/types/result'
import { DISCChart } from '@/components/charts/DISCChart'
import { SpiralChart } from '@/components/charts/SpiralChart'
import { PAEIChart } from '@/components/charts/PAEIChart'
import { EnneagramChart } from '@/components/charts/EnneagramChart'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Download, Home, LogOut } from 'lucide-react'

export default function ResultadoPage() {
  const router = useRouter()
  const params = useParams()
  const { user, isAuthenticated, logout } = useAuth()
  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const resultId = params.id as string

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    const loadResult = async () => {
      try {
        setLoading(true)
        const response = await api.get<AssessmentResult>(`/results/${resultId}`)
        setResult(response.data)
      } catch (err: any) {
        setError(err.response?.data?.message || 'Erro ao carregar resultado')
      } finally {
        setLoading(false)
      }
    }

    loadResult()
  }, [isAuthenticated, resultId, router])

  const handleDownloadPDF = async () => {
    try {
      const response = await api.get(`/results/${resultId}/pdf`, {
        responseType: 'blob',
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `resultado-assessment-${resultId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      console.error('Erro ao baixar PDF:', err)
      alert('Erro ao gerar PDF. Tente novamente.')
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Redirecionando...</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">Carregando seus resultados...</p>
        </div>
      </div>
    )
  }

  if (error || !result) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="text-center space-y-4 max-w-md">
          <p className="text-destructive">{error || 'Resultado não encontrado'}</p>
          <Button onClick={() => router.push('/')}>Voltar para Início</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-lg font-bold text-primary">Jornada do Empreendedor</h1>
            {user && <p className="text-sm text-muted-foreground">{user.name}</p>}
          </div>
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" onClick={() => router.push('/')}>
              <Home className="mr-2 h-4 w-4" />
              Início
            </Button>
            <Button variant="ghost" size="sm" onClick={logout}>
              <LogOut className="mr-2 h-4 w-4" />
              Sair
            </Button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header Section */}
        <div className="text-center mb-8 space-y-4">
          <h2 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Seus Resultados
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">{result.overall_summary}</p>
          <Button size="lg" onClick={handleDownloadPDF}>
            <Download className="mr-2 h-5 w-5" />
            Gerar Relatório Completo (PDF)
          </Button>
        </div>

        {/* Tabs com os frameworks */}
        <Tabs defaultValue="disc" className="w-full">
          <TabsList className="grid w-full grid-cols-2 md:grid-cols-5 mb-8">
            <TabsTrigger value="disc">DISC</TabsTrigger>
            <TabsTrigger value="spiral">Espiral Dinâmica</TabsTrigger>
            <TabsTrigger value="paei">PAEI</TabsTrigger>
            <TabsTrigger value="enneagram">Eneagrama</TabsTrigger>
            <TabsTrigger value="values">Valores</TabsTrigger>
          </TabsList>

          <TabsContent value="disc">
            <DISCChart data={result.disc} />
          </TabsContent>

          <TabsContent value="spiral">
            <SpiralChart data={result.spiral_dynamics} />
          </TabsContent>

          <TabsContent value="paei">
            <PAEIChart data={result.paei} />
          </TabsContent>

          <TabsContent value="enneagram">
            <EnneagramChart data={result.enneagram} />
          </TabsContent>

          <TabsContent value="values">
            <Card>
              <CardHeader>
                <CardTitle>Seus Valores Principais</CardTitle>
                <CardDescription>Os valores que mais guiam suas decisões e comportamentos</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {result.values.top_values.map((value, index) => (
                    <div key={index} className="p-4 bg-muted rounded-lg">
                      <h4 className="font-semibold text-lg mb-2">
                        {index + 1}. {value}
                      </h4>
                      <p className="text-sm text-muted-foreground">{result.values.descriptions[value]}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Recomendações */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Recomendações Personalizadas</CardTitle>
            <CardDescription>Com base no seu perfil, sugerimos:</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {result.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center text-sm">
                    {index + 1}
                  </span>
                  <span className="text-sm">{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
