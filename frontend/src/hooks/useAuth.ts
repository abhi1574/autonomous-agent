import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authApi, api } from '../api/client'
import { useAuthStore } from '../store/authStore'

export function useAuth() {
  const [loading, setLoading] = useState(false)
  const [error,   setError  ] = useState<string | null>(null)
  const { setAuth, logout }   = useAuthStore()
  const navigate              = useNavigate()

  const login = async (username: string, password: string) => {
    setLoading(true)
    setError(null)
    try {
      // Step 1 — get token
      const res   = await authApi.login(username, password)
      const token = res.data.access_token

      // Step 2 — store token in localStorage immediately
      localStorage.setItem('token', token)

      // Step 3 — set token in axios headers manually before calling /auth/me
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`

      // Step 4 — now call /auth/me with token already set
      const me = await authApi.me()

      // Step 5 — store everything in zustand
      setAuth(token, me.data)

      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
      localStorage.removeItem('token')
    } finally {
      setLoading(false)
    }
  }

  const register = async (username: string, email: string, password: string) => {
    setLoading(true)
    setError(null)
    try {
      await authApi.register(username, email, password)
      navigate('/login')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  const logoutUser = () => {
    logout()
    delete api.defaults.headers.common['Authorization']
    navigate('/login')
  }

  return { login, register, logoutUser, loading, error }
}