// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    
    runtimeConfig: {
        public: {
          apiURL: process.env.NUXT_API_URL || "http://localhost:9001",
          geocode: "http://localhost:9001/geocode",
          search: "http://localhost:9001/search",
          baseURL: "http://localhost:9002/search-page"
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
