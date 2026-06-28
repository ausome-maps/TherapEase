<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-col sm:flex-row gap-3 sm:gap-0">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Feedback</h2>
        <p class="mt-1 text-sm text-gray-600">View and manage user feedback submissions</p>
      </div>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      {{ error }}
    </div>
    <div v-if="successMsg" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
      {{ successMsg }}
    </div>

    <div class="flex items-center gap-3 flex-wrap">
      <label for="statusFilter" class="text-sm font-medium text-gray-700">Status:</label>
      <select
        id="statusFilter"
        v-model="statusFilter"
        @change="loadFeedback"
        class="px-3 py-2 border border-gray-300 rounded-lg shadow-sm text-sm focus:outline-none focus:ring-red-400 focus:border-red-400"
      >
        <option value="">All</option>
        <option value="new">New</option>
        <option value="in_review">In Review</option>
        <option value="resolved">Resolved</option>
        <option value="dismissed">Dismissed</option>
      </select>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
      <p class="mt-4 text-gray-600">Loading feedback...</p>
    </div>

    <div v-else class="bg-white shadow rounded-lg overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Facility</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contact</th>
            <th class="px-3 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="hidden sm:table-cell px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submitted</th>
            <th class="px-3 sm:px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="item in feedbackList" :key="item.id" class="hover:bg-gray-50">
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900 max-w-[200px] truncate">
                {{ item.facility_name || '—' }}
              </div>
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-[180px] truncate">
              {{ item.email_address }}
            </td>
            <td class="px-3 sm:px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ item.contact_number }}
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
              <button @click="openDetailModal(item)" class="text-red-400 hover:text-red-500 mr-1 sm:mr-3">View</button>
              <button @click="confirmDelete(item)" class="text-red-600 hover:text-red-800">Delete</button>
            </td>
          </tr>
          <tr v-if="feedbackList.length === 0">
            <td colspan="6" class="px-6 py-12 text-center text-gray-500">No feedback found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail / Action Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-xl font-bold text-gray-900">Feedback Details</h3>

        <div v-if="modalError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
          {{ modalError }}
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          <div>
            <span class="font-medium text-gray-500">Facility:</span>
            <p class="text-gray-900">{{ viewingFeedback?.facility_name || '—' }}</p>
          </div>
          <div>
            <span class="font-medium text-gray-500">Email:</span>
            <p class="text-gray-900">{{ viewingFeedback?.email_address }}</p>
          </div>
          <div>
            <span class="font-medium text-gray-500">Contact:</span>
            <p class="text-gray-900">{{ viewingFeedback?.contact_number }}</p>
          </div>
          <div>
            <span class="font-medium text-gray-500">Submitted:</span>
            <p class="text-gray-900">{{ formatDate(viewingFeedback?.created_at) }}</p>
          </div>
        </div>

        <div class="border-t border-gray-200 pt-4 space-y-4">
          <div>
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Concerns/Suggestions regarding data on the platform</h4>
            <p class="text-sm text-gray-600 bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">{{ viewingFeedback?.data_concerns }}</p>
          </div>
          <div>
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Concerns/Suggestions regarding features and usability</h4>
            <p class="text-sm text-gray-600 bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">{{ viewingFeedback?.usability_concerns }}</p>
          </div>
        </div>

        <div class="border-t border-gray-200 pt-4 space-y-4">
          <div>
            <label for="modalStatus" class="block text-sm font-medium text-gray-700">Status</label>
            <select
              id="modalStatus"
              v-model="modalStatus"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400 text-sm"
            >
              <option value="new">New</option>
              <option value="in_review">In Review</option>
              <option value="resolved">Resolved</option>
              <option value="dismissed">Dismissed</option>
            </select>
          </div>
          <div>
            <label for="modalNotes" class="block text-sm font-medium text-gray-700">Admin Notes</label>
            <textarea
              id="modalNotes"
              v-model="modalNotes"
              rows="3"
              placeholder="Add internal notes about this feedback..."
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400 text-sm"
            ></textarea>
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button
            type="button"
            @click="handleUpdate"
            :disabled="modalSaving"
            class="flex-1 py-2 px-4 bg-red-400 text-white rounded-lg hover:bg-red-500 disabled:opacity-50 text-sm font-medium"
          >
            {{ modalSaving ? 'Saving...' : 'Save' }}
          </button>
          <button
            type="button"
            @click="closeModal"
            class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-sm w-full p-6 space-y-4">
        <h3 class="text-xl font-bold text-gray-900">Delete Feedback</h3>
        <p class="text-gray-600 text-sm">
          Are you sure you want to delete this feedback from <strong>{{ deletingFeedback?.email_address }}</strong>? This action cannot be undone.
        </p>
        <div class="flex gap-3">
          <button @click="handleDelete"
            class="flex-1 py-2 px-4 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium">
            Delete
          </button>
          <button @click="showDeleteModal = false"
            class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

