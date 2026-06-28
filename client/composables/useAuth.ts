import { ref, computed } from 'vue'

interface UserProfile {
  id: string
  first_name: string
  last_name: string
  email: string
  login_count: number
  account_expiry: string
  active: boolean
  other_metadata: Record<string, unknown> | null
}

interface AdminUser {
  id: number
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  is_staff: boolean
  is_superuser: boolean
  date_joined: string
}

interface PaginatedUsers {
  count: number
  next: string | null
  previous: string | null
  results: AdminUser[]
}

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  user: UserProfile | null
  isStaff: boolean
  isSuperuser: boolean
}

const state = ref<AuthState>({
  accessToken: null,
  refreshToken: null,
  user: null,
  isStaff: false,
  isSuperuser: false,
})

const formatApiError = (err: unknown, fallback = 'Request failed'): string => {
  if (!err) return fallback
  if (typeof err === 'string') return err
  if (err instanceof Error) return err.message
  const obj = err as Record<string, unknown>
  if (obj.detail) {
    if (typeof obj.detail === 'string') return obj.detail
    if (Array.isArray(obj.detail)) return obj.detail.map((e) => formatApiError(e, fallback)).join(', ')
    return formatApiError(obj.detail, fallback)
  }
  if (Array.isArray(obj)) return obj.map((e) => formatApiError(e, fallback)).join(', ')
  const messages = Object.entries(obj).flatMap(([key, value]) => {
    if (key === 'status_code' || key === 'code') return []
    if (Array.isArray(value)) {
      return value.map((v) => (typeof v === 'string' ? v : `${key}: ${formatApiError(v, fallback)}`))
    }
    if (typeof value === 'string') return [`${key}: ${value}`]
    return [`${key}: ${formatApiError(value, fallback)}`]
  })
  return messages.join(', ') || fallback
}

