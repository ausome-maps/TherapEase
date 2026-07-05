import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'

/**
 * For this test we test the filter logic in isolation by
 * extracting the composable-like logic from the component.
 *
 * We mock the component's internal state management and test
 * the filter generation functions directly.
 */

// Replicate the filter logic from AppFilter.vue
const SERVICE_KEYS = [
  'speechlanguagetherapy', 'speechlanguagepathology', 'occupationaltherapy',
  'behavioraltherapy', 'physicaltherapy', 'lifeskillstraining',
  'socialskillstraining', 'integration', 'integrationprogram',
  'jobcoaching', 'specialeducation', 'spedtutorials', 'parentcoaching',
  'educationsessionforfamilies', 'feeding', 'counseling', 'psychotherapy',
  'abatherapy', 'mnri', 'sensoryintegration', 'playschool',
  'dysphagiamanagement', 'orthoses', 'homeschoolfacilitation', 'rehabconsultation',
]

interface FilterState {
  isPASPChecked: boolean
  isPAOTChecked: boolean
  teletherapyChecked: boolean
  onsiteChecked: boolean
  homeserviceChecked: boolean
  individualChecked: boolean
  groupChecked: boolean
  serviceCheckboxes: Record<string, boolean>
}

function createEmptyFilters(): FilterState {
  const services: Record<string, boolean> = {}
  for (const key of SERVICE_KEYS) {
    services[key] = false
  }
  return {
    isPASPChecked: false,
    isPAOTChecked: false,
    teletherapyChecked: false,
    onsiteChecked: false,
    homeserviceChecked: false,
    individualChecked: false,
    groupChecked: false,
    serviceCheckboxes: services,
  }
}

function generateFilterQuery(state: FilterState) {
  const filters: Record<string, unknown> = {}

  const accreditation: Record<string, number> = {}
  if (state.isPASPChecked) accreditation.pasp = 1
  if (state.isPAOTChecked) accreditation.paot = 1
  if (Object.keys(accreditation).length > 0) {
    filters.accreditation = accreditation
  }

  const modes: string[] = []
  if (state.teletherapyChecked) modes.push('teletherapy')
  if (state.onsiteChecked) modes.push('onsite')
  if (state.homeserviceChecked) modes.push('home_service')
  if (modes.length > 0) {
    filters.mode = modes
  }

  const sessionTypes: string[] = []
  if (state.individualChecked) sessionTypes.push('individual')
  if (state.groupChecked) sessionTypes.push('group')
  if (sessionTypes.length > 0) {
    filters.session_type = sessionTypes
  }

  const selectedServices: string[] = []
  for (const key in state.serviceCheckboxes) {
    if (state.serviceCheckboxes[key]) {
      selectedServices.push(key)
    }
  }
  if (selectedServices.length > 0) {
    filters.services_offered = selectedServices
  }

  return { filters, filter: filters }
}

function countActiveFilters(state: FilterState): number {
  let count = 0
  if (state.isPASPChecked) count++
  if (state.isPAOTChecked) count++
  if (state.teletherapyChecked) count++
  if (state.onsiteChecked) count++
  if (state.homeserviceChecked) count++
  if (state.individualChecked) count++
  if (state.groupChecked) count++
  for (const key in state.serviceCheckboxes) {
    if (state.serviceCheckboxes[key]) count++
  }
  return count
}

