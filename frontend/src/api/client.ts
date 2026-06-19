import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE,
})

// Attach JWT token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Redirect to login on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth endpoints
export const authApi = {
  login   : (username: string, password: string) =>
    api.post('/auth/token', new URLSearchParams({ username, password })),
  register: (username: string, email: string, password: string) =>
    api.post('/auth/register', { username, email, password }),
  me      : () => api.get('/auth/me'),
}

// Task endpoints
export const tasksApi = {
  create  : (title: string, description: string) =>
    api.post('/api/tasks', { title, description }),
  list    : () => api.get('/api/tasks'),
  get     : (id: string) => api.get(`/api/tasks/${id}`),
  toolLogs: () => api.get('/api/tool-logs'),
}