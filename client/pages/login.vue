<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <NuxtLink to="/" class="flex justify-center">
          <img class="h-8" src="/assets/images/logo_horizontal_1.png" alt="Ausome Maps">
        </NuxtLink>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">Sign in to your account</h2>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
        {{ error }}
      </div>

      <div v-if="successMessage" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
        {{ successMessage }}
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <input id="email" v-model="email" type="email" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input id="password" v-model="password" type="password" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-red-400 focus:border-red-400">
        </div>

        <button type="submit" :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-white bg-red-400 hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 disabled:opacity-50">
          <span v-if="loading" class="inline-block animate-spin mr-2">&#9696;</span>
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>

        <div class="relative my-4">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-gray-50 text-gray-500">or continue with</span>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <a :href="googleLoginUrl"
            class="flex justify-center items-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white hover:bg-gray-50 text-sm font-medium text-gray-700">
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Google
          </a>
          <a :href="facebookLoginUrl"
            class="flex justify-center items-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white hover:bg-gray-50 text-sm font-medium text-gray-700">
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="#1877F2">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
            Facebook
          </a>
        </div>
      </form>

      <div class="text-center">
        <p class="text-sm text-gray-600">
          Don't have an account?
          <NuxtLink to="/register" class="font-medium text-red-400 hover:text-red-500">Register here</NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const successMessage = ref('')
const router = useRouter()
const route = useRoute()

const { login } = useAuth()
const config = useRuntimeConfig()
const googleLoginUrl = `${config.public.apiURL}/social/login/google-oauth2/?next=/users/social/complete/`
const facebookLoginUrl = `${config.public.apiURL}/social/login/facebook/?next=/users/social/complete/`

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    router.push('/complete-profile')
  }
  if (route.query.activated) {
    successMessage.value = 'Your account has been activated! Please sign in.'
  }
})

const handleSubmit = async () => {
  error.value = ''
  loading.value = true
  try {
    await login(email.value, password.value)
    router.push('/complete-profile')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
