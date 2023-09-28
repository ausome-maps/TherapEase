<template>
  <nav class="bg-white shadow border-gray-200 dark:bg-gray-900">
        <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
            <a href='search-page' class="flex items-center">
                <img class="h-5" :src="image_placeholder" alt="">
                <!-- <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Ausome Maps</span> -->
            </a>
    </div>
</nav>
</template>
<script>
import placeholder from "assets/images/logo_horizontal.png"
export default {
  data() {
    return {
      image_placeholder: placeholder
    }
  },
  mounted(){
    let recaptchaScript = document.createElement('script')
      recaptchaScript.setAttribute('src', this.$config.googleTagManager)
      document.head.appendChild(recaptchaScript)
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-E1HY2D8NC8');
  }
      }
</script>