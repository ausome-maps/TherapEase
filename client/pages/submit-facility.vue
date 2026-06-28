<template>
  <div class="min-h-screen bg-gray-50 pb-24">
    <div class="max-w-4xl mx-auto px-4 py-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-xl font-bold text-gray-900">Submit a Facility</h1>
          <p class="text-gray-600 mt-0.5 text-sm">All submissions are reviewed before publication.</p>
        </div>
        <NuxtLink to="/" class="text-sm text-gray-500 hover:text-gray-700">&larr; Back to search</NuxtLink>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">{{ error }}</div>

      <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4 text-center text-sm">
        <p class="font-semibold text-lg">Thank you!</p>
        <p class="mt-1">{{ success }}</p>
        <NuxtLink to="/" class="inline-block mt-4 px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm">Return to map</NuxtLink>
      </div>

      <form v-if="!success" @submit.prevent="handleSubmit">
        <!-- Step indicator -->
        <nav aria-label="Progress" class="mb-8">
          <ol class="flex items-center">
            <li v-for="(step, i) in wizardSteps" :key="i" class="relative flex-1" :class="{ 'hidden sm:block': i > 0 && i < wizardSteps.length - 1 }">
              <div v-if="i > 0" class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="h-0.5 w-full" :class="currentStep > i ? 'bg-red-400' : 'bg-gray-200'" />
              </div>
              <button type="button" @click="goToStep(i + 1)" :disabled="i + 1 > maxVisitedStep"
                class="group relative flex items-center justify-center mx-auto w-8 h-8 rounded-full border-2 text-xs font-semibold transition-colors"
                :class="stepClass(i + 1)">
                <span v-if="i + 1 < currentStep" class="text-white">&#10003;</span>
                <span v-else>{{ i + 1 }}</span>
                <span class="absolute -bottom-5 text-[10px] whitespace-nowrap font-medium hidden sm:block"
                  :class="currentStep > i + 1 ? 'text-red-400' : currentStep === i + 1 ? 'text-gray-900' : 'text-gray-400'">
                  {{ step }}
                </span>
              </button>
            </li>
          </ol>
        </nav>

        <!-- Step 1: Basic Info -->
        <div v-show="currentStep === 1" class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-base font-semibold text-gray-900">Basic Information</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Facility Name <span class="text-red-400">*</span></label>
              <input v-model="form.payload.properties.placename" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">City</label>
              <input v-model="form.payload.properties.city" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Region</label>
              <input v-model="form.payload.properties.region" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <input v-model="form.payload.properties.address" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Landmarks / Directions</label>
              <textarea v-model="form.payload.properties.landmarks_desc" rows="2" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400"></textarea>
            </div>
          </div>
          <hr class="border-gray-200">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Source Name</label>
              <input v-model="form.payload.properties.info_src_name" type="text" placeholder="e.g. Juan Dela Cruz" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Source Designation</label>
              <input v-model="form.payload.properties.info_src_designation" type="text" placeholder="e.g. Owner" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
          </div>
        </div>

        <!-- Step 2: Contact + Social -->
        <div v-show="currentStep === 2" class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-base font-semibold text-gray-900">Contact Information</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Contact Number</label>
              <input v-model="form.payload.properties.contact_number" type="text" placeholder="+639123456789" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Alternate Contact</label>
              <input v-model="form.payload.properties.alt_contact_number" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email Address</label>
              <input v-model="form.payload.properties.email_address" type="email" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Website</label>
              <input v-model="form.payload.properties.website" type="url" placeholder="https://" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
          </div>
          <hr class="border-gray-200">
          <h3 class="text-sm font-semibold text-gray-700">Social Media</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Facebook</label>
              <input v-model="form.payload.properties.social_media.facebook" type="text" placeholder="facebook.com/..." class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Instagram</label>
              <input v-model="form.payload.properties.social_media.instagram" type="text" placeholder="@username" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
          </div>
        </div>

        <!-- Step 3: Services -->
        <div v-show="currentStep === 3" class="bg-white rounded-lg shadow-sm p-6 space-y-3">
          <h2 class="text-base font-semibold text-gray-900">Services Offered</h2>
          <p class="text-xs text-gray-500">Set the delivery mode for each service: 0=Off, 1=Individual, 2=Group, 3=Both</p>
          <div class="space-y-1 max-h-[60vh] overflow-y-auto">
            <div v-for="(service, key) in form.payload.properties.services_offered" :key="key" class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3 border-b border-gray-100 pb-1.5">
              <label class="flex items-center gap-2 cursor-pointer min-w-[180px] sm:min-w-[220px] shrink-0">
                <input type="checkbox" :checked="serviceActive(key)" class="rounded border-gray-300 text-red-400 focus:ring-red-400" />
                <span class="text-xs">{{ service.label }}</span>
              </label>
              <div class="flex gap-2 sm:gap-3 ml-6 sm:ml-0">
                <label class="text-xs flex items-center gap-1">
                  <span class="text-gray-400">Tel</span>
                  <select v-model.number="service.mode.teletherapy" class="border rounded text-xs px-1 py-0.5">
                    <option :value="0">0</option><option :value="1">1</option><option :value="2">2</option><option :value="3">3</option>
                  </select>
                </label>
                <label class="text-xs flex items-center gap-1">
                  <span class="text-gray-400">Site</span>
                  <select v-model.number="service.mode.onsite" class="border rounded text-xs px-1 py-0.5">
                    <option :value="0">0</option><option :value="1">1</option><option :value="2">2</option><option :value="3">3</option>
                  </select>
                </label>
                <label class="text-xs flex items-center gap-1">
                  <span class="text-gray-400">Home</span>
                  <select v-model.number="service.mode.home_service" class="border rounded text-xs px-1 py-0.5">
                    <option :value="0">0</option><option :value="1">1</option><option :value="2">2</option><option :value="3">3</option>
                  </select>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 4: Details (Caters To, Accreditation, Images) -->
        <div v-show="currentStep === 4" class="bg-white rounded-lg shadow-sm p-6 space-y-6">
          <div>
            <h2 class="text-base font-semibold text-gray-900">Caters To</h2>
            <div class="flex flex-wrap gap-x-6 gap-y-2 mt-2">
              <label v-for="opt in catersToOptions" :key="opt" class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" :value="opt" v-model="form.payload.properties.caters_to" class="rounded border-gray-300 text-red-400 focus:ring-red-400" />
                <span class="text-sm text-gray-700">{{ opt }}</span>
              </label>
            </div>
          </div>
          <hr class="border-gray-200">
          <div>
            <h2 class="text-base font-semibold text-gray-900">Accreditation</h2>
            <div class="flex gap-6 mt-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" :checked="form.payload.properties.accreditation.paot === 1" @change="form.payload.properties.accreditation.paot = form.payload.properties.accreditation.paot === 1 ? 0 : 1" class="rounded border-gray-300 text-red-400 focus:ring-red-400" />
                <span class="text-sm text-gray-700">PAOT Accredited</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" :checked="form.payload.properties.accreditation.pasp === 1" @change="form.payload.properties.accreditation.pasp = form.payload.properties.accreditation.pasp === 1 ? 0 : 1" class="rounded border-gray-300 text-red-400 focus:ring-red-400" />
                <span class="text-sm text-gray-700">PASP Accredited</span>
              </label>
            </div>
          </div>
          <hr class="border-gray-200">
          <div>
            <h2 class="text-base font-semibold text-gray-900">Images</h2>
            <p class="text-xs text-gray-500 mt-1">Upload facility photos (optional).</p>
            <div class="mt-2 space-y-1">
              <div v-for="(img, idx) in uploadedImages" :key="idx" class="flex items-center gap-2 text-xs">
                <span class="text-gray-600 truncate flex-1">{{ img.img_name }}</span>
                <button type="button" @click="removeImage(idx)" class="text-red-400 hover:text-red-600">Remove</button>
              </div>
            </div>
            <input type="file" accept=".jpg,.jpeg,.png,.gif,.webp" multiple @change="onFilesSelected"
              class="mt-3 block w-full text-xs text-gray-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-medium file:bg-red-50 file:text-red-500 hover:file:bg-red-100" />
            <p v-if="uploadingImages" class="text-xs text-gray-400 mt-1">Uploading...</p>
            <p v-if="imageError" class="text-xs text-red-500 mt-1">{{ imageError }}</p>
          </div>
        </div>

        <!-- Step 5: Location -->
        <div v-if="currentStep === 5" class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-base font-semibold text-gray-900">Location <span class="text-red-400">*</span></h2>
          <div class="flex gap-2">
            <input v-model="geocodeQuery" type="text" placeholder="Search address e.g. Makati City"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
              @keyup.enter="doGeocode" />
            <button type="button" @click="doGeocode" :disabled="geocoding"
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 text-sm font-medium whitespace-nowrap">
              <span v-if="geocoding" class="inline-block animate-spin mr-1">&#9696;</span>
              {{ geocoding ? '...' : 'Search' }}
            </button>
          </div>
          <ul v-if="geocodeResults.length > 0" class="bg-white border border-gray-200 rounded-lg divide-y divide-gray-200 max-h-40 overflow-y-auto shadow-sm">
            <li v-for="(result, idx) in geocodeResults" :key="idx" @click="selectGeocodeResult(result)"
              class="px-3 py-2 text-xs text-gray-700 hover:bg-red-50 cursor-pointer">
              {{ result.display_name }}
            </li>
          </ul>
          <p v-if="geocodeError" class="text-xs text-red-500">{{ geocodeError }}</p>
          <AppLocationPicker v-model:coordinates="form.payload.geometry.coordinates" />
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Latitude</label>
              <input v-model.number="form.payload.geometry.coordinates[1]" type="number" step="any" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Longitude</label>
              <input v-model.number="form.payload.geometry.coordinates[0]" type="number" step="any" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
          </div>
        </div>

        <!-- Step 6: Your Info -->
        <div v-show="currentStep === 6" class="bg-white rounded-lg shadow-sm p-6 space-y-4">
          <h2 class="text-base font-semibold text-gray-900">Your Information</h2>
          <p class="text-sm text-gray-500">We'll notify you by email once your submission is reviewed.</p>
          <div class="space-y-4 max-w-md">
            <div>
              <label class="block text-sm font-medium text-gray-700">Your Email <span class="text-red-400">*</span></label>
              <input v-model="form.submitter_email" type="email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Your Name</label>
              <input v-model="form.submitter_name" type="text" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-red-400 focus:border-red-400" />
            </div>
          </div>
        </div>

        <!-- Step 7: Review -->
        <div v-show="currentStep === 7" class="bg-white rounded-lg shadow-sm p-6 space-y-6">
          <h2 class="text-base font-semibold text-gray-900">Review Your Submission</h2>
          <p class="text-sm text-gray-500">Please verify all information before submitting.</p>

          <div class="space-y-4 text-sm">
            <section>
              <h3 class="font-semibold text-gray-600 text-xs uppercase tracking-wider mb-2">Basic Information</h3>
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
                <div><dt class="text-gray-400">Facility Name</dt><dd class="text-gray-900 font-medium">{{ form.payload.properties.placename || '—' }}</dd></div>
                <div><dt class="text-gray-400">City</dt><dd class="text-gray-900">{{ form.payload.properties.city || '—' }}</dd></div>
                <div><dt class="text-gray-400">Region</dt><dd class="text-gray-900">{{ form.payload.properties.region || '—' }}</dd></div>
                <div><dt class="text-gray-400">Address</dt><dd class="text-gray-900">{{ form.payload.properties.address || '—' }}</dd></div>
                <div class="sm:col-span-2"><dt class="text-gray-400">Source</dt><dd class="text-gray-900">{{ form.payload.properties.info_src_name || '—' }}{{ form.payload.properties.info_src_designation ? ` (${form.payload.properties.info_src_designation})` : '' }}</dd></div>
              </dl>
            </section>
            <hr class="border-gray-100">
            <section>
              <h3 class="font-semibold text-gray-600 text-xs uppercase tracking-wider mb-2">Contact</h3>
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
                <div><dt class="text-gray-400">Phone</dt><dd class="text-gray-900">{{ form.payload.properties.contact_number || '—' }}</dd></div>
                <div><dt class="text-gray-400">Email</dt><dd class="text-gray-900">{{ form.payload.properties.email_address || '—' }}</dd></div>
                <div><dt class="text-gray-400">Website</dt><dd class="text-gray-900">{{ form.payload.properties.website || '—' }}</dd></div>
              </dl>
            </section>
            <hr class="border-gray-100">
            <section>
              <h3 class="font-semibold text-gray-600 text-xs uppercase tracking-wider mb-2">Details</h3>
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
                <div><dt class="text-gray-400">Caters To</dt><dd class="text-gray-900">{{ form.payload.properties.caters_to.length ? form.payload.properties.caters_to.join(', ') : '—' }}</dd></div>
                <div><dt class="text-gray-400">Accreditation</dt><dd class="text-gray-900">{{ accreditationSummary }}</dd></div>
                <div><dt class="text-gray-400">Active Services</dt><dd class="text-gray-900">{{ activeServiceCount }}</dd></div>
                <div><dt class="text-gray-400">Images</dt><dd class="text-gray-900">{{ uploadedImages.length || 'None' }}</dd></div>
                <div class="sm:col-span-2"><dt class="text-gray-400">Coordinates</dt><dd class="text-gray-900">{{ form.payload.geometry.coordinates[1]?.toFixed(5) }}, {{ form.payload.geometry.coordinates[0]?.toFixed(5) }}</dd></div>
              </dl>
            </section>
            <hr class="border-gray-100">
            <section>
              <h3 class="font-semibold text-gray-600 text-xs uppercase tracking-wider mb-2">Submitter</h3>
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5">
                <div><dt class="text-gray-400">Email</dt><dd class="text-gray-900 font-medium">{{ form.submitter_email || '—' }}</dd></div>
                <div><dt class="text-gray-400">Name</dt><dd class="text-gray-900">{{ form.submitter_name || '—' }}</dd></div>
              </dl>
            </section>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex items-center justify-between mt-6">
          <button type="button" v-if="currentStep > 1" @click="prevStep"
            class="px-5 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm font-medium">
            &larr; Previous
          </button>
          <div v-else></div>

          <div class="flex gap-3">
            <NuxtLink to="/" class="px-5 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm text-center">
              Cancel
            </NuxtLink>
            <button v-if="currentStep < wizardSteps.length" type="button" @click="nextStep"
              class="px-5 py-2.5 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm font-medium">
              Next &rarr;
            </button>
            <button v-else type="submit" :disabled="loading"
              class="px-6 py-2.5 bg-red-400 text-white rounded-lg hover:bg-red-500 disabled:opacity-50 text-sm font-medium inline-flex items-center gap-2">
              <span v-if="loading" class="inline-block animate-spin">&#9696;</span>
              Submit for Review
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const config = useRuntimeConfig()

