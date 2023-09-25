<template>
  <div class="justify center top-5">
    <div class="flex justify-center">
      <div class="w-[1440px]">

        <!-- Loading State -->
        <template v-if="!properties">
          <div class="text-center py-5">
            Loading...
          </div>
        </template>

        <!-- Data Loaded State -->
        <template v-else>
          <template v-if="isMobile">
            <div class="rounded-xl mx-[20px]">
              <AppGalleryMobile :images="properties.images" />
            </div>
            <div class="mx-auto pl-8 pt-4">
              <AppDetails :facilityDetails="properties" />
            </div>
            <div class="sidebar mx-auto mb-[50px] pt-4 w-[90%]">
              <AppContacts :facilityDetails="properties" />
              <AppShareSubmit />
            </div>
            <div class="pb-[100px]"></div>
          </template>
          <template v-else>
            <div class="relative z-[1]">
              <div class="rounded-xl mx-[20px]">
                <AppGallery :images="properties.images" />
              </div>
              <div class="flex">
                <div class="min-w-[60%] pl-4 pt-4">
                  <AppDetails :facilityDetails="properties" />
                </div>
                <div class="min-w-[34%] p-4 mr-2">
                  <AppContacts :facilityDetails="properties" />
                  <AppShareSubmit />
                </div>
              </div>
            </div>
          </template>
          <div class="w-[100%] relative z-[0]">
            <AppDetailsMap :latitude="coordinates[0]" :longitude="coordinates[1]" />
          </div>
          <div class="h-[100px]"></div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>

// placeholder data
import data from '../components/facility-data.json'

export default {
  data() {
    return {
      properties: null,
      coordinates: null,
      isMobile: false,
      filteredData: null,
      error: null,
      isFetching: false,
      id: this.$route.query.id
    }
  },
  beforeRouteUpdate(to, from, next) {
    if (to.query.id !== from.query.id) {
      this.handleSearch();
    }
    next();
  },

  async mounted() {
    this.checkIfMobile(); // Initial check
    // Watch for changes in the window width
    window.addEventListener('resize', this.checkIfMobile);
    await this.$nextTick();
    await this.handleSearch();
  },

  beforeUnmount() {
    // Clean up the event listener before the component is unmounted
    window.removeEventListener('resize', this.checkIfMobile);
  },

  methods: {
    checkIfMobile() {
      // Check if the viewport width is less than or equal to 768px (tablet width)
      this.isMobile = window.visualViewport.width <= 769;
    },
    async handleSearch() {
      await this.fetchSearch();
      try {
        this.properties = this.filteredData.features[0].properties;
        this.coordinates = this.filteredData.features[0].geometry.coordinates;
        console.log(this.coordinates);
      } catch (error) {
        console.log("Error on HandleSearch");
      }
    },
    async fetchSearch() {
      const { data, error, isFetching } = await useFetch(`${this.$config.facilities}?q=${this.id}`, {
        method: "GET"
      });
      this.filteredData = data;
      this.error = error;
      this.isFetching = isFetching;
    },
  }
}
</script>
