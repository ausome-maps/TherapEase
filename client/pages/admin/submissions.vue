<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-col sm:flex-row gap-3 sm:gap-0">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Facility Submissions</h2>
        <p class="mt-1 text-sm text-gray-600">Review and approve/reject new facility submissions</p>
      </div>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      {{ error }}
    </div>
    <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
      {{ successMsg }}
    </div>

    <div class="flex items-center gap-3 flex-wrap">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search placename, email, name..."
        class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm text-sm w-64 focus:outline-none focus:ring-red-400 focus:border-red-400"
        @keyup.enter="searchSubmissions"
      />
      <button
        @click="searchSubmissions"
        class="px-3 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm font-medium"
      >
        Search
      </button>
      <label for="statusFilter" class="text-sm font-medium text-gray-700 ml-2">Status:</label>
      <select
        id="statusFilter"
        v-model="statusFilter"
        @change="searchSubmissions"
        class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm text-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
      >
        <option value="">All</option>
        <option value="new">New</option>
        <option value="in_review">In Review</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
        <option value="merged">Merged</option>
      </select>
      <label for="orderingFilter" class="text-sm font-medium text-gray-700">Sort:</label>
      <select
        id="orderingFilter"
        v-model="ordering"
        @change="searchSubmissions"
        class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm text-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
      >
        <option value="-created_at">Newest first</option>
        <option value="created_at">Oldest first</option>
        <option value="submitter_email">Email A-Z</option>
        <option value="-submitter_email">Email Z-A</option>
      </select>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
      <p class="mt-4 text-gray-600">Loading submissions...</p>
    </div>

    <div v-else class="bg-white shadow rounded-lg overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Placename</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submitter</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submitted</th>
            <th class="px-3 sm:px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in submissionsList" :key="item.id" class="hover:bg-gray-50">
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900 max-w-[200px] truncate">
                {{ item.placename || '—' }}
              </div>
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-[180px] truncate">
              {{ item.submitter_email }}
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
              <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                :class="statusBadgeClass(item.status)">
                {{ statusLabel(item.status) }}
              </span>
            </td>
            <td class="hidden sm:table-cell px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatDate(item.created_at) }}
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-right text-xs sm:text-sm font-medium">
              <button @click="openDetailModal(item)" class="text-red-400 hover:text-red-500 mr-2">View</button>
              <button @click="confirmDelete(item)" class="text-red-600 hover:text-red-800">Del</button>
            </td>
          </tr>
          <tr v-if="submissionsList.length === 0">
            <td colspan="5" class="px-6 py-12 text-center text-gray-500">No submissions found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="totalPages > 1" class="flex items-center justify-between gap-4 pt-2">
      <span class="text-xs text-gray-500">
        Page {{ currentPage }} of {{ totalPages }}
        <span class="hidden sm:inline">({{ totalCount }} submissions)</span>
      </span>
      <div class="flex items-center gap-2">
        <button
          :disabled="currentPage <= 1"
          @click="goToPage(currentPage - 1)"
          class="px-3 py-1.5 border border-gray-300 rounded-lg text-sm hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          &larr; Prev
        </button>
        <template v-for="p in visiblePages" :key="p">
          <button
            v-if="p !== '...'"
            @click="goToPage(p as number)"
            class="px-3 py-1.5 rounded-lg text-sm"
            :class="p === currentPage ? 'bg-red-400 text-white' : 'border border-gray-300 hover:bg-gray-50'"
          >
            {{ p }}
          </button>
          <span v-else class="px-1 text-gray-400">...</span>
        </template>
        <button
          :disabled="currentPage >= totalPages"
          @click="goToPage(currentPage + 1)"
          class="px-3 py-1.5 border border-gray-300 rounded-lg text-sm hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          Next &rarr;
        </button>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-gray-900">Submission Details</h3>
          <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="modalError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {{ modalError }}
        </div>

        <div v-if="viewingSubmission">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm mb-4">
            <div>
              <span class="font-medium text-gray-500">Submitter Email:</span>
              <p class="text-gray-900">{{ viewingSubmission.submitter_email }}</p>
            </div>
            <div>
              <span class="font-medium text-gray-500">Submitter Name:</span>
              <p class="text-gray-900">{{ viewingSubmission.submitter_name || '—' }}</p>
            </div>
            <div>
              <span class="font-medium text-gray-500">Status:</span>
              <p class="text-gray-900">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium" :class="statusBadgeClass(viewingSubmission.status)">
                  {{ statusLabel(viewingSubmission.status) }}
                </span>
              </p>
            </div>
            <div>
              <span class="font-medium text-gray-500">Submitted:</span>
              <p class="text-gray-900">{{ formatDate(viewingSubmission.created_at) }}</p>
            </div>
          </div>

          <div class="border-t border-gray-200 pt-4 space-y-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700">Facility Data</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
              <div>
                <span class="font-medium text-gray-500">Placename:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.placename || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Address:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.address || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">City:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.city || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Region:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.region || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Contact Number:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.contact_number || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Email:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.email_address || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Website:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.website || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Location:</span>
                <p class="text-gray-900" v-if="viewingSubmission.payload?.geometry?.coordinates">
                  {{ viewingSubmission.payload.geometry.coordinates[1]?.toFixed(5) }}, {{ viewingSubmission.payload.geometry.coordinates[0]?.toFixed(5) }}
                </p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Source Name:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.info_src_name || '—' }}</p>
              </div>
              <div>
                <span class="font-medium text-gray-500">Source Designation:</span>
                <p class="text-gray-900">{{ viewingSubmission.payload?.properties?.info_src_designation || '—' }}</p>
              </div>
            </div>
          </div>

          <div v-if="submissionCoords" class="border-t border-gray-200 pt-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Location Map</h4>
            <AppLocationPicker :coordinates="submissionCoords" :readonly="true" />
          </div>

          <div v-if="viewingSubmission.payload?.properties?.services_offered" class="border-t border-gray-200 pt-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Services Offered</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div v-for="(svc, key) in viewingSubmission.payload.properties.services_offered" :key="key">
                <template v-if="svc.mode">
                  <span v-if="svc.mode.teletherapy > 0 || svc.mode.onsite > 0 || svc.mode.home_service > 0">
                    <span class="font-medium">{{ svc.label || key }}:</span>
                    <span v-if="svc.mode.teletherapy > 0"> Tele:{{ modeLabel(svc.mode.teletherapy) }}</span>
                    <span v-if="svc.mode.onsite > 0"> Onsite:{{ modeLabel(svc.mode.onsite) }}</span>
                    <span v-if="svc.mode.home_service > 0"> Home:{{ modeLabel(svc.mode.home_service) }}</span>
                  </span>
                </template>
              </div>
            </div>
          </div>

          <div class="border-t border-gray-200 pt-4 space-y-4">
            <div>
              <label for="modalNotes" class="block text-sm font-medium text-gray-700">Admin Notes</label>
              <textarea
                id="modalNotes"
                v-model="modalNotes"
                rows="3"
                placeholder="Add notes or rejection reason..."
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400 text-sm"
                :disabled="viewingSubmission.status === 'merged'"
              ></textarea>
            </div>
            <div v-if="viewingSubmission.admin_notes && viewingSubmission.admin_notes !== modalNotes" class="text-xs text-gray-400">
              Previous notes: {{ viewingSubmission.admin_notes }}
            </div>
          </div>

          <div class="flex gap-3 pt-2" v-if="viewingSubmission.status === 'new' || viewingSubmission.status === 'in_review'">
            <button
              type="button"
              @click="handleAction('review')"
              :disabled="modalSaving"
              class="flex-1 py-2 px-4 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 disabled:opacity-50 text-sm font-medium"
            >
              {{ modalSaving ? 'Saving...' : 'Mark In Review' }}
            </button>
            <button
              type="button"
              @click="handleApprove"
              :disabled="modalSaving"
              class="flex-1 py-2 px-4 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 text-sm font-medium"
            >
              {{ modalSaving ? 'Saving...' : 'Approve & Merge' }}
            </button>
            <button
              type="button"
              @click="handleReject"
              :disabled="modalSaving || !modalNotes.trim()"
              class="flex-1 py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 text-sm font-medium"
            >
              {{ modalSaving ? 'Saving...' : 'Reject' }}
            </button>
          </div>

          <div v-if="viewingSubmission.status === 'rejected'" class="border-t border-gray-200 pt-4">
            <p class="text-sm text-gray-500">This submission was rejected.</p>
          </div>

          <div v-if="viewingSubmission.status === 'merged'" class="border-t border-gray-200 pt-4">
            <p class="text-sm text-green-600 font-medium">This submission has been approved and merged into the database.</p>
            <NuxtLink v-if="viewingSubmission.merged_facility"
              :to="`/details-page?id=${viewingSubmission.merged_facility}`"
              class="text-sm text-red-400 hover:text-red-500 mt-1 inline-block">
              View on map &rarr;
            </NuxtLink>
          </div>

          <div class="border-t border-gray-200 pt-3 mt-2">
            <button
              type="button"
              @click="deleteFromModal"
              class="py-1.5 px-3 border border-red-300 text-red-500 rounded-lg hover:bg-red-50 text-xs font-medium"
            >
              Delete Submission
            </button>
          </div>
        </div>

        <div class="flex pt-2">
          <button
            type="button"
            @click="closeModal"
            class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6 space-y-4">
        <h3 class="text-lg font-bold text-gray-900">Delete Submission</h3>
        <p class="text-sm text-gray-600">
          Are you sure you want to delete the submission
          <strong>{{ deletingSubmission?.placename || '—' }}</strong>?
        </p>
        <p class="text-xs text-red-500">This action cannot be undone.</p>
        <div v-if="deleteError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {{ deleteError }}
        </div>
        <div class="flex gap-3 pt-2">
          <button
            type="button"
            @click="showDeleteConfirm = false; deletingSubmission = null"
            :disabled="deleting"
            class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="handleDelete"
            :disabled="deleting"
            class="flex-1 py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 text-sm font-medium"
          >
            {{ deleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

definePageMeta({ layout: 'admin' })

interface FacilitySubmissionItem {
  id: string
  payload: {
    properties: Record<string, any>
    geometry: { type: string; coordinates: number[] }
  }
  images: any[]
  status: string
  admin_notes: string
  submitter_email: string
  submitter_name: string
  merged_facility: string | null
  created_at: string
  updated_at: string
  placename: string
}

const { isStaff, isSuperuser, initAuth, authedFetch, formatApiError } = useAuth()
const config = useRuntimeConfig()

const submissionsList = ref<FacilitySubmissionItem[]>([])
const loading = ref(true)
const error = ref('')
const successMsg = ref('')
const statusFilter = ref('')
const searchQuery = ref('')
const ordering = ref('-created_at')
const currentPage = ref(1)
const totalPages = ref(1)
const totalCount = ref(0)
const pageSize = ref(20)

const showModal = ref(false)
const viewingSubmission = ref<FacilitySubmissionItem | null>(null)
const modalNotes = ref('')
const modalError = ref('')
const modalSaving = ref(false)

const showDeleteConfirm = ref(false)
const deletingSubmission = ref<FacilitySubmissionItem | null>(null)
const deleting = ref(false)
const deleteError = ref('')

const submissionCoords = computed(() => {
  const coords = viewingSubmission.value?.payload?.geometry?.coordinates
  if (coords && coords.length === 2) {
    return [coords[0], coords[1]]
  }
  return null
})

const statusBadgeClass = (status: string) => {
  switch (status) {
    case 'new': return 'bg-blue-100 text-blue-800'
    case 'in_review': return 'bg-yellow-100 text-yellow-800'
    case 'approved': return 'bg-green-100 text-green-800'
    case 'rejected': return 'bg-red-100 text-red-800'
    case 'merged': return 'bg-green-100 text-green-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const statusLabel = (status: string) => {
  switch (status) {
    case 'new': return 'New'
    case 'in_review': return 'In Review'
    case 'approved': return 'Approved'
    case 'rejected': return 'Rejected'
    case 'merged': return 'Merged'
    default: return status
  }
}

const modeLabel = (val: number) => {
  switch (val) {
    case 1: return '1:1'
    case 2: return 'Group'
    case 3: return 'Both'
    default: return String(val)
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString()
}

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }
  pages.push(1)
  if (current > 3) pages.push('...')
  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  for (let i = start; i <= end; i++) pages.push(i)
  if (current < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadSubmissions()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const loadSubmissions = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = new URLSearchParams()
    if (statusFilter.value) params.set('status', statusFilter.value)
    if (searchQuery.value.trim()) params.set('search', searchQuery.value.trim())
    params.set('ordering', ordering.value)
    params.set('page', String(currentPage.value))
    params.set('page_size', String(pageSize.value))
    let url = `${config.public.apiURL}/submissions/?${params.toString()}`
    const res = await authedFetch(url)
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to load submissions' }))
      throw new Error(formatApiError(err, 'Failed to load submissions'))
    }
    const data = await res.json()
    if (Array.isArray(data)) {
      submissionsList.value = data
      totalCount.value = data.length
      totalPages.value = 1
      currentPage.value = 1
    } else if (data.results) {
      submissionsList.value = data.results
      totalCount.value = data.count || data.results.length
      totalPages.value = Math.max(1, Math.ceil(totalCount.value / pageSize.value))
    } else if (data.data && Array.isArray(data.data)) {
      submissionsList.value = data.data
      const meta = data.meta?.pagination
      totalCount.value = meta?.count || data.data.length
      totalPages.value = meta?.pages || Math.max(1, Math.ceil(totalCount.value / pageSize.value))
    } else {
      submissionsList.value = []
      totalCount.value = 0
      totalPages.value = 1
    }
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const searchSubmissions = () => {
  currentPage.value = 1
  loadSubmissions()
}

onMounted(async () => {
  await initAuth()
  if (!isStaff.value && !isSuperuser.value) {
    loading.value = false
    return
  }
  await loadSubmissions()
})

const openDetailModal = (item: FacilitySubmissionItem) => {
  viewingSubmission.value = item
  modalNotes.value = ''
  modalError.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  viewingSubmission.value = null
}

const confirmDelete = (item: FacilitySubmissionItem) => {
  deletingSubmission.value = item
  deleteError.value = ''
  showDeleteConfirm.value = true
}

const deleteFromModal = () => {
  if (viewingSubmission.value) {
    confirmDelete(viewingSubmission.value)
    closeModal()
  }
}

const handleDelete = async () => {
  if (!deletingSubmission.value) return
  deleting.value = true
  deleteError.value = ''
  try {
    const res = await authedFetch(
      `${config.public.apiURL}/submissions/${deletingSubmission.value.id}`,
      { method: 'DELETE' },
    )
    if (res.status === 204) {
      showDeleteConfirm.value = false
      deletingSubmission.value = null
      successMsg.value = 'Submission deleted.'
      setTimeout(() => { successMsg.value = '' }, 3000)
      await loadSubmissions()
    } else {
      const err = await res.json().catch(() => ({ detail: 'Delete failed' }))
      throw new Error(formatApiError(err, 'Delete failed'))
    }
  } catch (e: any) {
    deleteError.value = e.message
  } finally {
    deleting.value = false
  }
}

const handleAction = async (action: string) => {
  if (!viewingSubmission.value) return
  modalError.value = ''
  modalSaving.value = true
  try {
    const body: Record<string, string> = {}
    if (modalNotes.value.trim()) {
      body.admin_notes = modalNotes.value
    }
    const res = await authedFetch(
      `${config.public.apiURL}/submissions/${viewingSubmission.value.id}/${action}`,
      {
        method: 'POST',
        body: JSON.stringify(body),
      },
    )
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Action failed' }))
      throw new Error(formatApiError(err, 'Action failed'))
    }
    const updated = await res.json()
    viewingSubmission.value = updated
    successMsg.value = action === 'review' ? 'Status updated to In Review.' :
      action === 'reject' ? 'Submission rejected.' : 'Submission approved.'
    closeModal()
    await loadSubmissions()
    setTimeout(() => { successMsg.value = '' }, 3000)
  } catch (e: any) {
    modalError.value = e.message
  } finally {
    modalSaving.value = false
  }
}

const handleApprove = () => handleAction('approve')
const handleReject = () => handleAction('reject')
</script>
