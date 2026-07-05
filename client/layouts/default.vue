<template>
    <div>
      <AppHeader />
      <slot />
      <AppFooter />
    </div>
</template>

<script setup lang="ts">
const route = useRoute()
const analytics = useAnalytics()

watch(() => route.path, (newPath) => {
  analytics.trackPageVisit(newPath)
}, { immediate: true })
</script>
