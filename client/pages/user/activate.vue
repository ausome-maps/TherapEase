<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="max-w-md w-full text-center space-y-6">
      <NuxtLink to="/" class="flex justify-center">
        <img class="h-8" src="/assets/images/logo_horizontal_1.png" alt="Ausome Maps">
      </NuxtLink>

      <div v-if="loading" class="py-8">
        <div class="inline-block animate-spin text-4xl text-red-400">&#9696;</div>
        <p class="mt-4 text-gray-600">Activating your account...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        <h2 class="text-xl font-bold mb-2">Activation Failed</h2>
        <p>{{ error }}</p>
        <p class="mt-4">
          <NuxtLink to="/register" class="font-medium text-red-400 hover:text-red-500">Try registering again</NuxtLink>
        </p>
      </div>

      <div v-else-if="activated" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
        <h2 class="text-xl font-bold mb-2">Account Activated!</h2>
        <p>Your account has been successfully activated.</p>
        <NuxtLink to="/login?activated=true"
          class="mt-4 inline-block px-6 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500">
          Continue to Sign In
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const activated = ref(false)

const { activate } = useAuth()

onMounted(async () => {
  const uid = route.params.uid
  const token = route.params.token

  if (!uid || !token) {
    error.value = 'Invalid activation link'
    loading.value = false
    return
  }

  try {
    await activate(uid, token)
    activated.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>
