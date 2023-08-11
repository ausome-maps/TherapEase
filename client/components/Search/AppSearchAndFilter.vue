<template>
    <div class="flex justify-between items-center ">
         <input 
            type="text" 
            placeholder="Search..."
            v-model="searchInput"
            class="shadow appearance-none border rounded-3xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mr-2 w-3/4" />
         <button 
            @click="emitSearchQuery"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Search
         </button>
         <AppFilter />
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
    }
  }
}
</script>
