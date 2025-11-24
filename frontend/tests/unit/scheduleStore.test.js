/**
 * Unit tests for useScheduleStore
 * Testing schedule management state logic
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useScheduleStore } from '../../src/stores/schedule.js'

describe('useScheduleStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should add schedule to store', () => {
    const store = useScheduleStore()
    
    const newSchedule = {
      id: 1,
      food_type: 'Dry dog food',
      amount: '200g',
      time: '08:00',
      frequency: 'Daily'
    }
    
    store.schedules = []
    store.schedules.push(newSchedule)
    
    expect(store.schedules).toHaveLength(1)
    expect(store.schedules[0].food_type).toBe('Dry dog food')
    expect(store.schedules[0].time).toBe('08:00')
  })
})
