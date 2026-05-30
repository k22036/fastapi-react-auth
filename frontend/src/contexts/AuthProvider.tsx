import { useState, type ReactNode } from 'react'
import { AuthContext, type AuthContextValue } from './AuthContext'

const TOKEN_KEY = 'auth_token'

/** JWT ペイロードからメールアドレスを取得する */
function getEmailFromToken(token: string): string {
  try {
    // JWT は base64url エンコードされているため + と / に置換してからデコード
    const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    const payload = JSON.parse(atob(base64)) as Record<string, unknown>
    return typeof payload.sub === 'string' ? payload.sub : ''
  } catch {
    return ''
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(
    () => localStorage.getItem(TOKEN_KEY),
  )

  const saveToken = (newToken: string) => {
    localStorage.setItem(TOKEN_KEY, newToken)
    setTokenState(newToken)
  }

  const clearToken = () => {
    localStorage.removeItem(TOKEN_KEY)
    setTokenState(null)
  }

  const value: AuthContextValue = {
    token,
    email: token ? getEmailFromToken(token) : '',
    isAuthenticated: token !== null,
    saveToken,
    clearToken,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
