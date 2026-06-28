<template>
  <article
    class="relative overflow-hidden w-full min-h-[180px] sm:min-h-[250px] bg-white rounded-xl shadow-sm hover:shadow-lg transition-shadow duration-300"
    role="article"
    :aria-label="facilityData.properties.placename"
    @mouseenter="emit('facility-hovered', facilityData.id)"
    @mouseleave="emit('facility-unhovered', facilityData.id)"
  >
    <NuxtLink :to="`/details-page?id=${facilityData.id}`" class="block">
      <div class="relative h-[180px] sm:h-[220px] overflow-hidden rounded-t-xl bg-gray-200">
        <div v-if="imageLoading" class="animate-pulse absolute inset-0 bg-gray-200" />
        <img
          v-show="!imageError && !imageLoading"
          class="object-cover w-full h-full transition-opacity duration-300"
          :class="{ 'opacity-0': imageLoading, 'opacity-100': !imageLoading }"
          :src="imageSource"
          :alt="facilityData.properties.placename"
          @load="onImageLoad"
          @error="onImageError"
        />
        <div
          v-if="imageError"
          class="absolute inset-0 flex items-center justify-center bg-gray-100 text-gray-400 text-sm"
        >
          <span>No image available</span>
        </div>
      </div>
    </NuxtLink>
    <div class="px-4 pb-4 pt-3 space-y-1.5">
      <NuxtLink :to="`/details-page?id=${facilityData.id}`">
        <h5 class="font-semibold text-gray-900 text-sm sm:text-base line-clamp-2 leading-tight">
          {{ facilityData.properties.placename }}
        </h5>
      </NuxtLink>
      <p
        v-if="facilityData.properties.address"
        class="text-xs text-gray-500 line-clamp-1"
      >
        {{ facilityData.properties.address }}
      </p>
      <p
        v-if="activeServiceCount > 0"
        class="text-xs text-gray-500"
      >
        {{ activeServiceCount }} intervention{{ activeServiceCount !== 1 ? 's' : '' }} on offer
      </p>
      <AppAccBadge
        v-if="hasAccreditation"
        :accreditation="facilityData.properties.accreditation"
      />
    </div>
  </article>
</template>

<script setup>
import { ref, computed } from 'vue'
import placeholder from 'assets/images/ausome_placeholder_notext_1.png'

const props = defineProps({
  facilityData: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['facility-hovered', 'facility-unhovered'])

const image_placeholder = placeholder
const imageLoading = ref(true)
const imageError = ref(false)

const imageSource = computed(() => {
  const images = props.facilityData.properties.images
  if (!images || !Array.isArray(images)) return image_placeholder
  const image = images.find((img) => img.img_url && img.img_url.trim() !== '')
  return image ? image.img_url : image_placeholder
})

const activeServiceCount = computed(() => {
  const services = props.facilityData.properties.services_offered
  if (!services) return 0
  return Object.values(services).filter((s) => {
    const mode = s.mode
    if (!mode) return false
    return (mode.teletherapy || 0) > 0 || (mode.onsite || 0) > 0 || (mode.home_service || 0) > 0
  }).length
})

const hasAccreditation = computed(() => {
  const acc = props.facilityData.properties.accreditation
  if (!acc) return false
  return acc.paot === 1 || acc.pasp === 1
})

function onImageLoad() {
  imageLoading.value = false
  imageError.value = false
}

function onImageError() {
  imageLoading.value = false
  imageError.value = true
}
</script>
