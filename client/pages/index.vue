<template>
  <div class="relative z-1 w-full flex top-5 flex-col justify-center rounded">
    <div :class="{ 'justify-center': !showMap }" class="flex flex-col sm:flex-row h-[100%] min-h-[800px] gap-4">

      <!-- Content Section -->
      <div class="w-full lg:max-w-[850px] xl:max-w-[1100px] flex-grow">
        <ClientOnly>
          <!-- Search and Header Section -->
          <div class="px-5 pb-4 sticky top-0 z-50 bg-white">
            <AppSearchAndFilter @update-search="handleSearch" @query-passed="handleQueryPassed" />
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
      <div v-if="showMap" class="w-2/4 lg:flex-grow mr-4 h-[99vh] sticky top-5 z-10">
        <AppMap :coordinates="coordinates" :bounds="bounds" :latitude="center.lat" :longitude="center.lng" />
      </div>
    </div>
  </div>
  <div class="h-[100px]"></div>
</template>

<script>
import L from 'leaflet';
import "leaflet/dist/leaflet.css";

export default {
  data() {
    return {
      searchQuery: '*',
      data: [],
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
      selectedService: 'orthoses',
      filter: [],
      bounds:{
    "_southWest": {
        "lat": 7.054338,
        "lng": -237.179385
    },
    "_northEast": {
        "lat": 18.195933,
        "lng": 125.597421
    }
},
      center:{
    "lat": 12.6251355,
    "lng": -55.790982
},
    };
  },

  async mounted() {
    this.checkIfMobile();

    window.addEventListener('resize', this.checkIfMobile);
    await this.$nextTick();
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

    handleQueryPassed(queryBody) {
      this.filter = queryBody.filter;
    },

    async getMapCoordinates() {
      if (this.data && Array.isArray(this.data)) {
        
        let coordinates =  this.data.map(facility => {
          
          const name = facility.properties.placename
          const coords = facility.geometry.coordinates;
          const id = facility.id;
    
          let row = [coords[1], coords[0], name, id.toString()];
          
          return row; // returns [latitude, longitude]
        });
        coordinates = coordinates.filter(el => {
          return el[0] != "" && el[1] != "";
        })
        let features = coordinates;
        let markers = [];

        for (let i = 0; i < features.length; i++) {
          let el = features[i];
            let m = L.marker([el[0], el[1]]);
            markers.push(m);
        }

        let fGroup = L.featureGroup(markers);
        let bounds = fGroup.getBounds();
        
        let center = bounds.getCenter();

        return [ coordinates, bounds, center ]
      }
      return [];
    },

    async handleSearch(query = this.searchQuery) {
      this.searchQuery = query;
      try {
        await this.fetchSearch();
        this.data = this.filteredData.features;
       
        this.totalResults = this.filteredData.total.value;
        this.totalPages = Math.ceil(this.totalResults / this.paginationSize);
        this.currentPageResults = Math.min(this.paginationSize, this.data.length);
        // Set the coordinates array after the data has been fetched
        [this.coordinates,this.bounds, this.center] = await this.getMapCoordinates();
      } catch (error) {
        console.log(error)
        this.totalResults = 0;
        this.currentPageResults = 0;

        // Reset the coordinates if there's an error
        this.coordinates = [];
      }
    },
    async fetchSearch() {
      const startIndex = (this.currentPage - 1) * this.paginationSize;
      this.isFetching = true;
      let search = this.searchQuery;

      // If the search query is empty, set it to a wildcard
      if (search === '*') {
        search = '*';
      }
      // Build the body of the request
      let bodyObj = {
        query: {
          bool: {
            must: {
              query_string: {
                query: search
              }
            },
            filter: this.filter
          }
        },
        from: startIndex,
        size: this.paginationSize
      };

      let body = JSON.stringify(bodyObj);

      // Fetch the data
      try {
        // console.log("fetchSearchFunction", `${this.$config.apiURL}/facilities`);
        const response = await fetch(`${this.$config.apiURL}/facilities`, {
          body: body,
          headers: {
            "Content-Type": "application/json"
          },
          method: "POST"
        });


        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();

        this.filteredData = data;
        this.isFetching = false;
        this.error = null;

      } catch (error) {
        console.log("no response from search endpoint!")
        this.filteredData = null;
        this.error = error.message;
        this.isFetching = false;
      }
    }

    ,
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
