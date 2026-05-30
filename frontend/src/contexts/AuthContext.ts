import { createContext } from 'react'

export interface AuthContextValue {
  token: string | null
  email: string
  isAuthenticated: boolean
  saveToken: (token: string) => void
  clearToken: () => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)
