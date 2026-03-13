import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { CheckCircle, BarChart3, Brain, Target, TrendingUp, Users } from 'lucide-react'

export default function LandingPage() {
  const benefits = [
    {
      icon: <BarChart3 className="h-8 w-8 text-primary" />,
      title: 'DISC Profile',
      description: 'Entenda seu estilo de comunicação e comportamento',
    },
    {
      icon: <Brain className="h-8 w-8 text-primary" />,
      title: 'Espiral Dinâmica',
      description: 'Descubra seus valores e estágio de consciência',
    },
    {
      icon: <Target className="h-8 w-8 text-primary" />,
      title: 'PAEI de Adizes',
      description: 'Identifique seus papéis de gestão naturais',
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-primary" />,
      title: 'Eneagrama',
      description: 'Conheça sua personalidade e padrões de comportamento',
    },
    {
      icon: <Users className="h-8 w-8 text-primary" />,
      title: 'Valores Pessoais',
      description: 'Mapeie o que realmente importa para você',
    },
    {
      icon: <CheckCircle className="h-8 w-8 text-primary" />,
      title: 'Relatório Completo',
      description: 'Receba análise detalhada e recomendações',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-primary">Jornada do Empreendedor</h1>
          <div className="flex gap-4">
            <Link href="/login">
              <Button variant="ghost">Entrar</Button>
            </Link>
            <Link href="/register">
              <Button>Começar Agora</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto space-y-8">
          <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Descubra Sua Jornada de Sucesso Como Empreendedor
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Assessment comportamental completo em 30 minutos. Entenda profundamente seu perfil empreendedor através de 6
            frameworks científicos.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8 py-6">
                Iniciar Assessment Gratuito
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                Já tenho conta
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="container mx-auto px-4 py-16">
        <h3 className="text-3xl font-bold text-center mb-12">O Que Você Vai Descobrir</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {benefits.map((benefit, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mb-4">{benefit.icon}</div>
                <CardTitle>{benefit.title}</CardTitle>
                <CardDescription>{benefit.description}</CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <h3 className="text-3xl font-bold text-center mb-12">Como Funciona</h3>
          <div className="max-w-3xl mx-auto space-y-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-white">1</span>
                  Cadastre-se Gratuitamente
                </CardTitle>
                <CardDescription>Crie sua conta em menos de 1 minuto</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-white">2</span>
                  Responda o Questionário
                </CardTitle>
                <CardDescription>Aproximadamente 30 minutos de perguntas sobre você</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-white">3</span>
                  Receba Seus Resultados
                </CardTitle>
                <CardDescription>Análise completa com gráficos, insights e recomendações personalizadas</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-3xl mx-auto space-y-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white">
          <h3 className="text-4xl font-bold">Pronto para Começar?</h3>
          <p className="text-xl opacity-90">
            Milhares de empreendedores já descobriram seus pontos fortes e áreas de desenvolvimento. Sua vez!
          </p>
          <Link href="/register">
            <Button size="lg" variant="secondary" className="text-lg px-8 py-6 mt-4">
              Iniciar Meu Assessment Agora
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 bg-white">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>&copy; 2026 Jornada do Empreendedor de Sucesso. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  )
}
