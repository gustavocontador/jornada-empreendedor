'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import api from '@/lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { formatDateTime } from '@/lib/utils'
import { Search, Home, LogOut, BarChart3 } from 'lucide-react'

interface Client {
  id: string
  name: string
  email: string
  createdAt: string
  assessmentsCount: number
  completedAssessmentsCount: number
  latestAssessmentId?: string
  latestResultId?: string
}

export default function ClientesPage() {
  const router = useRouter()
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const [clients, setClients] = useState<Client[]>([])
  const [filteredClients, setFilteredClients] = useState<Client[]>([])
  const [searchTerm, setSearchTerm] = useState('')
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

    const loadClients = async () => {
      try {
        setLoading(true)
        const response = await api.get<Client[]>('/admin/clients')
        setClients(response.data)
        setFilteredClients(response.data)
      } catch (err) {
        console.error('Erro ao carregar clientes:', err)
      } finally {
        setLoading(false)
      }
    }

    loadClients()
  }, [isAuthenticated, isAdmin, router])

  useEffect(() => {
    if (searchTerm === '') {
      setFilteredClients(clients)
    } else {
      const filtered = clients.filter(
        (client) =>
          client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          client.email.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredClients(filtered)
    }
  }, [searchTerm, clients])

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
          <p className="text-muted-foreground">Carregando clientes...</p>
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
            <h1 className="text-lg font-bold text-primary">Gerenciar Clientes</h1>
            {user && <p className="text-sm text-muted-foreground">{user.name}</p>}
          </div>
          <div className="flex gap-2">
            <Link href="/dashboard">
              <Button variant="ghost" size="sm">
                <BarChart3 className="mr-2 h-4 w-4" />
                Dashboard
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
        <div className="mb-8 space-y-4">
          <h2 className="text-3xl font-bold">Clientes</h2>

          {/* Search */}
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Buscar por nome ou email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Clients List */}
        <Card>
          <CardHeader>
            <CardTitle>Lista de Clientes ({filteredClients.length})</CardTitle>
            <CardDescription>Todos os usuários cadastrados na plataforma</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {filteredClients.length === 0 ? (
                <p className="text-sm text-muted-foreground">Nenhum cliente encontrado</p>
              ) : (
                filteredClients.map((client) => (
                  <div key={client.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="space-y-1">
                      <p className="font-medium">{client.name}</p>
                      <p className="text-sm text-muted-foreground">{client.email}</p>
                      <p className="text-xs text-muted-foreground">
                        Cadastrado em {formatDateTime(client.createdAt)}
                      </p>
                    </div>
                    <div className="text-right space-y-2">
                      <div className="text-sm">
                        <span className="font-medium">{client.completedAssessmentsCount}</span>
                        <span className="text-muted-foreground"> / {client.assessmentsCount} completados</span>
                      </div>
                      {client.latestResultId && (
                        <Link href={`/resultado/${client.latestResultId}`}>
                          <Button size="sm" variant="outline">
                            Ver Último Resultado
                          </Button>
                        </Link>
                      )}
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
