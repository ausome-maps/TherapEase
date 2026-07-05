import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppCard from '../../components/Search/AppCard.vue'

// Mock NuxtLink for standalone vitest (Nuxt auto-imports not available)
const NuxtLinkStub = {
  name: 'NuxtLink',
  props: ['to'],
  template: '<a :href="to"><slot /></a>',
}

// Stub AppAccBadge (also Nuxt auto-imported)
const AppAccBadgeStub = {
  name: 'AppAccBadge',
  props: ['accreditation'],
  template: '<div class="accreditation-badge">{{ accreditation.paot }}-{{ accreditation.pasp }}</div>',
}

const stubFacility = (overrides = {}) => ({
  id: 'test-id-123',
  properties: {
    placename: 'Test Therapy Center',
    address: '123 Test Street, Manila',
    region: 'NCR',
    city: 'Manila',
    services_offered: {
      occupationaltherapy: {
        label: 'Occupational Therapy',
        mode: { teletherapy: 0, onsite: 1, home_service: 0 },
      },
      speechlanguagetherapy: {
        label: 'Speech-Language Therapy',
        mode: { teletherapy: 2, onsite: 0, home_service: 0 },
      },
    },
    accreditation: { paot: 1, pasp: 0 },
    images: [],
    ...overrides,
  },
  geometry: { type: 'Point', coordinates: [121.0, 14.5] },
})

describe('AppCard', () => {
  const mountOptions = {
    global: {
      stubs: {
        NuxtLink: NuxtLinkStub,
        AppAccBadge: AppAccBadgeStub,
      },
    },
  }

  it('renders facility placename', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    expect(wrapper.text()).toContain('Test Therapy Center')
  })

  it('renders facility address when available', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    expect(wrapper.text()).toContain('123 Test Street, Manila')
  })

  it('renders without address when not provided', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility({ address: '' }) },
      ...mountOptions,
    })
    const lines = wrapper.text()
    // Should not display empty address
    expect(lines).not.toContain('123 Test Street')
  })

  it('shows active service count', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    // 2 active services (occupationaltherapy onsite=1, speechlanguagetherapy teletherapy=2)
    expect(wrapper.text()).toContain('2 interventions on offer')
  })

  it('shows singular intervention text when only one active', () => {
    const facility = stubFacility({
      services_offered: {
        occupationaltherapy: {
          label: 'Occupational Therapy',
          mode: { teletherapy: 0, onsite: 1, home_service: 0 },
        },
      },
    })
    const wrapper = mount(AppCard, {
      props: { facilityData: facility },
      ...mountOptions,
    })
    expect(wrapper.text()).toContain('1 intervention on offer')
  })

  it('does not show intervention count when none are active', () => {
    const facility = stubFacility({
      services_offered: {
        occupationaltherapy: {
          label: 'Occupational Therapy',
          mode: { teletherapy: 0, onsite: 0, home_service: 0 },
        },
      },
    })
    const wrapper = mount(AppCard, {
      props: { facilityData: facility },
      ...mountOptions,
    })
    expect(wrapper.text()).not.toContain('intervention')
  })

  it('shows accreditation badge when accredited', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility({ accreditation: { paot: 1, pasp: 0 } }) },
      ...mountOptions,
    })
    expect(wrapper.find('.accreditation-badge').exists()).toBe(true)
  })

  it('does not show accreditation badge when not accredited', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility({ accreditation: { paot: 0, pasp: 0 } }) },
      ...mountOptions,
    })
    expect(wrapper.find('.accreditation-badge').exists()).toBe(false)
  })

  it('emits facility-hovered on mouseenter', async () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    await wrapper.find('article').trigger('mouseenter')
    expect(wrapper.emitted('facility-hovered')).toBeTruthy()
    expect(wrapper.emitted('facility-hovered')![0]).toEqual(['test-id-123'])
  })

  it('emits facility-unhovered on mouseleave', async () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    await wrapper.find('article').trigger('mouseleave')
    expect(wrapper.emitted('facility-unhovered')).toBeTruthy()
    expect(wrapper.emitted('facility-unhovered')![0]).toEqual(['test-id-123'])
  })

  it('contains link to detail page with correct id', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    const links = wrapper.findAll('a')
    const detailLink = links.find((link) =>
      link.attributes('href')?.includes('details-page')
    )
    expect(detailLink).toBeTruthy()
    expect(detailLink!.attributes('href')).toContain('id=test-id-123')
  })

  it('has accessible role on article', () => {
    const wrapper = mount(AppCard, {
      props: { facilityData: stubFacility() },
      ...mountOptions,
    })
    const article = wrapper.find('article')
    expect(article.attributes('role')).toBe('article')
    expect(article.attributes('aria-label')).toBe('Test Therapy Center')
  })
})
