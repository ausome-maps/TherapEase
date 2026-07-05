import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppCardList from '../../components/Search/AppCardList.vue'

// Mock NuxtLink for standalone vitest
const NuxtLinkStub = {
  name: 'NuxtLink',
  props: ['to'],
  template: '<a :href="to"><slot /></a>',
}

const stubFacility = (overrides = {}) => ({
  id: 'test-id-123',
  properties: {
    placename: 'Test Facility',
    address: '123 Test St',
    region: 'NCR',
    city: 'Manila',
    services_offered: {
      speechlanguagetherapy: {
        label: 'Speech-Language Therapy',
        mode: { teletherapy: 0, onsite: 1, home_service: 0 },
      },
    },
    accreditation: { paot: 0, pasp: 0 },
    images: [],
    ...overrides,
  },
  geometry: { type: 'Point', coordinates: [121.0, 14.5] },
})

describe('AppCardList', () => {
  it('renders empty state when no facilities are provided', () => {
    const wrapper = mount(AppCardList, {
      props: { facilities: [], loading: false, error: false },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    expect(wrapper.text()).toContain('No facilities found')
  })

  it('renders empty state when facilities is undefined', () => {
    const wrapper = mount(AppCardList, {
      props: { loading: false, error: false },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    expect(wrapper.text()).toContain('No facilities found')
  })

  it('renders cards for each facility in the array', () => {
    const facilities = [
      stubFacility({ placename: 'Center A' }),
      stubFacility({ placename: 'Center B' }),
      stubFacility({ placename: 'Center C' }),
    ]
    const wrapper = mount(AppCardList, {
      props: { facilities, loading: false, error: false },
      global: {
        stubs: {
          AppCard: {
            name: 'AppCard',
            props: { facilityData: Object },
            emits: ['facility-hovered', 'facility-unhovered'],
            template: '<div class="mock-card">{{ facilityData.properties.placename }}</div>',
          },
          NuxtLink: NuxtLinkStub,
        },
      },
    })
    const cards = wrapper.findAll('.mock-card')
    expect(cards).toHaveLength(3)
    expect(cards[0].text()).toBe('Center A')
    expect(cards[1].text()).toBe('Center B')
    expect(cards[2].text()).toBe('Center C')
  })

  it('renders loading skeletons when loading prop is true', () => {
    const wrapper = mount(AppCardList, {
      props: { facilities: [], loading: true, error: false },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    // Should show animate-pulse elements (skeletons)
    const skeletons = wrapper.findAll('.animate-pulse')
    expect(skeletons.length).toBeGreaterThan(0)
  })

  it('renders error state with retry button when error prop is true', () => {
    const wrapper = mount(AppCardList, {
      props: { facilities: [], loading: false, error: true },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    expect(wrapper.text()).toContain('Failed to load facilities')
    const retryBtn = wrapper.find('button')
    expect(retryBtn.exists()).toBe(true)
    expect(retryBtn.text()).toBe('Retry')
  })

  it('emits retry event when retry button is clicked', async () => {
    const wrapper = mount(AppCardList, {
      props: { facilities: [], loading: false, error: true },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('retry')).toBeTruthy()
    expect(wrapper.emitted('retry')).toHaveLength(1)
  })

  it('does not emit events when loading', () => {
    const wrapper = mount(AppCardList, {
      props: { facilities: [], loading: true, error: false },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    expect(wrapper.emitted('retry')).toBeFalsy()
    expect(wrapper.emitted('facility-hovered')).toBeFalsy()
  })

  it('renders suggestion text in empty state', () => {
    const wrapper = mount(AppCardList, {
      props: { facilities: [], loading: false, error: false },
      global: { stubs: { AppCard: true, NuxtLink: NuxtLinkStub } },
    })
    expect(wrapper.text()).toContain('Try adjusting your search')
  })
})
