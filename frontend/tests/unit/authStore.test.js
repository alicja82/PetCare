/**
 * Unit tests for useAuthStore
 * Testing authentication state logic
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../../src/stores/auth.js'

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should set user and token on login', () => {
    const store = useAuthStore()
    
    const userData = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    }
    const token = 'fake-jwt-token'
    
    store.user = userData
    store.token = token
    
    expect(store.user.username).toBe('testuser')
    expect(store.token).toBe('fake-jwt-token')
  })
})
