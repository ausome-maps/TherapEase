<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-6">
        <NuxtLink to="/" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back to Home
        </NuxtLink>
        <h2 class="mt-2 text-2xl sm:text-3xl font-bold text-gray-900">Your Profile</h2>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-6">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm mb-6">
        {{ success }}
      </div>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
        <p class="mt-4 text-gray-600">Loading profile...</p>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Sidebar -->
        <div class="lg:col-span-1 space-y-6">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Account</h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Status</span>
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="currentUser?.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                  {{ currentUser?.active ? 'Active' : 'Inactive' }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Login count</span>
                <span class="text-gray-900 font-medium">{{ loginCount }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Member since</span>
                <span class="text-gray-900">{{ createdAt }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Role</span>
                <span class="text-gray-900">{{ isStaff ? 'Staff' : 'User' }}</span>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Actions</h3>
            <nav class="space-y-2">
              <button type="button" @click="showPasswordChange = !showPasswordChange"
                class="w-full text-left block px-3 py-2 rounded-lg text-sm text-gray-700 hover:bg-gray-100"
                :class="{ 'bg-red-50 text-red-600': showPasswordChange }">
                Change Password
              </button>
              <NuxtLink v-if="isStaff" to="/users"
                class="block px-3 py-2 rounded-lg text-sm text-gray-700 hover:bg-gray-100">
                Manage Users
              </NuxtLink>
            </nav>
          </div>
        </div>

        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Edit Profile Form -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-6">Edit Profile</h3>
            <form class="space-y-5" @submit.prevent="handleSubmit">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                <div>
                  <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
                  <input id="firstName" v-model="firstName" type="text"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
                </div>
                <div>
                  <label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
                  <input id="lastName" v-model="lastName" type="text"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
                </div>
              </div>
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                <input id="email" v-model="email" type="email" disabled
                  class="mt-1 block w-full px-3 py-2 border border-gray-200 bg-gray-50 rounded-lg text-gray-500 cursor-not-allowed">
              </div>
              <div>
                <label for="contactNumber" class="block text-sm font-medium text-gray-700">Contact Number</label>
                <input id="contactNumber" v-model="contactNumber" type="text"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
              </div>
              <div>
                <label for="address" class="block text-sm font-medium text-gray-700">Address</label>
                <textarea id="address" v-model="address" rows="3"
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400"></textarea>
              </div>
              <button type="submit" :disabled="saving"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-red-400 hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 disabled:opacity-50">
                <span v-if="saving" class="inline-block animate-spin mr-2">&#9696;</span>
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </form>
          </div>

          <!-- Change Password -->
          <div v-if="showPasswordChange" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-6">Change Password</h3>
            <div v-if="passwordError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-4">
              {{ passwordError }}
            </div>
            <div v-if="passwordSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm mb-4">
              {{ passwordSuccess }}
            </div>
            <form @submit.prevent="handleChangePassword" class="space-y-4">
              <div>
                <label for="currentPassword" class="block text-sm font-medium text-gray-700">Current Password</label>
                <input id="currentPassword" v-model="currentPassword" type="password" required
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
              </div>
              <div class="grid grid-cols-1 gap-4">
                <div>
                  <label for="newPassword" class="block text-sm font-medium text-gray-700">New Password</label>
                  <input id="newPassword" v-model="newPassword" type="password" required minlength="8"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
                </div>
                <div>
                  <label for="confirmNewPassword" class="block text-sm font-medium text-gray-700">Confirm New Password</label>
                  <input id="confirmNewPassword" v-model="confirmNewPassword" type="password" required minlength="8"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
                </div>
              </div>
              <button type="submit" :disabled="changingPassword"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-red-400 hover:bg-red-500 focus:outline-none disabled:opacity-50">
                <span v-if="changingPassword" class="inline-block animate-spin mr-2">&#9696;</span>
                {{ changingPassword ? 'Updating...' : 'Update Password' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const { currentUser, updateProfile, changePassword, isStaff, initAuth, fetchProfile } = useAuth()

const firstName = ref('')
const lastName = ref('')
const email = ref('')
const contactNumber = ref('')
const address = ref('')
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const success = ref('')

const showPasswordChange = ref(false)
const currentPassword = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const changingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

const loginCount = computed(() => currentUser.value?.login_count ?? 0)
const createdAt = computed(() => {
  const expiry = currentUser.value?.account_expiry
  if (!expiry) return 'N/A'
  const date = new Date(expiry)
  date.setFullYear(date.getFullYear() - 10)
  return date.toLocaleDateString()
})

const populateFields = () => {
  const user = currentUser.value
  if (user) {
    firstName.value = user.first_name || ''
    lastName.value = user.last_name || ''
    email.value = user.email || ''
    const meta = user.other_metadata as Record<string, unknown> | null
    if (meta) {
      contactNumber.value = (meta.contact_nos as string) || ''
      address.value = (meta.address as string) || ''
    }
  }
}

onMounted(async () => {
  await initAuth()
  if (!currentUser.value) {
    await fetchProfile()
  }
  populateFields()
  loading.value = false
})

const handleSubmit = async () => {
  error.value = ''
  success.value = ''
  saving.value = true
  try {
    await updateProfile({
      first_name: firstName.value,
      last_name: lastName.value,
      other_metadata: {
        contact_nos: contactNumber.value,
        address: address.value,
      },
    })
    success.value = 'Profile updated successfully!'
    setTimeout(() => { success.value = '' }, 3000)
  } catch (e: any) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

const handleChangePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = ''

  if (newPassword.value !== confirmNewPassword.value) {
    passwordError.value = 'Passwords do not match'
    return
  }

  if (newPassword.value.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
    return
  }

  changingPassword.value = true
  try {
    await changePassword(currentPassword.value, newPassword.value, confirmNewPassword.value)
    passwordSuccess.value = 'Password changed successfully!'
    currentPassword.value = ''
    newPassword.value = ''
    confirmNewPassword.value = ''
    setTimeout(() => {
      passwordSuccess.value = ''
      showPasswordChange.value = false
    }, 2000)
  } catch (e: any) {
    passwordError.value = e.message
  } finally {
    changingPassword.value = false
  }
}
</script>
