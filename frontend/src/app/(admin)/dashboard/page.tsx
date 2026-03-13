'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import api from '@/lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { formatDateTime } from '@/lib/utils'
import { Users, ClipboardCheck, TrendingUp, Home, LogOut } from 'lucide-react'

interface DashboardStats {
  totalUsers: number
  totalAssessments: number
  completedAssessments: number
  inProgressAssessments: number
}

interface RecentAssessment {
  id: string
  userId: string
  userName: string
  status: string
  createdAt: string
  completedAt?: string
}

export default function DashboardPage() {
  const router = useRouter()
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentAssessments, setRecentAssessments] = useState<RecentAssessment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    if (!isAdmin) {
      router.push('/')
      return
    }

    const loadDashboard = async () => {
      try {
        setLoading(true)
        const [statsResponse, assessmentsResponse] = await Promise.all([
          api.get<DashboardStats>('/admin/stats'),
          api.get<RecentAssessment[]>('/admin/assessments/recent'),
        ])

        setStats(statsResponse.data)
        setRecentAssessments(assessmentsResponse.data)
      } catch (err) {
        console.error('Erro ao carregar dashboard:', err)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [isAuthenticated, isAdmin, router])

  if (!isAuthenticated || !isAdmin) {
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
          <p className="text-muted-foreground">Carregando dashboard...</p>
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
            <h1 className="text-lg font-bold text-primary">Dashboard Admin</h1>
            {user && <p className="text-sm text-muted-foreground">{user.name}</p>}
          </div>
          <div className="flex gap-2">
            <Link href="/clientes">
              <Button variant="ghost" size="sm">
                <Users className="mr-2 h-4 w-4" />
                Clientes
              </Button>
            </Link>
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
      <main className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold mb-8">Visão Geral</h2>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Usuários</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.totalUsers || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Assessments</CardTitle>
              <ClipboardCheck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.totalAssessments || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completados</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.completedAssessments || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Em Andamento</CardTitle>
              <ClipboardCheck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.inProgressAssessments || 0}</div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Assessments */}
        <Card>
          <CardHeader>
            <CardTitle>Assessments Recentes</CardTitle>
            <CardDescription>Últimos assessments realizados na plataforma</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentAssessments.length === 0 ? (
                <p className="text-sm text-muted-foreground">Nenhum assessment encontrado</p>
              ) : (
                recentAssessments.map((assessment) => (
                  <div key={assessment.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <p className="font-medium">{assessment.userName}</p>
                      <p className="text-sm text-muted-foreground">
                        Iniciado em {formatDateTime(assessment.createdAt)}
                      </p>
                    </div>
                    <div className="text-right">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          assessment.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {assessment.status === 'completed' ? 'Completo' : 'Em Andamento'}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
