import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Rotas que requerem autenticação
const protectedRoutes = ['/questionario', '/resultado', '/dashboard', '/clientes']

// Rotas que requerem admin
const adminRoutes = ['/dashboard', '/clientes']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Verificar se é uma rota protegida
  const isProtectedRoute = protectedRoutes.some((route) => pathname.startsWith(route))
  const isAdminRoute = adminRoutes.some((route) => pathname.startsWith(route))

  // Obter token do cookie (se estiver usando cookies) ou headers
  // Nota: Como estamos usando localStorage, a verificação real será feita no cliente
  // Este middleware é mais para redirecionamentos baseados em rotas

  if (isProtectedRoute) {
    // Aqui você pode adicionar lógica adicional se necessário
    // Por enquanto, a proteção real está nos componentes usando useAuth
    return NextResponse.next()
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}
