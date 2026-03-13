import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/authStore'
import api from '@/lib/api'
import { LoginRequest, RegisterRequest, AuthResponse } from '@/types/user'

export function useAuth() {
  const router = useRouter()
  const { user, isAuthenticated, isAdmin, setAuth, logout, initAuth } = useAuthStore()

  useEffect(() => {
    initAuth()
  }, [initAuth])

  const login = async (data: LoginRequest) => {
    try {
      const response = await api.post<AuthResponse>('/auth/login', data)
      setAuth(response.data.token, response.data.user)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao fazer login')
    }
  }

  const register = async (data: RegisterRequest) => {
    try {
      const response = await api.post<AuthResponse>('/auth/register', data)
      setAuth(response.data.token, response.data.user)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao criar conta')
    }
  }

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return {
    user,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout: handleLogout,
  }
}
