/**
 * Integration tests for Schedules view component
 * Testing schedule list rendering
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Schedules from '../../src/views/Schedules.vue'

describe('Schedules.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders schedules view title', () => {
    const wrapper = mount(Schedules)
    
    expect(wrapper.text()).toContain('Harmonogram karmienia')
  })
})
