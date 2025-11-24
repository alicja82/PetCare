/**
 * Integration tests for Pets management
 * Testing multiple pet operations in store
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePetStore } from '../../src/stores/pet.js'

describe('Pets Integration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should manage multiple pets in store', () => {
    const store = usePetStore()
    
    // Dodaj pierwszego zwierzaka
    const pet1 = {
      id: 1,
      name: 'Max',
      species: 'Dog',
      age: 3,
      weight: 25.5
    }
    
    const pet2 = {
      id: 2,
      name: 'Luna',
      species: 'Cat',
      age: 2,
      weight: 4.5
    }
    
    store.pets = [pet1, pet2]
    
    // Sprawdź czy są 2 zwierzaki
    expect(store.pets).toHaveLength(2)
    expect(store.pets[0].name).toBe('Max')
    expect(store.pets[1].name).toBe('Luna')
    
    // Usuń jednego zwierzaka (symulacja usunięcia)
    store.pets = store.pets.filter(pet => pet.id !== 1)
    
    expect(store.pets).toHaveLength(1)
    expect(store.pets[0].name).toBe('Luna')
  })
})