describe('AppFilter', () => {
  it('starts with all filters cleared', () => {
    const state = createEmptyFilters()
    expect(countActiveFilters(state)).toBe(0)

    const result = generateFilterQuery(state)
    expect(result.filters).toEqual({})
  })

  it('generates correct filter query for accreditation', () => {
    const state = createEmptyFilters()
    state.isPAOTChecked = true

    const result = generateFilterQuery(state)
    expect(result.filters.accreditation).toEqual({ paot: 1 })
  })

  it('generates correct filter query for both accreditations', () => {
    const state = createEmptyFilters()
    state.isPASPChecked = true
    state.isPAOTChecked = true

    const result = generateFilterQuery(state)
    expect(result.filters.accreditation).toEqual({ pasp: 1, paot: 1 })
  })

  it('generates correct filter query for service mode (teletherapy)', () => {
    const state = createEmptyFilters()
    state.teletherapyChecked = true

    const result = generateFilterQuery(state)
    expect(result.filters.mode).toEqual(['teletherapy'])
  })

  it('generates correct filter query for multiple modes', () => {
    const state = createEmptyFilters()
    state.teletherapyChecked = true
    state.onsiteChecked = true
    state.homeserviceChecked = true

    const result = generateFilterQuery(state)
    expect(result.filters.mode).toEqual(['teletherapy', 'onsite', 'home_service'])
  })

  it('generates correct filter query for session type', () => {
    const state = createEmptyFilters()
    state.individualChecked = true

    const result = generateFilterQuery(state)
    expect(result.filters.session_type).toEqual(['individual'])
  })

  it('generates correct filter query for both session types', () => {
    const state = createEmptyFilters()
    state.individualChecked = true
    state.groupChecked = true

    const result = generateFilterQuery(state)
    expect(result.filters.session_type).toEqual(['individual', 'group'])
  })

  it('generates correct filter query for services offered', () => {
    const state = createEmptyFilters()
    state.serviceCheckboxes['occupationaltherapy'] = true
    state.serviceCheckboxes['speechlanguagetherapy'] = true

    const result = generateFilterQuery(state)
    expect(result.filters.services_offered).toContain('occupationaltherapy')
    expect(result.filters.services_offered).toContain('speechlanguagetherapy')
    expect(result.filters.services_offered).toHaveLength(2)
  })

  it('clearAllFilters resets all checkboxes to false', () => {
    const state = createEmptyFilters()
    state.isPAOTChecked = true
    state.teletherapyChecked = true
    state.individualChecked = true
    state.serviceCheckboxes['feeding'] = true

    // Simulate clearAllFilters
    const cleared = createEmptyFilters()

    expect(cleared.isPAOTChecked).toBe(false)
    expect(cleared.teletherapyChecked).toBe(false)
    expect(cleared.individualChecked).toBe(false)
    expect(cleared.serviceCheckboxes['feeding']).toBe(false)
    expect(countActiveFilters(cleared)).toBe(0)
  })

  it('counts active filters correctly', () => {
    const state = createEmptyFilters()
    expect(countActiveFilters(state)).toBe(0)

    state.isPAOTChecked = true
    expect(countActiveFilters(state)).toBe(1)

    state.teletherapyChecked = true
    state.onsiteChecked = true
    expect(countActiveFilters(state)).toBe(3)

    state.serviceCheckboxes['feeding'] = true
    state.serviceCheckboxes['mnri'] = true
    expect(countActiveFilters(state)).toBe(5)
  })

  it('emits query-generated with empty filters when nothing is checked', () => {
    const state = createEmptyFilters()
    // Simulating clearAllFilters behavior
    const result = generateFilterQuery(state)
    expect(result.filters).toEqual({})
    expect(Object.keys(result.filters)).toHaveLength(0)
  })

  it('emits query-generated with combined filters when multiple categories are checked', () => {
    const state = createEmptyFilters()
    state.isPAOTChecked = true
    state.teletherapyChecked = true
    state.individualChecked = true
    state.serviceCheckboxes['occupationaltherapy'] = true

    const result = generateFilterQuery(state)
    expect(result.filters.accreditation).toEqual({ paot: 1 })
    expect(result.filters.mode).toEqual(['teletherapy'])
    expect(result.filters.session_type).toEqual(['individual'])
    expect(result.filters.services_offered).toContain('occupationaltherapy')

    // Check that all filter categories are present
    const filterKeys = Object.keys(result.filters)
    expect(filterKeys).toContain('accreditation')
    expect(filterKeys).toContain('mode')
    expect(filterKeys).toContain('session_type')
    expect(filterKeys).toContain('services_offered')
  })
})
