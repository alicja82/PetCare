import { defineStore } from 'pinia'
import api from '../services/api'

export const useVisitStore = defineStore('visit', {
  state: () => ({
    visits: [],
    currentVisit: null,
    loading: false,
    error: null
  }),

  getters: {
    getVisitsByPetId: (state) => (petId) => {
      return state.visits.filter(visit => visit.pet_id === petId)
    },
    hasVisits: (state) => state.visits.length > 0,
    sortedVisits: (state) => {
      return [...state.visits].sort((a, b) => new Date(b.visit_date) - new Date(a.visit_date))
    }
  },

  actions: {
    async fetchVisitsByPet(petId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/pets/${petId}/visits`)
        this.visits = response.data.visits
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch visits'
        console.error('Error fetching visits:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchVisit(visitId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/visits/${visitId}`)
        this.currentVisit = response.data.visit
        return response.data.visit
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch visit'
        console.error('Error fetching visit:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createVisit(petId, visitData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post(`/pets/${petId}/visits`, visitData)
        this.visits.push(response.data.visit)
        return response.data.visit
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to create visit'
        console.error('Error creating visit:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateVisit(visitId, visitData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.put(`/visits/${visitId}`, visitData)
        const index = this.visits.findIndex(v => v.id === visitId)
        if (index !== -1) {
          this.visits[index] = response.data.visit
        }
        if (this.currentVisit?.id === visitId) {
          this.currentVisit = response.data.visit
        }
        return response.data.visit
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update visit'
        console.error('Error updating visit:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteVisit(visitId) {
      this.loading = true
      this.error = null
      try {
        await api.delete(`/visits/${visitId}`)
        this.visits = this.visits.filter(v => v.id !== visitId)
        if (this.currentVisit?.id === visitId) {
          this.currentVisit = null
        }
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to delete visit'
        console.error('Error deleting visit:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})
