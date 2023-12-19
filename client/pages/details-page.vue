<template>
  <div class="justify center top-5 px-10">
    <div class="flex justify-left pt-5">
      <NuxtLink to="/">
        <p class="w-44 inline-block"><svg class="w-5 h-5 text-gray-800 dark:text-white inline-block" aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 8 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M7 1 1.3 6.326a.91.91 0 0 0 0 1.348L7 13" />
          </svg> Go back to search</p>
      </NuxtLink>
    </div>
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
                <div class="min-w-[60%] pl-4 pt-5">
                  <AppDetails :facilityDetails="properties" />
                </div>
                <div class="min-w-[34%] p-5 mr-2">
                  <AppContacts :facilityDetails="properties" />
                  <AppShareSubmit :feedback-url="$config.feedbackURL" />
                </div>
              </div>
            </div>
          </template>
          <div v-if="coordinates[0] != '' && coordinates[1] != ''" class="w-[100%] relative z-[0]">
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
// import data from '../components/facility-data.json'

export default {
  data() {
    return {
      properties: null,
      coordinates: null,
      isMobile: false,
      filteredData: null,
      error: null,
      isFetching: false,
      id: null,
      feedbackUrl: '',
    };
  },
  beforeMount() {
    this.id = this.$route.query.id;
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

    //console.log(this.$config.feedbackURL);
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
        console.log(this.coordinates[0], this.coordinates[1])
      } catch (error) {
        console.log("Error on HandleSearch");
      }
    },
    async fetchSearch() {
        this.isFetching = true;
        // Build the body of the request
        let bodyObj = {
          q: `id:${this.id}`,
          from: 0,
          size: 1
        };

        let body = JSON.stringify(bodyObj);
        console.log("body", body)
        // Fetch the data
        try {
          const response = await fetch(`${this.$config.apiURL}/facilities/search`, {
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
    }
  }
</script>
