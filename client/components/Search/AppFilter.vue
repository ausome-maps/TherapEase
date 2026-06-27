<script setup>
import { ref, reactive, computed } from 'vue'

const emit = defineEmits(['query-generated'])

const showModal = ref(false)

const isPASPChecked = ref(false)
const isPAOTChecked = ref(false)
const teletherapyChecked = ref(false)
const onsiteChecked = ref(false)
const homeserviceChecked = ref(false)
const individualChecked = ref(false)
const groupChecked = ref(false)

const serviceCheckboxes = reactive({
  speechlanguagetherapy: false,
  speechlanguagepathology: false,
  occupationaltherapy: false,
  behavioraltherapy: false,
  physicaltherapy: false,
  lifeskillstraining: false,
  socialskillstraining: false,
  integration: false,
  integrationprogram: false,
  jobcoaching: false,
  specialeducation: false,
  spedtutorials: false,
  parentcoaching: false,
  educationsessionforfamilies: false,
  feeding: false,
  counseling: false,
  psychotherapy: false,
  abatherapy: false,
  mnri: false,
  sensoryintegration: false,
  playschool: false,
  dysphagiamanagement: false,
  orthoses: false,
  homeschoolfacilitation: false,
  rehabconsultation: false,
})

const services = [
  { key: 'speechlanguagetherapy', label: 'Speech-Language Therapy' },
  { key: 'speechlanguagepathology', label: 'Speech-Language Pathology' },
  { key: 'occupationaltherapy', label: 'Occupational Therapy' },
  { key: 'behavioraltherapy', label: 'Behavioral Therapy' },
  { key: 'physicaltherapy', label: 'Physical Therapy' },
  { key: 'lifeskillstraining', label: 'Life Skills Training' },
  { key: 'socialskillstraining', label: 'Social Skills Training' },
  { key: 'integration', label: 'Integration' },
  { key: 'integrationprogram', label: 'Integration Program' },
  { key: 'jobcoaching', label: 'Job Coaching' },
  { key: 'specialeducation', label: 'Special Education' },
  { key: 'spedtutorials', label: 'SpEd Tutorials' },
  { key: 'parentcoaching', label: 'Parent Coaching' },
  { key: 'educationsessionforfamilies', label: 'Education Session for Families' },
  { key: 'feeding', label: 'Feeding' },
  { key: 'counseling', label: 'Counseling' },
  { key: 'psychotherapy', label: 'Psychotherapy' },
  { key: 'abatherapy', label: 'ABA Therapy' },
  { key: 'mnri', label: 'MNRI' },
  { key: 'sensoryintegration', label: 'Sensory Integration' },
  { key: 'playschool', label: 'Play School' },
  { key: 'dysphagiamanagement', label: 'Dysphagia Management' },
  { key: 'orthoses', label: 'Orthoses (Splinting)' },
  { key: 'homeschoolfacilitation', label: 'Homeschool Facilitation' },
  { key: 'rehabconsultation', label: 'Rehab Consultation' },
]

const activeFilterCount = computed(() => {
  let count = 0
  if (isPASPChecked.value) count++
  if (isPAOTChecked.value) count++
  if (teletherapyChecked.value) count++
  if (onsiteChecked.value) count++
  if (homeserviceChecked.value) count++
  if (individualChecked.value) count++
  if (groupChecked.value) count++
  for (const key in serviceCheckboxes) {
    if (serviceCheckboxes[key]) count++
  }
  return count
})

function generateFilterQuery() {
  const filters = {}

  const accreditation = {}
  if (isPASPChecked.value) accreditation.pasp = 1
  if (isPAOTChecked.value) accreditation.paot = 1
  if (Object.keys(accreditation).length > 0) {
    filters.accreditation = accreditation
  }

  const modes = []
  if (teletherapyChecked.value) modes.push('teletherapy')
  if (onsiteChecked.value) modes.push('onsite')
  if (homeserviceChecked.value) modes.push('home_service')
  if (modes.length > 0) {
    filters.mode = modes
  }

  const sessionTypes = []
  if (individualChecked.value) sessionTypes.push('individual')
  if (groupChecked.value) sessionTypes.push('group')
  if (sessionTypes.length > 0) {
    filters.session_type = sessionTypes
  }

  const selectedServices = []
  for (const key in serviceCheckboxes) {
    if (serviceCheckboxes[key]) {
      selectedServices.push(key)
    }
  }
  if (selectedServices.length > 0) {
    filters.services_offered = selectedServices
  }

  emit('query-generated', { filters, filter: filters })
}

function clearAllFilters() {
  isPASPChecked.value = false
  isPAOTChecked.value = false
  teletherapyChecked.value = false
  onsiteChecked.value = false
  homeserviceChecked.value = false
  individualChecked.value = false
  groupChecked.value = false

  for (const key in serviceCheckboxes) {
    serviceCheckboxes[key] = false
  }

  emit('query-generated', { filters: {}, filter: {} })
}

function openModal() {
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  showModal.value = false
  document.body.style.overflow = ''
}

function applyFilters() {
  generateFilterQuery()
  closeModal()
}
</script>