definePageMeta({ layout: 'admin' })

interface FeedbackItem {
  id: string
  facility: string
  facility_name: string
  email_address: string
  contact_number: string
  data_concerns: string
  usability_concerns: string
  status: string
  admin_notes: string
  created_at: string
  updated_at: string
}

const { isStaff, isSuperuser, initAuth, authedFetch, formatApiError } = useAuth()
const config = useRuntimeConfig()

const feedbackList = ref<FeedbackItem[]>([])
const loading = ref(true)
const error = ref('')
const successMsg = ref('')
const statusFilter = ref('')

const showModal = ref(false)
const showDeleteModal = ref(false)
const viewingFeedback = ref<FeedbackItem | null>(null)
const deletingFeedback = ref<FeedbackItem | null>(null)
const modalStatus = ref('new')
const modalNotes = ref('')
const modalError = ref('')
const modalSaving = ref(false)

const statusBadgeClass = (status: string) => {
  switch (status) {
    case 'new': return 'bg-blue-100 text-blue-800'
    case 'in_review': return 'bg-yellow-100 text-yellow-800'
    case 'resolved': return 'bg-green-100 text-green-800'
    case 'dismissed': return 'bg-red-100 text-red-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

const statusLabel = (status: string) => {
  switch (status) {
    case 'new': return 'New'
    case 'in_review': return 'In Review'
    case 'resolved': return 'Resolved'
    case 'dismissed': return 'Dismissed'
    default: return status
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString()
}

const loadFeedback = async () => {
  loading.value = true
  error.value = ''
  try {
    let url = `${config.public.apiURL}/feedback/`
    if (statusFilter.value) {
      url += `?status=${statusFilter.value}`
    }
    const res = await authedFetch(url)
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to load feedback' }))
      throw new Error(formatApiError(err, 'Failed to load feedback'))
    }
    const data = await res.json()
    feedbackList.value = data.results || data
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await initAuth()
  if (!isStaff.value && !isSuperuser.value) {
    loading.value = false
    return
  }
  await loadFeedback()
})

const openDetailModal = (item: FeedbackItem) => {
  viewingFeedback.value = item
  modalStatus.value = item.status
  modalNotes.value = item.admin_notes || ''
  modalError.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  viewingFeedback.value = null
}

const handleUpdate = async () => {
  if (!viewingFeedback.value) return
  modalError.value = ''
  modalSaving.value = true
  try {
    const res = await authedFetch(
      `${config.public.apiURL}/feedback/${viewingFeedback.value.id}`,
      {
        method: 'PATCH',
        body: JSON.stringify({
          status: modalStatus.value,
          admin_notes: modalNotes.value,
        }),
      },
    )
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Update failed' }))
      throw new Error(formatApiError(err, 'Update failed'))
    }
    successMsg.value = 'Feedback updated successfully!'
    closeModal()
    await loadFeedback()
    setTimeout(() => { successMsg.value = '' }, 3000)
  } catch (e: any) {
    modalError.value = e.message
  } finally {
    modalSaving.value = false
  }
}

const confirmDelete = (item: FeedbackItem) => {
  deletingFeedback.value = item
  showDeleteModal.value = true
}

const handleDelete = async () => {
  if (!deletingFeedback.value) return
  try {
    const res = await authedFetch(
      `${config.public.apiURL}/feedback/${deletingFeedback.value.id}`,
      { method: 'DELETE' },
    )
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Delete failed' }))
      throw new Error(formatApiError(err, 'Delete failed'))
    }
    feedbackList.value = feedbackList.value.filter((f) => f.id !== deletingFeedback.value!.id)
    successMsg.value = 'Feedback deleted successfully!'
    showDeleteModal.value = false
    deletingFeedback.value = null
    setTimeout(() => { successMsg.value = '' }, 3000)
  } catch (e: any) {
    error.value = e.message
    showDeleteModal.value = false
  }
}
</script>
