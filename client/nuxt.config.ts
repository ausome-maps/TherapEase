// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
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
    // vue: {  
    //     compilerOptions: {
    //         isCustomElement: (tag: string) => tag.startsWith('App'),
    //     },
    //   }
})
