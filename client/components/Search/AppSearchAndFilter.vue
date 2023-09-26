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
            class="shadow appearance-none border rounded-3xl py-2 px-3 pr-20 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-full" />

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
    handleQueryGenerated(queryBody) {
      this.$emit('query-passed', queryBody);
    }
  }
}
</script>
