import { defineStore } from 'pinia'
import api from '../services/api'

export const useScheduleStore = defineStore('schedule', {
  state: () => ({
    schedules: [],
    currentSchedule: null,
    loading: false,
    error: null
  }),

  getters: {
    getSchedulesByPetId: (state) => (petId) => {
      return state.schedules.filter(schedule => schedule.pet_id === petId)
    },
    hasSchedules: (state) => state.schedules.length > 0
  },

  actions: {
    async fetchSchedulesByPet(petId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/pets/${petId}/schedule`)
        this.schedules = response.data.schedules
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch schedules'
        console.error('Error fetching schedules:', error)
      } finally {
        this.loading = false
      }
    },

    async createSchedule(petId, scheduleData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post(`/pets/${petId}/schedule`, scheduleData)
        this.schedules.push(response.data.schedule)
        return response.data.schedule
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to create schedule'
        console.error('Error creating schedule:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateSchedule(scheduleId, scheduleData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.put(`/schedule/${scheduleId}`, scheduleData)
        const index = this.schedules.findIndex(s => s.id === scheduleId)
        if (index !== -1) {
          this.schedules[index] = response.data.schedule
        }
        return response.data.schedule
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update schedule'
        console.error('Error updating schedule:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteSchedule(scheduleId) {
      this.loading = true
      this.error = null
      try {
        await api.delete(`/schedule/${scheduleId}`)
        this.schedules = this.schedules.filter(s => s.id !== scheduleId)
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to delete schedule'
        console.error('Error deleting schedule:', error)
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
