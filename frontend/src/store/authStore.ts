import { create } from 'zustand'

interface User {
  id       : string
  username : string
  email    : string
  is_active: boolean
  role     : 'admin' | 'user' | 'viewer'
}

interface AuthStore {
  token   : string | null
  user    : User | null
  setAuth : (token: string, user: User) => void
  logout  : () => void
  isAuthed: () => boolean
}

export const useAuthStore = create<AuthStore>((set, get) => ({
  token   : localStorage.getItem('token'),
  user    : JSON.parse(localStorage.getItem('user') || 'null'),

  setAuth: (token, user) => {
    console.log('💾 setAuth called with:', { token, user })
    try {
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
      console.log('✅ Saved to localStorage:', { token, user })
    }catch (e){
      console.error('❌ localStorage error:', e)
    }
    set({ token, user })
  },

  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    set({ token: null, user: null })
  },

  isAuthed: () => !!get().token,
}))