export const useAuth = () => {
  const config = useRuntimeConfig()

  const apiBase = `${config.public.apiURL}/auth`

  const isAuthenticated = computed(() => {
    if (import.meta.server) return false
    return !!state.value.accessToken || !!localStorage.getItem('access_token')
  })

  const currentUser = computed(() => state.value.user)

  const isStaff = computed(() => state.value.isStaff)

  const isSuperuser = computed(() => state.value.isSuperuser)

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
      throw new Error(formatApiError(err, 'Login failed'))
    }
    const raw = await res.json()
    const data = raw.data?.attributes || raw
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('user_email', email)
    state.value.accessToken = data.access
    state.value.refreshToken = data.refresh
    state.value.user = {
      id: '',
      first_name: '',
      last_name: '',
      email,
      login_count: 0,
      account_expiry: '',
      active: true,
      other_metadata: null,
    }
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
      throw new Error(formatApiError(err, 'Registration failed'))
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
      throw new Error(formatApiError(err, 'Activation failed'))
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
    const headers = { ...(options.headers || {}), 'Authorization': `Bearer ${token}` } as Record<string, string>
    if (!headers['Content-Type']) {
      headers['Content-Type'] = 'application/json'
    }
    let res = await fetch(url, { ...options, headers })
    if (res.status === 401) {
      const newToken = await refreshTokens()
      if (newToken) {
        const retryHeaders = { ...headers, 'Authorization': `Bearer ${newToken}` }
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
    const raw = await res.json()
    const data = raw.data?.attributes || raw
    const userData = data.user || data
    state.value.user = {
      id: userData.id || data.id || '',
      first_name: userData.first_name || '',
      last_name: userData.last_name || '',
      email: userData.email || '',
      login_count: userData.login_count ?? 0,
      account_expiry: userData.account_expiry || '',
      active: userData.active ?? true,
      other_metadata: data.other_metadata || userData.other_metadata || null,
    }

    try {
      const selfRes = await authedFetch(`${apiBase}/users/me/`)
      if (selfRes.ok) {
        const selfData = await selfRes.json()
        const attrs = selfData.data?.attributes || selfData
        // DRF JSON:API may return keys as snake_case, kebab-case, or camelCase
        const getBool = (obj: Record<string, unknown>, ...keys: string[]) => {
          for (const key of keys) {
            if (key in obj) return Boolean(obj[key])
          }
          return false
        }
        state.value.isStaff = getBool(attrs, 'is_staff', 'is-staff', 'isStaff')
        state.value.isSuperuser = getBool(attrs, 'is_superuser', 'is-superuser', 'isSuperuser')
      } else {
        state.value.isStaff = false
        state.value.isSuperuser = false
      }
    } catch {
      state.value.isStaff = false
      state.value.isSuperuser = false
    }

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
          msg = err.errors.map((e: { detail?: string; code?: string }) => e.detail || e.code || JSON.stringify(e)).join(', ')
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

  const changePassword = async (currentPassword: string, newPassword: string, reNewPassword: string) => {
    const res = await authedFetch(`${apiBase}/users/set_password/`, {
      method: 'POST',
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
        re_new_password: reNewPassword,
      }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Password change failed'))
    }
    return res.json()
  }

  const resetPassword = async (email: string) => {
    const res = await fetch(`${apiBase}/users/reset_password/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Password reset request failed'))
    }
    return res.json()
  }

  const resetPasswordConfirm = async (uid: string, token: string, newPassword: string, reNewPassword: string) => {
    const res = await fetch(`${apiBase}/users/reset_password_confirm/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ uid, token, new_password: newPassword, re_new_password: reNewPassword }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Password reset failed'))
    }
    return res.json()
  }

  const fetchUsers = async (): Promise<PaginatedUsers> => {
    const res = await authedFetch(`${apiBase}/users/`)
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Failed to fetch users'))
    }
    return res.json()
  }

  const createUser = async (email: string, password: string) => {
    const res = await authedFetch(`${apiBase}/users/`, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Failed to create user'))
    }
    return res.json()
  }

  const updateUser = async (userId: number, data: Partial<AdminUser>) => {
    const res = await authedFetch(`${apiBase}/users/${userId}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Failed to update user'))
    }
    return res.json()
  }

  const deleteUser = async (userId: number) => {
    const res = await authedFetch(`${apiBase}/users/${userId}/`, {
      method: 'DELETE',
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Failed to delete user'))
    }
  }

  const fetchAdminStats = async () => {
    const res = await authedFetch(`${config.public.apiURL}/users/admin/stats/`)
    if (!res.ok) {
      const err = await res.json()
      throw new Error(formatApiError(err, 'Failed to fetch admin stats'))
    }
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
      throw new Error(formatApiError(err, 'Social login failed'))
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

  const submitFeedback = async (payload: {
    facility: string
    email_address: string
    contact_number: string
    data_concerns: string
    usability_concerns: string
  }) => {
    const res = await fetch(`${config.public.apiURL}/feedback/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Submission failed' }))
      throw new Error(formatApiError(err, 'Submission failed'))
    }
    return res.json()
  }

  const fetchFeedback = async (params?: string) => {
    let url = `${config.public.apiURL}/feedback/`
    if (params) url += `?${params}`
    const res = await authedFetch(url)
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to fetch feedback' }))
      throw new Error(formatApiError(err, 'Failed to fetch feedback'))
    }
    return res.json()
  }

  const fetchFeedbackDetail = async (id: string) => {
    const res = await authedFetch(`${config.public.apiURL}/feedback/${id}`)
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to fetch feedback detail' }))
      throw new Error(formatApiError(err, 'Failed to fetch feedback detail'))
    }
    return res.json()
  }

  const updateFeedback = async (id: string, data: { status?: string; admin_notes?: string }) => {
    const res = await authedFetch(`${config.public.apiURL}/feedback/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to update feedback' }))
      throw new Error(formatApiError(err, 'Failed to update feedback'))
    }
    return res.json()
  }

  const deleteFeedback = async (id: string) => {
    const res = await authedFetch(`${config.public.apiURL}/feedback/${id}`, {
      method: 'DELETE',
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to delete feedback' }))
      throw new Error(formatApiError(err, 'Failed to delete feedback'))
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    state.value.accessToken = null
    state.value.refreshToken = null
    state.value.user = null
    state.value.isStaff = false
    state.value.isSuperuser = false
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
    isStaff,
    isSuperuser,
    login,
    register,
    activate,
    socialLogin,
    refreshTokens,
    fetchProfile,
    updateProfile,
    changePassword,
    resetPassword,
    resetPasswordConfirm,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,
    fetchAdminStats,
    submitFeedback,
    fetchFeedback,
    fetchFeedbackDetail,
    updateFeedback,
    deleteFeedback,
    logout,
    initAuth,
    getHeaders,
    authedFetch,
    apiBase,
    formatApiError,
  }
}