const wizardSteps = ['Basic', 'Contact', 'Services', 'Details', 'Location', 'You', 'Review']
const currentStep = ref(1)
const maxVisitedStep = ref(1)

const stepClass = (step: number) => {
  if (step < currentStep.value) return 'bg-red-400 border-red-400 text-white cursor-pointer'
  if (step === currentStep.value) return 'border-red-400 text-red-400'
  if (step <= maxVisitedStep.value) return 'border-gray-300 text-gray-500 cursor-pointer hover:border-red-300'
  return 'border-gray-200 text-gray-300 cursor-not-allowed'
}

const nextStep = () => {
  if (!validateStep(currentStep.value)) return
  if (currentStep.value < wizardSteps.length) {
    currentStep.value++
    if (currentStep.value > maxVisitedStep.value) maxVisitedStep.value = currentStep.value
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToStep = (step: number) => {
  if (step <= maxVisitedStep.value) {
    currentStep.value = step
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const validateStep = (step: number): boolean => {
  error.value = ''
  switch (step) {
    case 1:
      if (!form.payload.properties.placename.trim()) {
        error.value = 'Please enter the facility name.'
        return false
      }
      return true
    case 6:
      if (!form.submitter_email.trim()) {
        error.value = 'Please provide your email address.'
        return false
      }
      return true
    default:
      return true
  }
}

const defaultServices: Record<string, { label: string; mode: { teletherapy: number; onsite: number; home_service: number } }> = {
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

const catersToOptions = ["Pediatric", "Adolescent", "Adult"]

const form = reactive({
  submitter_email: '',
  submitter_name: '',
  payload: {
    properties: {
      placename: '',
      address: '',
      region: '',
      city: '',
      landmarks_desc: '',
      info_src_name: '',
      info_src_designation: '',
      contact_number: '',
      alt_contact_number: '',
      email_address: '',
      website: '',
      social_media: { facebook: '', instagram: '' },
      services_offered: JSON.parse(JSON.stringify(defaultServices)),
      caters_to: [] as string[],
      accreditation: { paot: 0, pasp: 0 },
      images: [] as { img_name: string; img_url: string }[],
    },
    geometry: {
      type: 'Point' as const,
      coordinates: [121.7740, 12.8797],
    },
  },
})

const loading = ref(false)
const error = ref('')
const success = ref('')
const uploadedImages = ref<{ img_name: string; img_url: string }[]>([])
const uploadingImages = ref(false)
const imageError = ref('')

const geocodeQuery = ref('')
const geocoding = ref(false)
const geocodeError = ref('')
const geocodeResults = ref<{ display_name: string; lat: string; lon: string }[]>([])

const activeServiceCount = computed(() => {
  let count = 0
  for (const key in form.payload.properties.services_offered) {
    if (serviceActive(key)) count++
  }
  return count
})

const accreditationSummary = computed(() => {
  const parts: string[] = []
  if (form.payload.properties.accreditation.paot === 1) parts.push('PAOT')
  if (form.payload.properties.accreditation.pasp === 1) parts.push('PASP')
  return parts.length ? parts.join(', ') : 'None'
})

interface GeocodeResult {
  display_name: string
  lat: string
  lon: string
}

const doGeocode = async () => {
  const q = geocodeQuery.value.trim()
  if (!q) return
  geocodeError.value = ''
  geocodeResults.value = []
  geocoding.value = true

  try {
    const res = await fetch(`${config.public.apiURL}/geocode?q=${encodeURIComponent(q)}`)
    if (!res.ok) {
      const errMsg = await parseApiError(res, 'Geocoding failed')
      throw new Error(errMsg)
    }
    const data = await res.json()
    if (data.features && data.features.length > 0) {
      geocodeResults.value = data.features
    } else {
      geocodeError.value = 'No locations found. Try a more specific address.'
    }
  } catch (e: any) {
    geocodeError.value = e.message || 'Geocoding failed'
  } finally {
    geocoding.value = false
  }
}

const selectGeocodeResult = (result: GeocodeResult) => {
  form.payload.geometry.coordinates = [parseFloat(result.lon), parseFloat(result.lat)]
  geocodeResults.value = []
}

const serviceActive = (key: string): boolean => {
  const s = form.payload.properties.services_offered[key]
  if (!s) return false
  return s.mode.teletherapy > 0 || s.mode.onsite > 0 || s.mode.home_service > 0
}

const onFilesSelected = async (e: Event) => {
  const target = e.target as HTMLInputElement
  const files = target.files
  if (!files || files.length === 0) return

  imageError.value = ''
  uploadingImages.value = true

  for (const file of files) {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${config.public.apiURL}/submissions/upload-image`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        const errMsg = await parseApiError(res, 'Upload failed')
        throw new Error(errMsg)
      }
      const data = await res.json()
      if (data.img_name && data.img_url) {
        uploadedImages.value.push(data)
      } else if (data.error) {
        throw new Error(data.error)
      }
    } catch (e: any) {
      imageError.value = `Failed to upload ${file.name}: ${e.message}`
    }
  }

  target.value = ''
  uploadingImages.value = false
}

const removeImage = (idx: number) => {
  uploadedImages.value.splice(idx, 1)
}

const formatApiError = (err: unknown, fallback = 'Request failed'): string => {
  if (!err) return fallback
  if (typeof err === 'string') return err
  if (err instanceof Error) return err.message
  const obj = err as Record<string, unknown>
  if (obj.detail) return String(obj.detail)
  const messages = Object.entries(obj).flatMap(([, value]) => {
    if (Array.isArray(value)) return value.map((v) => String(v))
    return [String(value)]
  })
  return messages.join(', ') || fallback
}

const parseApiError = async (res: Response, fallback = 'Request failed'): Promise<string> => {
  const text = await res.text()
  try {
    const data = JSON.parse(text)
    return formatApiError(data, fallback)
  } catch {
    const snippet = text.replace(/\s+/g, ' ').slice(0, 120)
    return `${fallback} (HTTP ${res.status} ${res.url}): ${snippet || 'Empty response'}`
  }
}

const handleSubmit = async () => {
  error.value = ''
  success.value = ''

  if (!form.submitter_email.trim()) {
    error.value = 'Please provide your email address.'
    return
  }

  if (!form.payload.properties.placename.trim()) {
    error.value = 'Please provide the facility name.'
    return
  }

  loading.value = true

  const payload = {
    submitter_email: form.submitter_email,
    submitter_name: form.submitter_name,
    payload: {
      properties: {
        ...form.payload.properties,
        images: uploadedImages.value,
      },
      geometry: form.payload.geometry,
    },
    images: uploadedImages.value,
  }

  try {
    const res = await fetch(`${config.public.apiURL}/submissions/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!res.ok) {
      const errMsg = await parseApiError(res, 'Failed to submit')
      throw new Error(errMsg)
    }

    success.value = 'Your facility submission has been received and is pending review. You will be notified by email once it has been reviewed.'
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
