<template>
  <div class="relative z-1 w-full flex top-5 flex-col justify-center rounded">
    <!-- Mobile Tab Switcher -->
    <div v-if="isMobile" class="fixed top-0 left-0 right-0 z-40 bg-white border-b shadow-sm" style="top: 52px;">
      <div class="flex">
        <button @click="mobileTab = 'list'"
          :class="mobileTab === 'list' ? 'border-b-2 border-red-400 text-red-400' : 'text-gray-500'"
          class="flex-1 py-3 text-sm font-medium text-center">
          <svg class="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
          Facilities
        </button>
        <button @click="mobileTab = 'map'"
          :class="mobileTab === 'map' ? 'border-b-2 border-red-400 text-red-400' : 'text-gray-500'"
          class="flex-1 py-3 text-sm font-medium text-center">
          <svg class="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
          Map
        </button>
      </div>
    </div>

    <div :class="{ 'justify-center': !showMap && !isMobile }" class="flex flex-col sm:flex-row h-[100%] min-h-[800px] gap-4"
      :style="isMobile ? 'margin-top: 44px;' : ''">

      <!-- Content Section (hidden when map tab active on mobile) -->
      <div v-show="!isMobile || mobileTab === 'list'" class="w-full lg:max-w-[850px] xl:max-w-[1100px] flex-grow">
        <ClientOnly>
          <div class="px-3 sm:px-5 pb-4 sticky z-50 bg-white" :style="isMobile ? 'top: 96px;' : 'top: 0;'">
            <AppSearchAndFilter @update-search="handleSearch" @query-passed="handleQueryPassed" />
            <AppListingHeader :show-map="showMap" @hide-map="showMap = false" @show-map="showMap = true"
              :view-mode="viewMode" @change-view-mode="handleChangeViewMode" :facilitiesLength="totalResults"
              :filteredFacilitiesLength="currentPageResults" />
          </div>

          <div v-if="currentPageResults === 0" class="w-full text-center py-10">
            <h2 class="text-xl font-semibold">No results found</h2>
            <p>Try adjusting your search or filter criteria.</p>
          </div>

          <AppCardList v-if="viewMode === 'card'" :facilities="data" :filteredFacilities="data"
            @facility-hovered="hoveredFacilityId = $event"
            @facility-unhovered="hoveredFacilityId = null" />
          <AppListView v-else-if="viewMode === 'list'" :facilities="data" :filteredFacilities="data"
            @facility-hovered="hoveredFacilityId = $event"
            @facility-unhovered="hoveredFacilityId = null" />

          <div v-if="totalPages > 1" class="flex justify-center my-4 flex-wrap gap-1">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="px-3 py-2 text-sm bg-gray-200 text-gray-700 border rounded-l-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed">Prev</button>

            <template v-for="page in totalPages" :key="page">
              <button v-if="page === currentPage" class="px-3 py-2 text-sm bg-gray-300 text-gray-700 border">{{ page }}</button>
              <button v-else @click="goToPage(page)"
                class="px-3 py-2 text-sm bg-gray-200 text-gray-700 border hover:bg-red-300">{{ page }}</button>
            </template>

            <button @click="nextPage" :disabled="currentPage === totalPages"
              class="px-3 py-2 text-sm bg-gray-200 text-gray-700 border rounded-r-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed">Next</button>
          </div>
        </ClientOnly>
      </div>

      <!-- Map Section (hidden when list tab active on mobile) -->
      <div v-show="!isMobile || mobileTab === 'map'" :class="isMobile ? 'fixed inset-0 z-30' : (showMap ? 'w-2/4 lg:flex-grow mr-4 h-[99vh] sticky top-5 z-10' : '')" :style="isMobile ? 'top: 96px;' : ''">
        <AppMap v-if="showMap || isMobile" :key="isMobile ? mobileTab : 'map'" :coordinates="coordinates" :bounds="bounds" :latitude="center.lat" :longitude="center.lng" :hoveredFacilityId="hoveredFacilityId" />
      </div>
    </div>
    <div class="h-[80px]"></div>
  </div>
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
      mobileTab: 'list',
      filteredData: [],
      error: null,
      isFetching: false,
      paginationSize: 50,
      totalResults: 0,
      currentPageResults: 0,
      currentPage: 1,
      totalPages: Math.ceil(this.totalResults / this.paginationSize),
      coordinates: [],
      selectedService: 'orthoses',
      filter: {},
      bounds: L.latLngBounds(L.latLng(5.458624890542083, 116.51879773556522), L.latLng(19.215291042674977, 127.04232194261539)),
      center: {
        "lat": 12.384994440877549,
        "lng": 121.67093979526709
      },
      hoveredFacilityId: null,
    };
  },

  async mounted() {
    this.checkIfMobile();

    const access = this.$route.query.access
    const refresh = this.$route.query.refresh
    if (access && refresh) {
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      this.$router.replace({ query: {} })
    }

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
      if (!this.isMobile) {
        this.mobileTab = 'list';
      }
    },

    updateURL() {
      this.$router.push({ query: { search: this.searchQuery, page: this.currentPage } });
    },

    handleChangeViewMode(newViewMode) {
      this.viewMode = newViewMode;
    },

    handleQueryPassed(queryBody) {
      this.filter = queryBody.filters;
      this.currentPage = 1;
      this.handleSearch();
    },

    async getMapCoordinates() {
      if (this.data && Array.isArray(this.data)) {
        let coordinates = this.data.map(facility => {
          const name = facility.properties.placename
          const coords = facility.geometry.coordinates;
          const id = facility.id;
          if (coords[1] < -180 && coords[0] < -180) {
            console.log(coords[0], coords[1]);
          }
          let row = [coords[1], coords[0], name, id.toString()];
          return row;
        });
        coordinates = coordinates.filter(el => {
          return el[0] != "" && el[1] != "";
        }).filter(i => {
          return i[0] > -180 && i[1] > -180;
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
        if (!bounds || !bounds.isValid()) return [[], this.bounds, this.center];
        let center = bounds.getCenter();
        return [coordinates, bounds, center]
      }
      return [];
    },

    async handleSearch(query = this.searchQuery) {
      this.searchQuery = query;
      try {
        await this.fetchSearch();
        this.data = this.filteredData.features;
        this.totalResults = this.filteredData.total;
        this.totalPages = Math.ceil(this.totalResults / this.paginationSize);
        this.currentPageResults = Math.min(this.paginationSize, this.data.length);
        this.hoveredFacilityId = null;
        [this.coordinates, this.bounds, this.center] = await this.getMapCoordinates();
      } catch (error) {
        console.log("error", error)
        this.totalResults = 0;
        this.currentPageResults = 0;
        this.coordinates = [];
      }
    },

    async fetchSearch() {
      const startIndex = (this.currentPage - 1) * this.paginationSize;
      this.isFetching = true;
      let search = this.searchQuery;

      if (search === '*') {
        search = '*';
      }

      let bodyObj = {
        q: search,
        filters: this.filter,
        from: startIndex,
        size: this.paginationSize
      };

      let body = JSON.stringify(bodyObj);

      try {
        const response = await fetch(`${this.$config.public.apiURL}/facilities/search`, {
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