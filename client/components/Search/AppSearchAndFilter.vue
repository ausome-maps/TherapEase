<script setup>
import { ref } from 'vue'

const emit = defineEmits(['update-search', 'query-passed'])

const searchInput = ref('')

function emitSearchQuery() {
  if (searchInput.value === '') {
    emit('update-search', '*')
  } else {
    emit('update-search', searchInput.value)
  }
}

function clearSearch() {
  searchInput.value = ''
  emit('update-search', '*')
}

function handleQueryGenerated(queryBody) {
  emit('query-passed', queryBody)
}
</script>

<template>
  <div class="flex items-stretch gap-2 pb-3 sm:pb-5">
    <div class="relative flex items-center flex-1">
      <input
        type="text"
        placeholder="Search..."
        v-model="searchInput"
        @keyup.enter="emitSearchQuery"
        class="shadow appearance-none border rounded-3xl py-2 px-3 pr-24 sm:pr-24 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-full text-sm sm:text-base"
      />

      <button
        v-if="searchInput"
        @click="clearSearch"
        class="absolute inset-y-0 right-[80px] px-2 text-gray-400 hover:text-gray-600 font-bold"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>

      <button
        @click="emitSearchQuery"
        class="absolute inset-y-0 right-0 px-4 py-2 bg-red-400 hover:bg-white hover:text-red-400 border-l text-white font-bold rounded-r-3xl text-sm sm:text-base"
      >
        Search
      </button>
    </div>
    <div class="flex-shrink-0">
      <AppFilter @query-generated="handleQueryGenerated" />
    </div>
  </div>
</template>
