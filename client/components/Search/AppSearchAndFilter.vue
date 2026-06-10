<template>
    <div class="flex justify-between items-center pb-5">
      <!-- <div class="relative flex items-center w-3/4"> -->
        <div class="relative flex items-center w-full">
        <!-- Input Field -->
        <input
            type="text"
            placeholder="Search..."
            v-model="searchInput"
            @keyup.enter="emitSearchQuery"
            class="shadow appearance-none border rounded-3xl py-2 px-3 pr-24 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-full" />

        <!-- Clear Button -->
        <button
            v-if="searchInput"
            @click="clearSearch"
            class="absolute inset-y-0 right-[80px] px-2 text-gray-400 hover:text-gray-600 font-bold">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>

        <!-- Search Button -->
        <button
            @click="emitSearchQuery"
            class="absolute inset-y-0 right-0 px-4 py-2 bg-red-400 hover:bg-white hover:text-red-400 border-l text-white font-bold rounded-r-3xl">
            Search
        </button>
    </div>
         <!-- <AppFilter @query-generated="handleQueryGenerated"/> -->
    </div>
</template>


<script>
export default {
  data() {
    return {
      searchInput: '',
      emitInput: ''
    };
  },
  methods: {
    emitSearchQuery() {
      if (this.searchInput == '') {
        this.emitInput = '*';
      } else {
        this.emitInput = this.searchInput;
      }
      this.$emit('update-search', this.emitInput);
    },
    clearSearch() {
      this.searchInput = '';
      this.$emit('update-search', '*');
    },
    handleQueryGenerated(queryBody) {
      this.$emit('query-passed', queryBody);
    }
  }
}
</script>
