<template>
  <div class="relative z-1 w-full flex flex-col justify-center rounded">
    <div :class="{ 'justify-center': !showMap }" class="flex flex-col sm:flex-row h-[100%] min-h-[800px] gap-4">

      <!-- Content Section -->
      <div class="w-full lg:max-w-[850px] xl:max-w-[1100px] flex-grow">
        <ClientOnly>
          <!-- Search and Header Section -->
          <div class="px-5 pb-4 sticky top-0 z-50 bg-white">
            <AppSearchAndFilter @update-search="handleSearch" />
            <AppListingHeader :show-map="showMap" @hide-map="showMap = false" @show-map="showMap = true"
              :view-mode="viewMode" @change-view-mode="handleChangeViewMode" :facilitiesLength="totalResults"
              :filteredFacilitiesLength="currentPageResults" />
          </div>

          <!-- No Results Section -->
          <div v-if="currentPageResults === 0" class="w-full text-center py-10">
            <h2 class="text-xl font-semibold">No results found</h2>
            <p>Try adjusting your search or filter criteria.</p>
          </div>

          <!-- Listings View -->
          <AppCardList v-if="viewMode === 'card'" :facilities="data" :filteredFacilities="data" />
          <AppListView v-else-if="viewMode === 'list'" :facilities="data" :filteredFacilities="data" />

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="flex justify-center my-4">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="px-4 py-2 bg-gray-200 text-gray-700 border rounded-l-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed mr-2">Previous</button>

            <template v-for="page in totalPages">
              <button v-if="page === currentPage" class="px-4 py-2 bg-gray-300 text-gray-700 border mx-1">{{ page
              }}</button>
              <button v-else @click="goToPage(page)"
                class="px-4 py-2 bg-gray-200 text-gray-700 border hover:bg-red-300 mx-1">{{ page }}</button>
            </template>

            <button @click="nextPage" :disabled="currentPage === totalPages"
              class="px-4 py-2 bg-gray-200 text-gray-700 border rounded-r-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed ml-2">Next</button>
          </div>
        </ClientOnly>
      </div>

      <!-- Map Section -->
      <div v-if="showMap" class="w-full lg:flex-grow mr-8 h-[99vh] sticky top-5 z-10">
        <AppMap :coordinates="coordinates" :latitude="14.621071" :longitude="121.0073" />
      </div>
    </div>
  </div>
  <div class="h-[100px]"></div>
</template>

<script>
import data from '../components/facility-data.json'

export default {
  data() {
    return {
      searchQuery: '*',
      data: data.features,
      viewMode: 'card',
      showMap: true,
      isMobile: false,
      filteredData: [],
      error: null,
      isFetching: false,
      paginationSize: 20,
      totalResults: 0,
      currentPageResults: 0,
      currentPage: 1,
      totalPages: Math.ceil(this.totalResults / this.paginationSize),
      coordinates: [],  // New coordinates array
      selectedService: 'orthoses'
    };
  },

  async mounted() {
    this.checkIfMobile();
    window.addEventListener('resize', this.checkIfMobile);
    await this.$nextTick();
    this.searchQuery = this.$route.query.search || '*';
    this.currentPage = Number(this.$route.query.page) || 1;
    this.$router.push({ query: { search: this.searchQuery, page: this.currentPage } });
    await this.handleSearch();
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.checkIfMobile);
  },

  watch: {
    searchQuery(newQuery) {
      this.$router.push({ query: { search: newQuery, page: this.currentPage } });
    },
  },

  methods: {
    checkIfMobile() {
      this.isMobile = window.visualViewport.width <= 768;
    },

    updateURL() {
      this.$router.push({ query: { search: this.searchQuery, page: this.currentPage } });
    },

    handleChangeViewMode(newViewMode) {
      this.viewMode = newViewMode;
    },

    async getMapCoordinates() {
      console.log(this.data.hits)
      if (this.data && Array.isArray(this.data.hits)) {
        return this.data.hits.map(facility => {
          const name = facility._source.properties.placename
          const coords = facility._source.geometry.coordinates;
          return [coords[1], coords[0]]; // returns [latitude, longitude]
        });
      }
      return [];
    },

    async handleSearch(query = this.searchQuery) {
      this.searchQuery = query;
      try {
        await this.fetchSearch();
        this.data = this.filteredData.hits;
        this.totalResults = this.data.total.value;
        this.totalPages = Math.ceil(this.totalResults / this.paginationSize);
        this.currentPageResults = Math.min(this.paginationSize, this.data.hits.length);

        // Set the coordinates array after the data has been fetched
        this.coordinates = await this.getMapCoordinates();
      } catch (error) {
        this.totalResults = 0;
        this.currentPageResults = 0;
        this.coordinates = [];  // Reset the coordinates if there's an error
      }
    },
    async fetchSearch() {
  const startIndex = (this.currentPage - 1) * this.paginationSize;



  const queryParameters = {
    q: this.searchQuery,
    size: this.paginationSize,
    from: startIndex};

  const queryString = new URLSearchParams(queryParameters).toString();
  const url = `${this.$config.search}?${queryString}`;

  try {
    const response = await fetch(url);

    // Check if the response is successful
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    this.filteredData = data;
    this.isFetching = false;
    this.error = null;
  } catch (error) {
    this.filteredData = null;
    this.error = error.message;
    this.isFetching = false;
  }
},

    goToPage(pageNumber) {
      this.currentPage = pageNumber;
      this.handleSearch();
      this.updateURL();
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.handleSearch();
        this.updateURL();
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.handleSearch();
        this.updateURL();
      }
    }
  }
}
</script>
