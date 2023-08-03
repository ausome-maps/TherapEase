// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
            apiURL: ""
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
            watch:{
                usePolling:true
            },
            hmr: {
                 clientPort: 24600,
                 port: 24600
            }
        }  
    },
    components: [
        {
          path: '~/components', // will get any components nested in let's say /components/test too
          pathPrefix: false,
        },
      ]
    
    
    // vue: {  
    //     compilerOptions: {
    //         isCustomElement: (tag: string) => tag.startsWith('App'),
    //     },
    //   }
})
