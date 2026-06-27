import tailwindcss from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  css: ['~/assets/css/input.css'],
  runtimeConfig: {
    public: {
      apiURL: process.env.NUXT_PUBLIC_API_URL || "http://localhost:9001",
      geocodeURL: process.env.NUXT_PUBLIC_API_URL + "/geocode" || "http://localhost:9001/geocode",
      searchURL: process.env.NUXT_PUBLIC_API_URL + "/search" || "http://localhost:9001/search",
      baseURL: process.env.NUXT_PUBLIC_UI_URL || "http://localhost:9002",
      facilitiesURL:  process.env.NUXT_PUBLIC_API_URL + "/facilities/search" || "http://localhost:9001/facilities/search",
      feedbackURL: process.env.NUXT_PUBLIC_FEEDBACK_URL || "https://forms.gle/Yo4zMgBXXfAL7vyS6",
      googleTagManager: process.env.GOOGLE_TAG_MANAGER || "https://www.googletagmanager.com/gtag/js?id=G-E1HY2D8NC8",
      authURL: process.env.NUXT_PUBLIC_API_URL + "/auth" || "http://localhost:9001/auth",
    }
  },
  routeRules: {
    '/geocode': {
      proxy: { to: "http://localhost:9001/geocode" }
    }
  },
  modules: [],
  vite: {
    plugins: [tailwindcss()],
    server: {
      watch: {
        usePolling: true
      },
      hmr: {
        clientPort: 24600,
        port: 24600
      }
    }
  },
  components: [
    {
      path: '~/components',
      pathPrefix: false
    }
  ]
})
