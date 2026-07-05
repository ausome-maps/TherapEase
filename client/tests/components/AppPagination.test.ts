import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppPagination from '../../components/Search/AppPagination.vue'

describe('AppPagination', () => {
  it('does not render when totalPages is 1', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 1, currentPage: 1 },
    })
    expect(wrapper.find('button').exists()).toBe(false)
  })

  it('does not render when totalPages is 0', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 0, currentPage: 1 },
    })
    expect(wrapper.find('button').exists()).toBe(false)
  })

  it('renders Previous and Next buttons when totalPages > 1', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 3 },
    })
    const buttons = wrapper.findAll('button')
    expect(buttons).toHaveLength(2)
    expect(buttons[0].text()).toBe('Previous')
    expect(buttons[1].text()).toBe('Next')
  })

  it('displays current page and total pages', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 10, currentPage: 4 },
    })
    expect(wrapper.text()).toContain('4 / 10')
  })

  it('disables Previous button on first page', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 1 },
    })
    const prevBtn = wrapper.findAll('button')[0]
    expect(prevBtn.attributes('disabled')).toBeDefined()
  })

  it('disables Next button on last page', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 5 },
    })
    const nextBtn = wrapper.findAll('button')[1]
    expect(nextBtn.attributes('disabled')).toBeDefined()
  })

  it('enables both buttons on middle pages', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 3 },
    })
    const buttons = wrapper.findAll('button')
    expect(buttons[0].attributes('disabled')).toBeUndefined()
    expect(buttons[1].attributes('disabled')).toBeUndefined()
  })

  it('emits change-page with next page when Next clicked', async () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 3 },
    })
    await wrapper.findAll('button')[1].trigger('click')
    expect(wrapper.emitted('change-page')).toBeTruthy()
    expect(wrapper.emitted('change-page')![0]).toEqual([4])
  })

  it('emits change-page with previous page when Previous clicked', async () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 3 },
    })
    await wrapper.findAll('button')[0].trigger('click')
    expect(wrapper.emitted('change-page')).toBeTruthy()
    expect(wrapper.emitted('change-page')![0]).toEqual([2])
  })

  it('does not emit when Next is disabled and clicked', async () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 5 },
    })
    await wrapper.findAll('button')[1].trigger('click')
    expect(wrapper.emitted('change-page')).toBeFalsy()
  })

  it('does not emit when Previous is disabled and clicked', async () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 5, currentPage: 1 },
    })
    await wrapper.findAll('button')[0].trigger('click')
    expect(wrapper.emitted('change-page')).toBeFalsy()
  })

  it('has disabled cursor styling on disabled buttons', () => {
    const wrapper = mount(AppPagination, {
      props: { totalPages: 3, currentPage: 1 },
    })
    const prevBtn = wrapper.findAll('button')[0]
    expect(prevBtn.classes()).toContain('disabled:cursor-not-allowed')
  })
})
