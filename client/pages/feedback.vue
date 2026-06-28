<template>
  <div class="min-h-screen bg-gray-50 flex items-start justify-center px-4 py-12">
    <div class="w-full max-w-2xl">
      <NuxtLink to="/" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-6">
        <svg class="w-5 h-5 mr-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 8 14">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 1 1.3 6.326a.91.91 0 0 0 0 1.348L7 13" />
        </svg>
        Go back to search
      </NuxtLink>

      <div v-if="loadingFacility" class="text-center py-8">
        <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
        <p class="mt-4 text-gray-600">Loading facility details...</p>
      </div>

      <div v-else-if="facilityError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
        {{ facilityError }}
      </div>

      <template v-else>
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h1 class="text-2xl font-bold text-gray-900 mb-2">Submit Feedback</h1>
          <p v-if="facilityName" class="text-sm text-gray-600">
            You are submitting feedback about <strong class="text-gray-800">{{ facilityName }}</strong>
          </p>
          <p class="text-sm text-gray-500 mt-1">
            Help us improve the platform by sharing your concerns and suggestions.
          </p>
        </div>

        <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm mb-6">
          {{ success }}
          <NuxtLink v-if="facilityId" :to="`/details-page?id=${facilityId}`" class="ml-2 underline font-medium">
            View facility details
          </NuxtLink>
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-6">
          {{ error }}
        </div>

        <form v-if="!success" @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-5">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address <span class="text-red-400">*</span></label>
            <input
              id="email"
              v-model.trim="form.email_address"
              type="email"
              required
              placeholder="your@email.com"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
            >
          </div>

          <div>
            <label for="contact" class="block text-sm font-medium text-gray-700">Contact Number <span class="text-red-400">*</span></label>
            <input
              id="contact"
              v-model.trim="form.contact_number"
              type="text"
              required
              placeholder="+639123456789"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
            >
          </div>

          <div>
            <label for="dataConcerns" class="block text-sm font-medium text-gray-700">
              Concerns/Suggestions regarding the data available in the platform <span class="text-red-400">*</span>
            </label>
            <textarea
              id="dataConcerns"
              v-model="form.data_concerns"
              required
              rows="4"
              placeholder="Describe any issues with the correctness of data, missing information, or suggestions about data on this therapy center..."
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
            ></textarea>
          </div>

          <div>
            <label for="usabilityConcerns" class="block text-sm font-medium text-gray-700">
              Concerns/Suggestions regarding the features and overall usability of the platform <span class="text-red-400">*</span>
            </label>
            <textarea
              id="usabilityConcerns"
              v-model="form.usability_concerns"
              required
              rows="4"
              placeholder="Describe any issues with the interface, features you'd like to see, or other suggestions..."
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
            ></textarea>
          </div>

          <button
            type="submit"
            :disabled="submitting"
            class="w-full py-3 px-4 bg-red-400 text-white rounded-lg hover:bg-red-500 disabled:opacity-50 text-sm font-medium transition-colors duration-300"
          >
            <span v-if="submitting">
              <span class="inline-block animate-spin">&#9696;</span> Submitting...
            </span>
            <span v-else>Submit Feedback</span>
          </button>
        </form>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

const route = useRoute()
const config = useRuntimeConfig()

const facilityId = ref(route.query.facility_id as string || '')
const facilityName = ref('')
const loadingFacility = ref(false)
const facilityError = ref('')
const submitting = ref(false)
const error = ref('')
const success = ref('')

const form = reactive({
  email_address: '',
  contact_number: '',
  data_concerns: '',
  usability_concerns: '',
})

onMounted(async () => {
  if (!facilityId.value) {
    facilityError.value = 'No therapy center specified. Please navigate from a facility details page to submit feedback.'
    return
  }
  loadingFacility.value = true
  try {
    const res = await fetch(`${config.public.apiURL}/facilities/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ q: `id:${facilityId.value}`, from: 0, size: 1 }),
    })
    if (!res.ok) throw new Error('Failed to fetch facility details')
    const data = await res.json()
    if (data.features && data.features.length > 0) {
      facilityName.value = data.features[0].properties.placename || 'Unknown Facility'
    } else {
      facilityError.value = 'Therapy center not found. Please navigate from a valid facility details page.'
    }
  } catch (e: any) {
    facilityError.value = e.message || 'Failed to load facility details'
  } finally {
    loadingFacility.value = false
  }
})

const handleSubmit = async () => {
  if (!facilityId.value) {
    error.value = 'Missing therapy center reference. Please navigate back to the facility and try again.'
    return
  }
  error.value = ''
  submitting.value = true
  try {
    const res = await fetch(`${config.public.apiURL}/feedback/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        facility: facilityId.value,
        email_address: form.email_address,
        contact_number: form.contact_number,
        data_concerns: form.data_concerns,
        usability_concerns: form.usability_concerns,
      }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Submission failed' }))
      const msg = typeof err === 'object' ? Object.values(err).flat().join(', ') : err
      throw new Error(msg || 'Submission failed')
    }
    success.value = 'Thank you! Your feedback has been submitted successfully.'
  } catch (e: any) {
    error.value = e.message || 'An error occurred while submitting your feedback. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>
