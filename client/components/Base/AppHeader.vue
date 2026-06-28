<template>
  <nav class="bg-white shadow border-gray-200 dark:bg-gray-900 relative z-50">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto px-3 py-3 sm:p-4">
      <a href='/' class="flex items-center">
        <img class="h-4 sm:h-5" :src="image_placeholder" alt="">
      </a>
      <button
        class="sm:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-500 hover:text-red-400 hover:bg-gray-100 focus:outline-none"
        @click="mobileMenuOpen = !mobileMenuOpen"
        aria-label="Toggle menu"
      >
        <svg v-if="!mobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <div class="hidden sm:flex items-center gap-2">
        <template v-if="mounted && authEnabled">
          <template v-if="isAuthenticated">
            <div class="relative">
              <button @click="showDropdown = !showDropdown"
                class="flex items-center gap-2 text-sm text-gray-600 hover:text-red-400 px-3 py-1 border border-gray-300 rounded-full hover:border-red-400 cursor-pointer">
                <span class="hidden sm:inline">{{ userEmail }}</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div v-if="showDropdown"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
                @click="showDropdown = false">
                <NuxtLink to="/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  Profile
                </NuxtLink>
                <NuxtLink v-if="isStaff || isSuperuser" to="/admin"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  Admin
                </NuxtLink>
                <hr class="my-1 border-gray-200">
                <button @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-red-500 hover:bg-gray-100">
                  Sign out
                </button>
              </div>
            </div>
          </template>
          <template v-else>
            <NuxtLink to="/login" class="text-sm text-gray-600 hover:text-red-400 px-3 py-1 border border-gray-300 rounded-full hover:border-red-400">
              Sign in
            </NuxtLink>
            <NuxtLink to="/register" class="text-sm text-white bg-red-400 hover:bg-red-500 px-3 py-1 rounded-full">
              Register
            </NuxtLink>
          </template>
        </template>
      </div>
    </div>
    <transition name="mobile-slide">
      <div v-if="mobileMenuOpen && mounted && authEnabled" class="sm:hidden border-t border-gray-200 bg-white dark:bg-gray-900">
        <div class="px-3 py-2 space-y-1">
          <template v-if="isAuthenticated">
            <div class="px-3 py-2 text-sm text-gray-500 border-b border-gray-100">{{ userEmail }}</div>
            <NuxtLink to="/profile" @click="mobileMenuOpen = false"
              class="block px-3 py-3 text-sm text-gray-700 hover:bg-gray-100 rounded-lg">
              Profile
            </NuxtLink>
            <NuxtLink v-if="isStaff || isSuperuser" to="/admin" @click="mobileMenuOpen = false"
              class="block px-3 py-3 text-sm text-gray-700 hover:bg-gray-100 rounded-lg">
              Admin
            </NuxtLink>
            <button @click="handleLogout"
              class="block w-full text-left px-3 py-3 text-sm text-red-500 hover:bg-gray-100 rounded-lg">
              Sign out
            </button>
          </template>
          <template v-else>
            <NuxtLink to="/login" @click="mobileMenuOpen = false"
              class="block px-3 py-3 text-sm text-gray-700 hover:bg-gray-100 rounded-lg">
              Sign in
            </NuxtLink>
            <NuxtLink to="/register" @click="mobileMenuOpen = false"
              class="block px-3 py-3 text-sm text-red-500 hover:bg-gray-100 rounded-lg font-medium">
              Register
            </NuxtLink>
          </template>
        </div>
      </div>
    </transition>
  </nav>
</template>
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import placeholder from "assets/images/logo_horizontal_1.png"

const config = useRuntimeConfig()
const authEnabled = computed(() => config.public.authEnabled)
const image_placeholder = placeholder
const mounted = ref(false)
const showDropdown = ref(false)
const mobileMenuOpen = ref(false)

const { isAuthenticated, currentUser, isStaff, isSuperuser, initAuth, logout } = useAuth()

const userEmail = computed(() => {
  return currentUser.value?.email || localStorage.getItem('user_email') || ''
})

const handleLogout = () => {
  logout()
  showDropdown.value = false
  mobileMenuOpen.value = false
  window.location.href = '/'
}

onMounted(async () => {
  mounted.value = true

  if (isAuthenticated.value) {
    await initAuth()
  }

  let recaptchaScript = document.createElement('script')
  recaptchaScript.setAttribute('src', config.public.googleTagManager)
  document.head.appendChild(recaptchaScript)
  window.dataLayer = window.dataLayer || [];
  function gtag(){(window.dataLayer as any[]).push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-E1HY2D8NC8');

  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (!target.closest('.relative')) {
    showDropdown.value = false
  }
}
</script>
<style scoped>
.mobile-slide-enter-active,
.mobile-slide-leave-active {
  transition: all 0.2s ease;
  max-height: 300px;
  overflow: hidden;
}
.mobile-slide-enter-from,
.mobile-slide-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
