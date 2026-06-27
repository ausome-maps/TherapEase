import { ref, computed } from 'vue'

interface UserProfile {
  id: string
  first_name: string
  last_name: string
  email: string
  login_count: number
  account_expiry: string
  active: boolean
}

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  user: UserProfile | null
}

const state = ref<AuthState>({
  accessToken: null,
  refreshToken: null,
  user: null,
})

export const useAuth = () => {
  const config = useRuntimeConfig()

  const apiBase = `${config.public.apiURL}/auth`

  const isAuthenticated = computed(() => {
    if (import.meta.server) return false
    return !!localStorage.getItem('access_token')
  })

  const currentUser = computed(() => state.value.user)

  const getHeaders = () => {
    const token = localStorage.getItem('access_token')
    if (!token) return { 'Content-Type': 'application/json' }
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    }
  }

  const login = async (email: string, password: string) => {
    const res = await fetch(`${apiBase}/jwt/create/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Login failed')
    }
    const raw = await res.json()
    const data = raw.data?.attributes || raw
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('user_email', email)
    state.value.accessToken = data.access
    state.value.refreshToken = data.refresh
    await fetchProfile()
    return data
  }

  const register = async (email: string, password: string) => {
    const res = await fetch(`${apiBase}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(
        Array.isArray(err) ? Object.values(err).flat().join(', ') : (err.detail || 'Registration failed')
      )
    }
    return res.json()
  }

  const activate = async (uid: string, token: string) => {
    const res = await fetch(`${apiBase}/users/activation/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ uid, token }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Activation failed')
    }
    return res.json()
  }

  const refreshTokens = async () => {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) {
      logout()
      return null
    }
    try {
      const res = await fetch(`${apiBase}/jwt/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      })
      if (!res.ok) {
        logout()
        return null
      }
      const raw = await res.json()
      const data = raw.data?.attributes || raw
      localStorage.setItem('access_token', data.access)
      state.value.accessToken = data.access
      return data.access
    } catch {
      logout()
      return null
    }
  }

  const authedFetch = async (url: string, options: RequestInit = {}) => {
    const token = localStorage.getItem('access_token')
    const headers = { ...(options.headers || {}), 'Authorization': `Bearer ${token}` }
    let res = await fetch(url, { ...options, headers })
    if (res.status === 401) {
      const newToken = await refreshTokens()
      if (newToken) {
        const retryHeaders = { ...(options.headers || {}), 'Authorization': `Bearer ${newToken}` }
        res = await fetch(url, { ...options, headers: retryHeaders })
      }
    }
    return res
  }

  const fetchProfile = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return null
    const res = await authedFetch(`${config.public.apiURL}/users/profile/me/`)
    if (!res.ok) return null
    const data = await res.json()
    state.value.user = data
    return data
  }

  const updateProfile = async (profileData: { first_name?: string; last_name?: string; other_metadata?: Record<string, unknown> }) => {
    const token = localStorage.getItem('access_token')
    if (!token) throw new Error('Not authenticated')

    const body: Record<string, unknown> = {
      user: {
        first_name: profileData.first_name,
        last_name: profileData.last_name,
      },
    }
    if (profileData.other_metadata) {
      body.other_metadata = profileData.other_metadata
    }

    const res = await authedFetch(`${config.public.apiURL}/users/profile/me/`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(body),
    })
    if (!res.ok) {
      const text = await res.text()
      try {
        const err = JSON.parse(text)
        let msg = 'Profile update failed'
        if (err.errors) {
          msg = err.errors.map((e) => e.detail || e.code || JSON.stringify(e)).join(', ')
        } else if (Array.isArray(err)) {
          msg = Object.values(err).flat().join(', ')
        } else if (err.detail) {
          msg = err.detail
        }
        throw new Error(msg)
      } catch (e) {
        if (e instanceof Error && e.message !== 'Profile update failed') throw e
        throw new Error(text.substring(0, 200) || 'Profile update failed')
      }
    }
    await fetchProfile()
    return res.json()
  }

  const socialLogin = async (provider: string, socialToken: string) => {
    const res = await fetch(`${config.public.apiURL}/users/social/jwt/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ provider, access_token: socialToken }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Social login failed')
    }
    const raw = await res.json()
    const data = raw.data?.attributes || raw
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('user_email', provider === 'google-oauth2' ? 'Google User' : 'Facebook User')
    state.value.accessToken = data.access
    state.value.refreshToken = data.refresh
    await fetchProfile()
    return data
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    state.value.accessToken = null
    state.value.refreshToken = null
    state.value.user = null
  }

  const initAuth = async () => {
    if (import.meta.server) return
    const token = localStorage.getItem('access_token')
    if (!token) return
    state.value.accessToken = token
    state.value.refreshToken = localStorage.getItem('refresh_token')
    await fetchProfile()
  }

  return {
    isAuthenticated,
    currentUser,
    login,
    register,
    activate,
    socialLogin,
    refreshTokens,
    fetchProfile,
    updateProfile,
    logout,
    initAuth,
    getHeaders,
    authedFetch,
    apiBase,
  }
}
