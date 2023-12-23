<template>
    <div v-if="totalPages > 1" class="flex justify-center my-4">
      <button @click="prevPage" :disabled="currentPage === 1" class="px-4 py-2 bg-gray-200 text-gray-700 border rounded-l-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed mr-2">Previous</button>
      <span class="text-lg mx-2">{{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="px-4 py-2 bg-gray-200 text-gray-700 border rounded-r-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed ml-2">Next</button>
    </div>
  </template>

  <script>
  export default {
    props: {
      totalPages: {
        type: Number,
        required: true
      },
      currentPage: {
        type: Number,
        required: true
      }
    },
    methods: {
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.$emit('change-page', this.currentPage + 1);
        }
      },
      prevPage() {
        if (this.currentPage > 1) {
          this.$emit('change-page', this.currentPage - 1);
        }
      }
    }
  }
  </script>
