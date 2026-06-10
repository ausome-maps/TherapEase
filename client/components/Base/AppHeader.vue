<template>
  <nav class="bg-white shadow border-gray-200 dark:bg-gray-900 relative z-50">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <a href='/' class="flex items-center">
        <img class="h-5" :src="image_placeholder" alt="">
      </a>
      <div class="flex items-center gap-2">
        <template v-if="mounted">
          <template v-if="isLoggedIn">
            <span class="text-sm text-gray-600 hidden sm:inline">{{ userEmail }}</span>
            <button type="button" @click="handleLogout" class="text-sm text-red-400 hover:text-red-600 border border-red-400 px-3 py-1 rounded-full hover:bg-red-50 cursor-pointer">
              Sign out
            </button>
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
  </nav>
</template>
<script>
import placeholder from "assets/images/logo_horizontal_1.png"

export default {
  data() {
    return {
      image_placeholder: placeholder,
      mounted: false,
      isLoggedIn: false,
      userEmail: '',
    }
  },
  mounted() {
    this.mounted = true
    this.checkAuth()
    window.addEventListener('storage', this.checkAuth)

    let recaptchaScript = document.createElement('script')
    recaptchaScript.setAttribute('src', this.$config.public.googleTagManager)
    document.head.appendChild(recaptchaScript)
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-E1HY2D8NC8');
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.checkAuth)
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('access_token')
      this.isLoggedIn = !!token
      if (token) {
        this.userEmail = localStorage.getItem('user_email') || ''
      }
    },
    handleLogout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_email')
      this.isLoggedIn = false
      this.userEmail = ''
      window.location.href = '/'
    },
  }
}
</script>
