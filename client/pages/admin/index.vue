<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900">Dashboard</h2>
      <p class="mt-1 text-sm text-gray-600">Overview of the TherapEase platform</p>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
      <p class="mt-4 text-gray-600">Loading stats...</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500">Total Users</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.users.total ?? '—' }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500">Active Users</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.users.active ?? '—' }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500">Staff / Superusers</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ (stats?.users.staff ?? 0) + (stats?.users.superusers ?? 0) }}
            </p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500">Organizations</p>
            <p class="text-2xl font-bold text-gray-900">{{ stats?.organizations ?? '—' }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500">Feedback</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ stats?.feedback?.total ?? '—' }}
              <span v-if="stats?.feedback?.new" class="text-sm font-normal text-red-500 ml-1">
                ({{ stats.feedback.new }} new)
              </span>
            </p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <div>
            <p class="text-sm text-gray-500">Facility Submissions</p>
            <p class="text-2xl font-bold text-gray-900">
              {{ stats?.submissions?.total ?? '—' }}
              <span v-if="stats?.submissions?.new" class="text-sm font-normal text-red-500 ml-1">
                ({{ stats.submissions.new }} new)
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Quick Actions</h3>
      <div class="flex flex-wrap gap-3">
        <NuxtLink
          to="/admin/users"
          class="inline-flex items-center gap-2 px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm font-medium"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
          Manage Users
        </NuxtLink>
        <NuxtLink
          to="/admin/feedback"
          class="inline-flex items-center gap-2 px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm font-medium"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          Manage Feedback
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

definePageMeta({ layout: 'admin' })

interface AdminStats {
  users: {
    total: number
    active: number
    staff: number
    superusers: number
  }
  organizations: number
  feedback: {
    total: number
    new: number
  }
  submissions: {
    total: number
    new: number
  }
}

const { fetchAdminStats } = useAuth()

const stats = ref<AdminStats | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    stats.value = await fetchAdminStats()
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>
