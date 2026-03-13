import { create } from 'zustand'
import { User } from '@/types/user'
import { getUser, getToken, setToken, setUser as saveUser, removeToken } from '@/lib/auth'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isAdmin: boolean
  setAuth: (token: string, user: User) => void
  logout: () => void
  initAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isAdmin: false,

  setAuth: (token: string, user: User) => {
    setToken(token)
    saveUser(user)
    set({
      token,
      user,
      isAuthenticated: true,
      isAdmin: user.role === 'admin',
    })
  },

  logout: () => {
    removeToken()
    set({
      token: null,
      user: null,
      isAuthenticated: false,
      isAdmin: false,
    })
  },

  initAuth: () => {
    const token = getToken()
    const user = getUser()
    if (token && user) {
      set({
        token,
        user,
        isAuthenticated: true,
        isAdmin: user.role === 'admin',
      })
    }
  },
}))
