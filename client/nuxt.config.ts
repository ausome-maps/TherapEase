// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
    runtimeConfig: {
        public: {
          apiURL: process.env.NUXT_API_URL || "https://api.find.ausomemaps.org",
          geocode: "http://localhost:9001/geocode",
          search: "https://api.find.ausomemaps.org/search",
          baseURL: "http://localhost:9002",
          facilities:  "https://api.find.ausomemaps.org/facilities",
          feedbackUrl: process.env.FEEDBACK_FORM,
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
