import { defineStore } from 'pinia'
import { authService } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  actions: {
    async register(username, email, password) {
      try {
        const data = await authService.register(username, email, password)
        this.token = data.access_token
        this.user = data.user
        this.isAuthenticated = true
        localStorage.setItem('token', data.access_token)
        return { success: true, data }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Registration failed' 
        }
      }
    },

    async login(username, password) {
      try {
        const data = await authService.login(username, password)
        this.token = data.access_token
        this.user = data.user
        this.isAuthenticated = true
        localStorage.setItem('token', data.access_token)
        return { success: true, data }
      } catch (error) {
        return { 
          success: false, 
          error: error.response?.data?.error || 'Login failed' 
        }
      }
    },

    async fetchUser() {
      try {
        const data = await authService.getCurrentUser()
        this.user = data.user
        return { success: true, data }
      } catch (error) {
        this.logout()
        return { success: false, error: 'Failed to fetch user' }
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    }
  }
})
