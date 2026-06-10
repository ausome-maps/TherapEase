<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <NuxtLink to="/" class="flex justify-center">
          <img class="h-8" src="/assets/images/logo_horizontal_1.png" alt="Ausome Maps">
        </NuxtLink>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">Complete Your Profile</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Please fill in your details to finish setting up your account
        </p>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
        {{ success }}
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label for="firstName" class="block text-sm font-medium text-gray-700">First Name</label>
          <input id="firstName" v-model="firstName" type="text" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
        </div>
        <div>
          <label for="lastName" class="block text-sm font-medium text-gray-700">Last Name</label>
          <input id="lastName" v-model="lastName" type="text" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
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

        <button type="submit" :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-white bg-red-400 hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 disabled:opacity-50">
          <span v-if="loading" class="inline-block animate-spin mr-2">&#9696;</span>
          {{ loading ? 'Saving...' : 'Save Profile' }}
        </button>
      </form>

      <div class="flex justify-between text-sm">
        <NuxtLink to="/" class="text-gray-500 hover:text-gray-700">Skip for now</NuxtLink>
        <button @click="handleLogout" class="text-gray-500 hover:text-gray-700">Sign out</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const firstName = ref('')
const lastName = ref('')
const contactNumber = ref('')
const address = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const router = useRouter()
const { updateProfile, logout } = useAuth()

const handleSubmit = async () => {
  error.value = ''
  success.value = ''
  loading.value = true
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
    setTimeout(() => router.push('/'), 1500)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>
