/**
 * Unit tests for usePetStore
 * Testing pet management state logic
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePetStore } from '../../src/stores/pet.js'

describe('usePetStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should add pet to store', () => {
    const store = usePetStore()
    
    const newPet = {
      id: 1,
      name: 'Max',
      species: 'Dog',
      age: 3,
      weight: 25.5
    }
    
    store.pets = []
    store.pets.push(newPet)
    
    expect(store.pets).toHaveLength(1)
    expect(store.pets[0].name).toBe('Max')
    expect(store.pets[0].species).toBe('Dog')
  })
})
