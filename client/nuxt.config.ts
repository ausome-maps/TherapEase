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
      copyrightYear: process.env.NUXT_PUBLIC_COPYRIGHT_YEAR || "2023",
      authEnabled: process.env.FEATURE_AUTH_ENABLED !== '0',
      registrationEnabled: process.env.FEATURE_REGISTRATION_ENABLED !== '0',
    }
  },
  routeRules: {
    '/geocode': {
      proxy: { to: "http://localhost:9001/geocode" }
    }
  },
  modules: ['@vite-pwa/nuxt'],
  pwa: {
    registerType: 'autoUpdate',
    manifest: {
      name: 'TherapEase',
      short_name: 'TherapEase',
      description: 'Find special education facilities and services in the Philippines',
      theme_color: '#f87171',
      background_color: '#ffffff',
      display: 'standalone',
      orientation: 'portrait-primary',
      start_url: '/',
      icons: [
        { src: '/pwa-192x192.png', sizes: '192x192', type: 'image/png' },
        { src: '/pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
      ],
    },
    workbox: {
      globPatterns: ['**/*.{js,css,html,png,svg,woff2}'],
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/.*\.tile\.openstreetmap\.org\/.*/,
          handler: 'CacheFirst',
          options: {
            cacheName: 'map-tiles',
            expiration: { maxEntries: 200, maxAgeSeconds: 30 * 24 * 60 * 60 },
          },
        },
        {
          urlPattern: /\/api\/.*/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-calls',
            networkTimeoutSeconds: 5,
            expiration: { maxEntries: 100, maxAgeSeconds: 5 * 60 },
          },
        },
      ],
    },
    client: {
      installPrompt: true,
    },
    devOptions: {
      enabled: true,
      type: 'module',
    },
  },
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
