<template>
  <div class="relative z-1 w-full flex flex-col justify-center rounded">
    <div :class="{ 'justify-center': !showMap }" class="flex flex-col sm:flex-row h-[100%] min-h-[800px] gap-4">
      <div class="w-full lg:max-w-[850px] xl:max-w-[1100px] flex-grow">
        <ClientOnly>
          <div class="px-5 pb-4 sticky top-0 z-50 bg-white">
            <AppSearchAndFilter @update-search="handleSearch" />
            <AppListingHeader :show-map="showMap" @hide-map="showMap = false" @show-map="showMap = true"
              :view-mode="viewMode" @change-view-mode="handleChangeViewMode" :facilities="data"
              :filteredFacilities="filteredFacilities" />
          </div>
          <AppCardList v-if="viewMode === 'card'" :facilities="data" :filteredFacilities="filteredFacilities" />
          <AppListView v-else-if="viewMode === 'list'" :facilities="data" :filteredFacilities="filteredFacilities" />
        </ClientOnly>
      </div>
      <div v-if="showMap" class="w-full lg:flex-grow mr-8 h-[99vh] sticky top-5 z-10">
        <AppMap :latitude="12.852673" :longitude="121.377034" />
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
      searchQuery: '',
      data: data.features,
      filteredFacilities: [{}],
      viewMode: 'card',
      showMap: true,
      isMobile: false,
      data2: null
    };
  },
  mounted() {
    this.checkIfMobile(); // Initial check
    // Watch for changes in the window width
    window.addEventListener('resize', this.checkIfMobile);
  },
  beforeUnmount() {
    // Clean up the event listener before the component is unmounted
    window.removeEventListener('resize', this.checkIfMobile);
  },
  methods: {
    checkIfMobile() {
      // Check if the viewport width is less than or equal to 768px (tablet width)
      this.isMobile = window.visualViewport.width <= 768;
    },
    handleChangeViewMode(newViewMode) {
      this.viewMode = newViewMode;
      console.log(this.viewMode);
    },
    handleSearch(query) {
      this.searchQuery = query;
      console.log(this.searchQuery);
      this.fetchGeocodeData();
    }
  },
}
</script>
  