import { defineStore } from 'pinia'
import api from '../services/api'

export const usePetStore = defineStore('pet', {
  state: () => ({
    pets: [],
    currentPet: null,
    loading: false,
    error: null
  }),

  getters: {
    getPetById: (state) => (id) => {
      return state.pets.find(pet => pet.id === id)
    },
    hasPets: (state) => state.pets.length > 0
  },

  actions: {
    async fetchPets() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/pets')
        this.pets = response.data.pets
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch pets'
        console.error('Error fetching pets:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchPet(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/pets/${id}`)
        this.currentPet = response.data.pet
        return response.data.pet
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch pet'
        console.error('Error fetching pet:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createPet(petData) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        
        // Add pet data
        Object.keys(petData).forEach(key => {
          if (key === 'photo' && petData[key]) {
            formData.append('photo', petData[key])
          } else if (key === 'tags' && Array.isArray(petData[key])) {
            formData.append('tags', petData[key].join(','))
          } else if (petData[key] !== null && petData[key] !== undefined) {
            formData.append(key, petData[key])
          }
        })

        const response = await api.post('/pets', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        this.pets.push(response.data.pet)
        return response.data.pet
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to create pet'
        console.error('Error creating pet:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updatePet(id, petData) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        
        // Add pet data
        Object.keys(petData).forEach(key => {
          if (key === 'photo' && petData[key] instanceof File) {
            formData.append('photo', petData[key])
          } else if (key === 'tags' && Array.isArray(petData[key])) {
            formData.append('tags', petData[key].join(','))
          } else if (petData[key] !== null && petData[key] !== undefined && key !== 'photo') {
            formData.append(key, petData[key])
          }
        })

        const response = await api.put(`/pets/${id}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        const index = this.pets.findIndex(p => p.id === id)
        if (index !== -1) {
          this.pets[index] = response.data.pet
        }
        
        if (this.currentPet?.id === id) {
          this.currentPet = response.data.pet
        }
        
        return response.data.pet
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update pet'
        console.error('Error updating pet:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deletePet(id) {
      this.loading = true
      this.error = null
      try {
        await api.delete(`/pets/${id}`)
        this.pets = this.pets.filter(p => p.id !== id)
        if (this.currentPet?.id === id) {
          this.currentPet = null
        }
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to delete pet'
        console.error('Error deleting pet:', error)
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
