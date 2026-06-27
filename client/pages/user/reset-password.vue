<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <NuxtLink to="/" class="flex justify-center">
          <img class="h-8" src="/assets/images/logo_horizontal_1.png" alt="Ausome Maps">
        </NuxtLink>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
          {{ isConfirmMode ? 'Reset Your Password' : 'Forgot Password?' }}
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          {{ isConfirmMode ? 'Enter your new password below.' : 'Enter your email and we\'ll send you a reset link.' }}
        </p>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
        {{ error }}
      </div>
      <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
        {{ success }}
      </div>

      <form v-if="isConfirmMode" class="mt-8 space-y-6" @submit.prevent="handleResetConfirm">
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
        <button type="submit" :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-white bg-red-400 hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 disabled:opacity-50">
          <span v-if="loading" class="inline-block animate-spin mr-2">&#9696;</span>
          {{ loading ? 'Resetting...' : 'Reset Password' }}
        </button>
      </form>

      <form v-else class="mt-8 space-y-6" @submit.prevent="handleResetRequest">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <input id="email" v-model="email" type="email" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
        </div>
        <button type="submit" :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-white bg-red-400 hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 disabled:opacity-50">
          <span v-if="loading" class="inline-block animate-spin mr-2">&#9696;</span>
          {{ loading ? 'Sending...' : 'Send Reset Link' }}
        </button>
      </form>

      <div class="text-center">
        <NuxtLink to="/login" class="text-sm text-gray-500 hover:text-gray-700">Back to Sign In</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const route = useRoute()
const { resetPassword, resetPasswordConfirm } = useAuth()

const email = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const isConfirmMode = computed(() => {
  return !!(route.params?.uid && route.params?.token)
})

const uid = computed(() => (route.params?.uid as string) || '')
const token = computed(() => (route.params?.token as string) || '')

const handleResetRequest = async () => {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await resetPassword(email.value)
    success.value = 'If an account with that email exists, we\'ve sent a password reset link.'
    email.value = ''
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const handleResetConfirm = async () => {
  error.value = ''
  success.value = ''

  if (newPassword.value !== confirmNewPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (newPassword.value.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }

  loading.value = true
  try {
    await resetPasswordConfirm(uid.value, token.value, newPassword.value, confirmNewPassword.value)
    success.value = 'Password has been reset successfully!'
    newPassword.value = ''
    confirmNewPassword.value = ''
    setTimeout(() => {
      window.location.href = '/login'
    }, 2000)
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
