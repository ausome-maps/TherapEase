<template>
  <div class="min-h-screen flex items-center justify-center">
    <p class="text-gray-500">Redirecting to search...</p>
  </div>
</template>

<script setup>
const router = useRouter()
onMounted(() => {
  router.replace({ path: '/', query: router.currentRoute.value.query })
})
</script>

<script>
import { onMounted } from 'vue'
export default {}
</script>