<template>
  <div>
    <div class="flex justify-center p-4">
      <button
        type="button"
        class="relative border shadow-md p-2 px-5 active:shadow-sm rounded-3xl hover:bg-gray-50"
        @click="openModal"
      >
        Filter
        <span
          v-if="activeFilterCount > 0"
          class="absolute -top-2 -right-2 bg-red-400 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center"
        >
          {{ activeFilterCount }}
        </span>
      </button>
    </div>

    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-start justify-center p-2 overflow-y-auto bg-black/50"
        @click.self="closeModal"
        role="dialog"
        aria-modal="true"
      >
        <div class="relative w-full max-w-3xl my-8" @click.stop>
          <div class="relative bg-white rounded-lg shadow-lg border border-black">
            <div class="flex justify-center items-start p-4 border-b rounded-t">
              <h3 class="text-xl font-semibold text-gray-900 lg:text-2xl">
                Filter
              </h3>
              <button
                type="button"
                class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto absolute right-5 inline-flex items-center"
                @click="closeModal"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path
                    fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </button>
            </div>

          <div class="content-body px-4 sm:px-10 py-4 space-y-6 overflow-y-auto max-h-[calc(100vh-12rem)]">
            <h2 class="font-bold">Accreditation</h2>
            <div class="flex justify-between border-b pb-6">
              <div>
                <AppCheckbox
                  label="Philippine Association of Speech Pathologists"
                  id_="PASP"
                  v-model="isPASPChecked"
                />
              </div>
              <div>
                <AppCheckbox
                  label="Philippine Academy of Occupational Therapist"
                  id_="PAOT"
                  v-model="isPAOTChecked"
                />
              </div>
            </div>

            <div>
              <h2 class="font-bold">Mode of Intervention</h2>
            </div>
            <div class="flex space-x-2 sm:space-x-4 md:space-x-6 lg:space-x-6 pb-6 border-b">
              <button
                type="button"
                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border-2 shadow-md rounded-md transition-colors cursor-pointer"
                :class="teletherapyChecked ? 'border-black bg-gray-50 text-gray-900' : 'border-gray-200 text-gray-500 hover:text-gray-700'"
                @click="teletherapyChecked = !teletherapyChecked"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
                <span class="mt-2 text-sm font-medium">Teletherapy</span>
              </button>
              <button
                type="button"
                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border-2 shadow-md rounded-md transition-colors cursor-pointer"
                :class="onsiteChecked ? 'border-black bg-gray-50 text-gray-900' : 'border-gray-200 text-gray-500 hover:text-gray-700'"
                @click="onsiteChecked = !onsiteChecked"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
                </svg>
                <span class="mt-2 text-sm font-medium">Onsite</span>
              </button>
              <button
                type="button"
                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border-2 shadow-md rounded-md transition-colors cursor-pointer"
                :class="homeserviceChecked ? 'border-black bg-gray-50 text-gray-900' : 'border-gray-200 text-gray-500 hover:text-gray-700'"
                @click="homeserviceChecked = !homeserviceChecked"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819" />
                </svg>
                <span class="mt-2 text-sm font-medium">Home Service</span>
              </button>
            </div>

            <div>
              <h2 class="font-bold">Type of Session</h2>
            </div>
            <div class="flex space-x-2 sm:space-x-4 md:space-x-6 lg:space-x-6 pb-6 border-b">
              <button
                type="button"
                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border-2 shadow-md rounded-md transition-colors cursor-pointer"
                :class="individualChecked ? 'border-black bg-gray-50 text-gray-900' : 'border-gray-200 text-gray-500 hover:text-gray-700'"
                @click="individualChecked = !individualChecked"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
                <span class="mt-2 px-2 text-sm font-medium">Individual</span>
              </button>

              <button
                type="button"
                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border-2 shadow-md rounded-md transition-colors cursor-pointer"
                :class="groupChecked ? 'border-black bg-gray-50 text-gray-900' : 'border-gray-200 text-gray-500 hover:text-gray-700'"
                @click="groupChecked = !groupChecked"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
                </svg>
                <span class="mt-2 px-2 text-sm font-medium">Group</span>
              </button>
            </div>

            <div>
              <h2 class="font-bold">Interventions</h2>
            </div>
            <div class="grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-2">
              <AppCheckbox
                v-for="service in services"
                :key="service.key"
                :label="service.label"
                v-model="serviceCheckboxes[service.key]"
                :id_="service.key"
                class="min-h-[35px]"
              />
            </div>
          </div>

            <div
              class="flex items-center p-6 space-x-2 border-t justify-between border-gray-200 rounded-b"
            >
              <button
                type="button"
                @click="clearAllFilters"
                class="border px-4 py-2 bg-white hover:bg-gray-200 active:bg-gray-300 text-black rounded-lg"
              >
                Clear all filters
              </button>
              <button
                type="button"
                @click="applyFilters"
                class="border px-4 py-2 bg-black active:bg-gray-700 text-white rounded-lg"
              >
                Apply filters
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.content-body::-webkit-scrollbar,
.content-body::-webkit-scrollbar-thumb {
  width: 8px;
  border-radius: 13px;
  background-clip: padding-box;
  border: 2px solid transparent;
}

.content-body::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 0 10px;
}
</style>
