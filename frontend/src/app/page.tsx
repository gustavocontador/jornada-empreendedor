import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { CheckCircle, BarChart3, Brain, Target, TrendingUp, Users, Star, Clock, Award, Shield, Sparkles, ArrowRight } from 'lucide-react'

export default function LandingPage() {
  const benefits = [
    {
      icon: <BarChart3 className="h-10 w-10 text-blue-600" />,
      title: 'DISC Profile',
      description: 'Entenda seu estilo de comunicação e comportamento',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: <Brain className="h-10 w-10 text-purple-600" />,
      title: 'Espiral Dinâmica',
      description: 'Descubra seus valores e estágio de consciência',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: <Target className="h-10 w-10 text-indigo-600" />,
      title: 'PAEI de Adizes',
      description: 'Identifique seus papéis de gestão naturais',
      color: 'from-indigo-500 to-indigo-600'
    },
    {
      icon: <TrendingUp className="h-10 w-10 text-emerald-600" />,
      title: 'Eneagrama',
      description: 'Conheça sua personalidade e padrões de comportamento',
      color: 'from-emerald-500 to-emerald-600'
    },
    {
      icon: <Users className="h-10 w-10 text-cyan-600" />,
      title: 'Valores Empresariais',
      description: 'Mapeie o que realmente importa para você',
      color: 'from-cyan-500 to-cyan-600'
    },
    {
      icon: <Award className="h-10 w-10 text-amber-600" />,
      title: 'Arquétipos',
      description: 'Identifique perfis ideais para sua equipe',
      color: 'from-amber-500 to-amber-600'
    },
  ]

  const stats = [
    { number: '6', label: 'Frameworks Científicos', icon: <Sparkles className="h-5 w-5" /> },
    { number: '105', label: 'Perguntas Otimizadas', icon: <CheckCircle className="h-5 w-5" /> },
    { number: '30min', label: 'Tempo de Assessment', icon: <Clock className="h-5 w-5" /> },
    { number: '15-20', label: 'Páginas de Relatório', icon: <BarChart3 className="h-5 w-5" /> },
  ]

  const testimonials = [
    {
      name: 'Maria Silva',
      role: 'CEO, TechStart',
      content: 'O assessment me ajudou a entender meus pontos cegos como líder. Mudou completamente como eu gerencio minha equipe.',
      rating: 5
    },
    {
      name: 'João Santos',
      role: 'Fundador, InovaHub',
      content: 'Finalmente entendi por que eu delegava mal. O relatório PAEI foi revelador!',
      rating: 5
    },
    {
      name: 'Ana Costa',
      role: 'Empresária, Wellness Co',
      content: 'Os insights sobre Espiral Dinâmica me ajudaram a alinhar meus valores com o negócio.',
      rating: 5
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white/90 backdrop-blur-md sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
              J
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Jornada do Empreendedor
            </h1>
          </div>
          <div className="flex gap-3">
            <Link href="/login">
              <Button variant="ghost" className="font-medium">Entrar</Button>
            </Link>
            <Link href="/register">
              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 font-medium shadow-lg shadow-blue-500/20">
                Começar Agora
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-24 md:py-32">
        <div className="max-w-5xl mx-auto text-center space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-sm font-medium">
            <Shield className="h-4 w-4" />
            Baseado em 6 Metodologias Científicas
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold leading-tight">
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-600 bg-clip-text text-transparent animate-gradient">
              Descubra Seu Verdadeiro
            </span>
            <br />
            <span className="text-slate-900">Potencial Empreendedor</span>
          </h1>

          <p className="text-xl md:text-2xl text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Assessment comportamental completo em <span className="font-semibold text-blue-600">30 minutos</span>.
            Receba um relatório detalhado com análise profunda de 6 frameworks psicométricos.
          </p>

          {/* Stats Pills */}
          <div className="flex flex-wrap justify-center gap-4 pt-4">
            {stats.map((stat, idx) => (
              <div key={idx} className="flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-slate-200 shadow-sm">
                <div className="text-blue-600">{stat.icon}</div>
                <div className="text-left">
                  <div className="font-bold text-slate-900">{stat.number}</div>
                  <div className="text-xs text-slate-600">{stat.label}</div>
                </div>
              </div>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
            <Link href="/register">
              <Button size="lg" className="text-lg px-10 py-7 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-xl shadow-blue-500/30 hover:shadow-2xl hover:shadow-blue-500/40 transition-all duration-300 font-semibold group">
                Iniciar Assessment Gratuito
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-10 py-7 border-2 border-slate-300 hover:border-blue-600 hover:text-blue-600 font-semibold">
                Já tenho conta
              </Button>
            </Link>
          </div>

          <p className="text-sm text-slate-500 pt-4">
            ✓ Sem cartão de crédito &nbsp;•&nbsp; ✓ Resultados instantâneos &nbsp;•&nbsp; ✓ Relatório PDF incluído
          </p>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="container mx-auto px-4 py-20 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
              6 Frameworks em Um Único Assessment
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Análise completa e integrada do seu perfil empreendedor
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {benefits.map((benefit, index) => (
              <Card key={index} className="group hover:shadow-2xl hover:scale-105 transition-all duration-300 border-2 hover:border-blue-200 bg-gradient-to-br from-white to-slate-50">
                <CardHeader className="space-y-4">
                  <div className={`h-16 w-16 rounded-2xl bg-gradient-to-br ${benefit.color} p-3 shadow-lg group-hover:scale-110 transition-transform`}>
                    <div className="text-white">{benefit.icon}</div>
                  </div>
                  <CardTitle className="text-xl font-bold text-slate-900">{benefit.title}</CardTitle>
                  <CardDescription className="text-slate-600 text-base">{benefit.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Social Proof / Testimonials */}
      <section className="bg-gradient-to-br from-blue-50 to-purple-50 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
              Transformando Empreendedores
            </h2>
            <p className="text-xl text-slate-600">
              Veja o que outros empreendedores descobriram
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="bg-white border-2 hover:border-blue-200 hover:shadow-xl transition-all">
                <CardHeader>
                  <div className="flex gap-1 mb-3">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 fill-amber-400 text-amber-400" />
                    ))}
                  </div>
                  <CardDescription className="text-base text-slate-700 italic leading-relaxed">
                    "{testimonial.content}"
                  </CardDescription>
                  <div className="pt-4 border-t mt-4">
                    <div className="font-semibold text-slate-900">{testimonial.name}</div>
                    <div className="text-sm text-slate-600">{testimonial.role}</div>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
              Simples e Rápido
            </h2>
            <p className="text-xl text-slate-600">
              Apenas 3 passos para transformar sua jornada
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="relative">
              {/* Connection Line */}
              <div className="hidden md:block absolute left-12 top-16 bottom-16 w-0.5 bg-gradient-to-b from-blue-600 to-purple-600"></div>

              <div className="space-y-12">
                {[
                  {
                    number: '1',
                    title: 'Cadastre-se Gratuitamente',
                    description: 'Crie sua conta em menos de 1 minuto. Sem cartão de crédito necessário.',
                    icon: <Users className="h-6 w-6" />
                  },
                  {
                    number: '2',
                    title: 'Responda o Questionário',
                    description: '105 perguntas cuidadosamente elaboradas. Aproximadamente 30 minutos do seu tempo.',
                    icon: <CheckCircle className="h-6 w-6" />
                  },
                  {
                    number: '3',
                    title: 'Receba Seus Resultados',
                    description: 'Relatório completo em PDF com análise profunda, gráficos e recomendações personalizadas.',
                    icon: <Award className="h-6 w-6" />
                  }
                ].map((step, idx) => (
                  <div key={idx} className="flex gap-6 relative">
                    <div className="flex-shrink-0">
                      <div className="h-24 w-24 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white shadow-xl relative z-10">
                        <span className="text-3xl font-bold">{step.number}</span>
                      </div>
                    </div>
                    <Card className="flex-1 border-2 hover:border-blue-200 hover:shadow-lg transition-all">
                      <CardHeader>
                        <div className="flex items-center gap-3 mb-2">
                          <div className="text-blue-600">{step.icon}</div>
                          <CardTitle className="text-2xl">{step.title}</CardTitle>
                        </div>
                        <CardDescription className="text-base text-slate-600 leading-relaxed">
                          {step.description}
                        </CardDescription>
                      </CardHeader>
                    </Card>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-24">
        <div className="max-w-5xl mx-auto">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 via-purple-600 to-blue-700 p-12 md:p-16 text-white shadow-2xl">
            {/* Decorative elements */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>

            <div className="relative z-10 text-center space-y-8">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 backdrop-blur-sm border border-white/30 text-sm font-medium">
                <Sparkles className="h-4 w-4" />
                Comece Sua Transformação Hoje
              </div>

              <h2 className="text-4xl md:text-5xl font-extrabold leading-tight">
                Pronto para Descobrir Seu<br />Verdadeiro Potencial?
              </h2>

              <p className="text-xl md:text-2xl opacity-95 max-w-2xl mx-auto leading-relaxed">
                Junte-se a centenas de empreendedores que já transformaram sua forma de liderar e gerenciar seus negócios.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
                <Link href="/register">
                  <Button size="lg" className="text-lg px-10 py-7 bg-white text-blue-600 hover:bg-slate-50 shadow-xl font-semibold group">
                    Iniciar Meu Assessment Gratuito
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-12 border-t border-white/20">
                <div>
                  <div className="text-3xl md:text-4xl font-bold mb-1">6</div>
                  <div className="text-sm opacity-90">Frameworks</div>
                </div>
                <div>
                  <div className="text-3xl md:text-4xl font-bold mb-1">105</div>
                  <div className="text-sm opacity-90">Perguntas</div>
                </div>
                <div>
                  <div className="text-3xl md:text-4xl font-bold mb-1">30min</div>
                  <div className="text-sm opacity-90">Duração</div>
                </div>
                <div>
                  <div className="text-3xl md:text-4xl font-bold mb-1">100%</div>
                  <div className="text-sm opacity-90">Gratuito</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-slate-50">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
                  J
                </div>
                <h3 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Jornada do Empreendedor
                </h3>
              </div>
              <p className="text-slate-600 max-w-sm leading-relaxed">
                Assessment comportamental completo baseado em 6 metodologias científicas para empreendedores que querem crescer.
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 className="font-semibold text-slate-900 mb-4">Produto</h4>
              <ul className="space-y-2 text-slate-600">
                <li><Link href="/register" className="hover:text-blue-600 transition-colors">Começar Agora</Link></li>
                <li><Link href="/login" className="hover:text-blue-600 transition-colors">Login</Link></li>
                <li><a href="http://localhost:8000/docs" target="_blank" className="hover:text-blue-600 transition-colors">API Docs</a></li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h4 className="font-semibold text-slate-900 mb-4">Suporte</h4>
              <ul className="space-y-2 text-slate-600">
                <li><a href="#" className="hover:text-blue-600 transition-colors">Central de Ajuda</a></li>
                <li><a href="#" className="hover:text-blue-600 transition-colors">Contato</a></li>
                <li><a href="#" className="hover:text-blue-600 transition-colors">Privacidade</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-slate-200 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-slate-600 text-sm">
              &copy; 2026 Jornada do Empreendedor de Sucesso. Todos os direitos reservados.
            </p>
            <div className="flex items-center gap-2">
              <Shield className="h-4 w-4 text-slate-400" />
              <span className="text-sm text-slate-600">Seus dados estão protegidos</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
