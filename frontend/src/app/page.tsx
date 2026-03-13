import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, CheckCircle, Sparkles } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black/80 backdrop-blur-xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg blur opacity-75 group-hover:opacity-100 transition"></div>
                <div className="relative bg-gradient-to-r from-blue-500 to-purple-500 p-2 rounded-lg">
                  <Sparkles className="h-5 w-5 text-white" />
                </div>
              </div>
              <span className="font-semibold text-lg">Jornada</span>
            </Link>

            <nav className="flex items-center gap-4">
              <Link href="/login">
                <Button variant="ghost" className="text-white/70 hover:text-white hover:bg-white/5">
                  Entrar
                </Button>
              </Link>
              <Link href="/register">
                <Button className="bg-white text-black hover:bg-white/90">
                  Começar
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-5xl">
          <div className="text-center space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/20 bg-white/5 text-sm text-white/70">
              <div className="h-1.5 w-1.5 rounded-full bg-green-400 animate-pulse"></div>
              6 frameworks científicos em um único assessment
            </div>

            {/* Main Heading */}
            <h1 className="text-6xl md:text-8xl font-bold tracking-tight">
              Descubra quem
              <br />
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                você realmente é
              </span>
            </h1>

            {/* Subheading */}
            <p className="text-xl md:text-2xl text-white/60 max-w-2xl mx-auto leading-relaxed">
              Assessment comportamental completo. 30 minutos que vão transformar como você se enxerga como empreendedor.
            </p>

            {/* CTA */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/register">
                <Button size="lg" className="bg-white text-black hover:bg-white/90 px-8 py-6 text-lg font-medium">
                  Começar agora
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <div className="flex items-center gap-2 text-sm text-white/50">
                <CheckCircle className="h-4 w-4" />
                <span>Gratuito • Sem cartão</span>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-8 max-w-xl mx-auto pt-16">
              <div className="text-center">
                <div className="text-4xl font-bold mb-1">30min</div>
                <div className="text-sm text-white/50">Duração</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold mb-1">105</div>
                <div className="text-sm text-white/50">Perguntas</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold mb-1">6</div>
                <div className="text-sm text-white/50">Frameworks</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Visual Mockup */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="relative">
            {/* Glow effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-3xl"></div>

            {/* Mockup */}
            <div className="relative border border-white/10 rounded-2xl overflow-hidden bg-gradient-to-br from-white/5 to-white/10 p-8 backdrop-blur">
              <div className="grid grid-cols-3 gap-4">
                <div className="h-40 bg-gradient-to-br from-blue-500/20 to-blue-600/20 rounded-lg border border-white/10"></div>
                <div className="h-40 bg-gradient-to-br from-purple-500/20 to-purple-600/20 rounded-lg border border-white/10"></div>
                <div className="h-40 bg-gradient-to-br from-pink-500/20 to-pink-600/20 rounded-lg border border-white/10"></div>
              </div>
              <div className="mt-4 space-y-2">
                <div className="h-8 bg-white/5 rounded border border-white/10"></div>
                <div className="h-8 bg-white/5 rounded border border-white/10 w-4/5"></div>
                <div className="h-8 bg-white/5 rounded border border-white/10 w-3/5"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-32 px-6 border-t border-white/10">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-2 gap-16">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                Análise completa do seu perfil
              </h2>
              <p className="text-xl text-white/60 leading-relaxed">
                Seis frameworks científicos trabalham juntos para criar um mapa completo de quem você é como líder e empreendedor.
              </p>
            </div>

            <div className="space-y-6">
              {[
                { title: 'DISC', desc: 'Seu estilo de comunicação' },
                { title: 'Espiral Dinâmica', desc: 'Seus valores evolutivos' },
                { title: 'PAEI', desc: 'Seu estilo de gestão' },
                { title: 'Eneagrama', desc: 'Suas motivações profundas' },
                { title: 'Valores', desc: 'O que você prioriza' },
                { title: 'Arquétipos', desc: 'Quem você deve contratar' },
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-4 p-4 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition">
                  <div className="h-2 w-2 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 mt-2"></div>
                  <div>
                    <div className="font-semibold mb-1">{item.title}</div>
                    <div className="text-sm text-white/50">{item.desc}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-32 px-6">
        <div className="container mx-auto max-w-4xl">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Simples. Rápido. Profundo.
            </h2>
            <p className="text-xl text-white/60">
              Três passos para entender quem você é
            </p>
          </div>

          <div className="space-y-12">
            {[
              {
                num: '01',
                title: 'Crie sua conta',
                desc: 'Menos de 1 minuto. Sem cartão de crédito.',
              },
              {
                num: '02',
                title: 'Responda 105 perguntas',
                desc: 'Aproximadamente 30 minutos do seu tempo.',
              },
              {
                num: '03',
                title: 'Receba seu relatório',
                desc: 'Análise completa em PDF. Insights que vão mudar sua forma de liderar.',
              },
            ].map((step, i) => (
              <div key={i} className="flex gap-8 items-start">
                <div className="text-6xl font-bold text-white/10">{step.num}</div>
                <div className="flex-1 pt-2">
                  <h3 className="text-2xl font-bold mb-2">{step.title}</h3>
                  <p className="text-white/60">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-32 px-6">
        <div className="container mx-auto max-w-4xl">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-3xl"></div>
            <div className="relative text-center space-y-8 p-12 border border-white/10 rounded-2xl bg-white/5 backdrop-blur">
              <h2 className="text-4xl md:text-5xl font-bold">
                Pronto para começar?
              </h2>
              <p className="text-xl text-white/60 max-w-2xl mx-auto">
                Junte-se a centenas de empreendedores que já descobriram seus pontos cegos e forças.
              </p>
              <Link href="/register">
                <Button size="lg" className="bg-white text-black hover:bg-white/90 px-8 py-6 text-lg font-medium">
                  Iniciar meu assessment
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-white/40 text-sm">
              © 2026 Jornada do Empreendedor. Todos os direitos reservados.
            </div>
            <div className="flex gap-8 text-sm text-white/40">
              <Link href="/login" className="hover:text-white transition">Login</Link>
              <Link href="/register" className="hover:text-white transition">Cadastro</Link>
              <a href="http://localhost:8000/docs" target="_blank" className="hover:text-white transition">API</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
