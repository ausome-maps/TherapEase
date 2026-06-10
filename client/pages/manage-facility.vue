<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">{{ isEditing ? 'Edit Facility' : 'Add New Facility' }}</h1>
          <p class="text-gray-600 mt-1">{{ isEditing ? 'Update facility information' : 'Register a new facility in the database' }}</p>
        </div>
        <NuxtLink to="/" class="text-sm text-gray-500 hover:text-gray-700">
          &larr; Back to search
        </NuxtLink>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6">
        {{ success }}
      </div>

      <div v-if="!isAuthenticated" class="text-center py-10">
        <p class="text-gray-600 mb-4">Please sign in to manage facilities.</p>
        <NuxtLink to="/login" class="px-6 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500">Sign In</NuxtLink>
      </div>

      <form v-else @submit.prevent="handleSubmit" class="space-y-8">
        <div class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">Basic Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Facility Name *</label>
              <input v-model="form.placename" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">City</label>
              <input v-model="form.city" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Region</label>
              <input v-model="form.region" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <input v-model="form.address" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Landmarks / Directions</label>
              <textarea v-model="form.landmarks_desc" rows="2" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg"></textarea>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">Contact Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Contact Number</label>
              <input v-model="form.contact_number" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Alternate Contact</label>
              <input v-model="form.alt_contact_number" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email Address</label>
              <input v-model="form.email_address" type="email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Website</label>
              <input v-model="form.website" type="url" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">Accreditation</h2>
          <div class="flex gap-6">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" :checked="form.accreditation.paot === 1" @change="form.accreditation.paot = form.accreditation.paot === 1 ? 0 : 1" class="rounded" />
              <span>PAOT Accredited</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" :checked="form.accreditation.pasp === 1" @change="form.accreditation.pasp = form.accreditation.pasp === 1 ? 0 : 1" class="rounded" />
              <span>PASP Accredited</span>
            </label>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">Services Offered</h2>
          <p class="text-sm text-gray-500">Check services and set mode values (1=Individual, 2=Group, 3=Both)</p>
          <div class="space-y-3 max-h-96 overflow-y-auto">
            <div v-for="(service, key) in form.services_offered" :key="key" class="flex items-center gap-4 border-b pb-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" :checked="serviceActive(key)" class="rounded" />
                <span class="text-sm w-48">{{ form.services_offered[key].label }}</span>
              </label>
              <div class="flex gap-2">
                <label class="text-xs">
                  <span class="text-gray-500">Teletherapy:</span>
                  <select v-model.number="form.services_offered[key].mode.teletherapy" class="ml-1 border rounded text-xs px-1 py-0.5">
                    <option :value="0">Off</option>
                    <option :value="1">1:1</option>
                    <option :value="2">Group</option>
                    <option :value="3">Both</option>
                  </select>
                </label>
                <label class="text-xs">
                  <span class="text-gray-500">Onsite:</span>
                  <select v-model.number="form.services_offered[key].mode.onsite" class="ml-1 border rounded text-xs px-1 py-0.5">
                    <option :value="0">Off</option>
                    <option :value="1">1:1</option>
                    <option :value="2">Group</option>
                    <option :value="3">Both</option>
                  </select>
                </label>
                <label class="text-xs">
                  <span class="text-gray-500">Home:</span>
                  <select v-model.number="form.services_offered[key].mode.home_service" class="ml-1 border rounded text-xs px-1 py-0.5">
                    <option :value="0">Off</option>
                    <option :value="1">1:1</option>
                    <option :value="2">Group</option>
                    <option :value="3">Both</option>
                  </select>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-lg font-semibold text-gray-900">Location</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Latitude</label>
              <input v-model.number="form.geometry.coordinates[1]" type="number" step="any" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Longitude</label>
              <input v-model.number="form.geometry.coordinates[0]" type="number" step="any" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg" />
            </div>
          </div>
        </div>

        <div class="flex gap-4">
          <button type="submit" :disabled="loading"
            class="px-6 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 disabled:opacity-50">
            {{ loading ? 'Saving...' : (isEditing ? 'Update Facility' : 'Create Facility') }}
          </button>
          <NuxtLink to="/" class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">Cancel</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()

