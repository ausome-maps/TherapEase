<template>
  <div class="relative z-1 w-full flex flex-col justify-center rounded">
    <div :class="{ 'justify-center': !showMap }" class="flex flex-col sm:flex-row h-[100%] min-h-[800px] gap-4">
      <div class="w-full lg:max-w-[850px] flex-grow">
        <ClientOnly>
          <div class="px-5 pb-4 sticky top-0 z-10 bg-white">
            <AppSearchAndFilter />
            <AppListingHeader :show-map="showMap" @hide-map="showMap = false" @show-map="showMap = true"
            :view-mode="viewMode" @change-view-mode="handleChangeViewMode" :facilities="data"
            :filteredFacilities="filteredFacilities" />
          </div>
          
          <AppCardList v-if="viewMode === 'card'" :facilities="data" :filteredFacilities="filteredFacilities" />
          <AppListView v-else-if="viewMode === 'list'" :facilities="data"
            :filteredFacilities="filteredFacilities" />
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
      data: data.features,
      filteredFacilities: [{}],
      viewMode: 'card',
      showMap: true,
      facilities: [
        {
          "id": 1,
          "facilityUrl": "https://example.com/facility1",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "Harmony - Accessible Accommodations",
          "averageRating": 4.5,
          "facilityRate": 120.99,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 2,
          "facilityUrl": "https://example.com/facility2",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "Red Tomato",
          "averageRating": 4.8,
          "facilityRate": 60.0,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 3,
          "facilityUrl": "https://example.com/facility3",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "AccessTech - Assistive Technology Center",
          "averageRating": 4.2,
          "facilityRate": null,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 4,
          "facilityUrl": "https://example.com/facility4",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "Aquatic Haven - Swimming Facility",
          "averageRating": 4.6,
          "facilityRate": 30.0,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 5,
          "facilityUrl": "https://example.com/facility5",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "Paws & Partners - Service Animals Welcome",
          "averageRating": 4.9,
          "facilityRate": null,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 6,
          "facilityUrl": "https://example.com/facility6",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "SoundSense - Hearing Loop System",
          "averageRating": 4.4,
          "facilityRate": 80.0,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 7,
          "facilityUrl": "https://example.com/facility7",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "FlexFit - Fitness Center",
          "averageRating": 4.7,
          "facilityRate": 50.0,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 8,
          "facilityUrl": "https://example.com/facility8",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "AscendElevate",
          "averageRating": 4.3,
          "facilityRate": null,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 9,
          "facilityUrl": "https://example.com/facility9",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "ParkEase",
          "averageRating": 4.1,
          "facilityRate": 10.0,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
        ,
        {
          "id": 10,
          "facilityUrl": "https://example.com/facility10",
          "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
          "facilityName": "BraillePath",
          "averageRating": 4.5,
          "facilityRate": null,
          "facilityLocation": "123 Example St, San Francisco, CA 94105",
          "services": [{}]
        }
      ]

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
    }
  }

}
</script>
  