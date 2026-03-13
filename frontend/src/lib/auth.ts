const TOKEN_KEY = 'entrepreneur_assessment_token'
const USER_KEY = 'entrepreneur_assessment_user'

export function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token)
  }
}

export function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY)
  }
  return null
}

export function removeToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }
}

export function setUser(user: any): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  }
}

export function getUser(): any | null {
  if (typeof window !== 'undefined') {
    const user = localStorage.getItem(USER_KEY)
    return user ? JSON.parse(user) : null
  }
  return null
}

export function isAuthenticated(): boolean {
  return !!getToken()
}

export function isAdmin(): boolean {
  const user = getUser()
  return user?.role === 'admin'
}