const isEditing = computed(() => !!route.query.id)
const isAuthenticated = computed(() => {
  if (import.meta.server) return false
  return !!localStorage.getItem('access_token')
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const defaultServices = {
  speechlanguagetherapy: { label: "Speech-Language Therapy", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  speechlanguagepathology: { label: "Speech-Language Pathology", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  occupationaltherapy: { label: "Occupational Therapy", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  behavioraltherapy: { label: "Behavioral Therapy", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  physicaltherapy: { label: "Physical Therapy", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  lifeskillstraining: { label: "Life Skills Training", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  socialskillstraining: { label: "Social Skills Training", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  integration: { label: "Integration", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  integrationprogram: { label: "Integration Program", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  jobcoaching: { label: "Job Coaching", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  specialeducation: { label: "Special Education", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  spedtutorials: { label: "SpEd Tutorials", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  parentcoaching: { label: "Parent Coaching", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  educationsessionforfamilies: { label: "Education Session for Families", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  feeding: { label: "Feeding", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  counseling: { label: "Counseling", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  psychotherapy: { label: "Psychotherapy", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  abatherapy: { label: "ABA Therapy", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  mnri: { label: "MNRI", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  sensoryintegration: { label: "Sensory Integration", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  playschool: { label: "Play School", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  dysphagiamanagement: { label: "Dysphagia Management", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  orthoses: { label: "Orthoses (Splinting)", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  homeschoolfacilitation: { label: "Homeschool Facilitation", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
  rehabconsultation: { label: "Rehab Consultation", mode: { teletherapy: 0, onsite: 0, home_service: 0 } },
}

const form = reactive({
  placename: '',
  address: '',
  region: '',
  city: '',
  landmarks_desc: '',
  contact_number: '',
  alt_contact_number: '',
  email_address: '',
  website: '',
  accreditation: { paot: 0, pasp: 0 },
  services_offered: JSON.parse(JSON.stringify(defaultServices)),
  geometry: {
    type: 'Point',
    coordinates: [121.0, 14.5],
  },
})

const getHeaders = () => {
  const token = localStorage.getItem('access_token')
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  }
}

const serviceActive = (key) => {
  const s = form.services_offered[key]
  return s.mode.teletherapy > 0 || s.mode.onsite > 0 || s.mode.home_service > 0
}

onMounted(async () => {
  if (route.query.id) {
    try {
      const res = await fetch(`${config.public.apiURL}/facilities/${route.query.id}`, {
        headers: getHeaders(),
      })
      if (res.ok) {
        const data = await res.json()
        const facility = data.data || data
        form.placename = facility.properties?.placename || ''
        form.address = facility.properties?.address || ''
        form.region = facility.properties?.region || ''
        form.city = facility.properties?.city || ''
        form.landmarks_desc = facility.properties?.landmarks_desc || ''
        form.contact_number = facility.properties?.contact_number || ''
        form.alt_contact_number = facility.properties?.alt_contact_number || ''
        form.email_address = facility.properties?.email_address || ''
        form.website = facility.properties?.website || ''
        form.accreditation = facility.properties?.accreditation || { paot: 0, pasp: 0 }
        if (facility.properties?.services_offered) {
          form.services_offered = { ...JSON.parse(JSON.stringify(defaultServices)), ...facility.properties.services_offered }
        }
        if (facility.geometry?.coordinates) {
          form.geometry.coordinates = facility.geometry.coordinates
        }
      }
    } catch {}
  }
})

const handleSubmit = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  const payload = {
    properties: {
      placename: form.placename,
      address: form.address,
      region: form.region,
      city: form.city,
      landmarks_desc: form.landmarks_desc,
      contact_number: form.contact_number,
      alt_contact_number: form.alt_contact_number,
      email_address: form.email_address,
      website: form.website,
      accreditation: form.accreditation,
      services_offered: form.services_offered,
    },
    geometry: form.geometry,
  }

  try {
    const url = isEditing.value
      ? `${config.public.apiURL}/facilities/${route.query.id}`
      : `${config.public.apiURL}/facilities/`
    const method = isEditing.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method,
      headers: getHeaders(),
      body: JSON.stringify(payload),
    })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Failed to save facility')
    }

    success.value = isEditing.value ? 'Facility updated!' : 'Facility created!'
    setTimeout(() => router.push('/'), 1500)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
