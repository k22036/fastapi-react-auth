const BASE_URL = '/auth'

// ---- Request / Response types ----

export interface SignUpRequest {
  email: string
  password: string
}

export interface SignInRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface MessageResponse {
  message: string
}

// ---- Error handling ----

async function handleResponse<T>(res: Response): Promise<T> {
  if (res.ok) return res.json() as Promise<T>

  const body = await res.json().catch(() => null)
  const detail = body?.detail

  if (typeof detail === 'string') throw new Error(detail)

  // Pydantic バリデーションエラー: { loc, msg, type }[] の形式
  if (Array.isArray(detail)) {
    const messages = detail.map((d: { msg: string }) => d.msg).join(' / ')
    throw new Error(messages)
  }

  throw new Error('予期しないエラーが発生しました')
}

// ---- API functions ----

export async function signUp(data: SignUpRequest): Promise<MessageResponse> {
  const res = await fetch(`${BASE_URL}/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse<MessageResponse>(res)
}

export async function signIn(data: SignInRequest): Promise<TokenResponse> {
  const res = await fetch(`${BASE_URL}/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse<TokenResponse>(res)
}

export async function signOut(token: string): Promise<MessageResponse> {
  const res = await fetch(`${BASE_URL}/signout`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
  return handleResponse<MessageResponse>(res)
}
