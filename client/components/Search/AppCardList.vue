<template>
  <div class="flex justify-center w-full">
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-3 sm:gap-4 p-2 sm:p-4 w-full justify-items-center">
      <div v-for="n in skeletonCount" :key="n" class="p-1 sm:p-2 w-full">
        <div class="rounded-xl overflow-hidden bg-gray-100 animate-pulse">
          <div class="h-[220px] bg-gray-200" />
          <div class="px-4 pb-4 pt-3 space-y-2">
            <div class="h-5 bg-gray-200 rounded w-3/4" />
            <div class="h-3 bg-gray-200 rounded w-1/2" />
            <div class="h-3 bg-gray-200 rounded w-1/3" />
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="text-center py-10 w-full">
      <p class="text-gray-500 mb-2">Failed to load facilities.</p>
      <button
        class="px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500 text-sm"
        @click="emit('retry')"
      >
        Retry
      </button>
    </div>

    <div v-else-if="!facilities || facilities.length === 0" class="text-center py-10 w-full">
      <h2 class="text-xl font-semibold text-gray-700">No facilities found</h2>
      <p class="text-gray-500 mt-1">Try adjusting your search or filter criteria.</p>
    </div>

    <div
      v-else
      class="bg-transparent grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-3 sm:gap-4 p-2 sm:p-4 w-full justify-items-center"
    >
      <div
        v-for="facility in facilities"
        :key="facility.id"
        class="transition duration-200 ease-in-out p-1 sm:p-2 transform hover:-translate-y-1 w-full"
      >
        <AppCard
          :facilityData="facility"
          @facility-hovered="(id) => emit('facility-hovered', id)"
          @facility-unhovered="(id) => emit('facility-unhovered', id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  facilities: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['facility-hovered', 'facility-unhovered', 'retry'])

const skeletonCount = computed(() => {
  const count = Array.isArray(props.facilities) ? props.facilities.length : 0
  return Math.max(count, 8)
})
</script>
