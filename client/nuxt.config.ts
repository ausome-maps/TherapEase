// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
    runtimeConfig: {
        public: {
          apiURL: process.env.NUXT_PUBLIC_API_URL || "http://localhost:9001",
          geocodeURL: process.env.NUXT_PUBLIC_API_URL + "/geocode" || "http://localhost:9001/geocode",
          searchURL: process.env.NUXT_PUBLIC_API_URL + "/search" || "http://localhost:9001/search",
          baseURL: process.env.NUXT_PUBLIC_UI_URL || "http://localhost:9002",
          facilitiesURL:  process.env.NUXT_PUBLIC_API_URL + "/facilities" || "http://localhost:9001/facilities",
          feedbackURL: process.env.NUXT_PUBLIC_FEEDBACK_URL || "https://forms.gle/Yo4zMgBXXfAL7vyS6",
          googleTagManager: process.env.GOOGLE_TAG_MANAGER || "https://www.googletagmanager.com/gtag/js?id=G-E1HY2D8NC8", 
        }
      },
      routeRules: {
        '/geocode': {
          proxy: { to: "http://localhost:9001/geocode" }
        }
      },
      modules: [
        '@nuxtjs/tailwindcss'
      ],
      tailwindcss: {
        cssPath: '~/assets/css/input.css'
      },
      vite: {
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
