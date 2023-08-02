<template>
  <div class="justify center">
    <div class="flex justify-center">
      <div class="w-[1440px]">
        <template v-if="isMobile">
          <div class="rounded-xl mx-[20px]">
            <AppGalleryMobile :images="carouselImages" />
          </div>
          <div class="mx-auto pl-8 pt-4">
            <AppDetails :facilityDetails="data" />
          </div>
          <div class="sidebar mx-auto mb-[50px] pt-4 w-[90%]">
            <AppContacts :facilityDetails="facilityDetailsObject" />
            <AppShareSubmit />
          </div>
          <div class="pb-[100px]">

          </div>
        </template>
        <template v-else>
          <div class="relative z-[1]">
            <div class="rounded-xl mx-[20px]">
              <AppGallery :images="carouselImages" />
            </div>
            <div class="flex">
              <div class="min-w-[60%] pl-4 pt-4">
                <AppDetails :facilityDetails="data" />
              </div>
              <div class="min-w-[34%] p-4 mr-2">
                <AppContacts :facilityDetails="data" />
                <AppShareSubmit />
              </div>
            </div>
          </div>
        </template>
        <div class="w-[100%] relative z-[0]">
          <!-- Use a higher z-index value, for example, z-[2] -->
          <AppDetailsMap :latitude="geometry.coordinates[0]"
            :longitude="geometry.coordinates[1]" />
        </div>
        <div class="h-[100px]"></div>
      </div>
    </div>
  </div>
</template>



<script>
import data from '../components/facility-data.json'
export default {
  data() {
    return {
      data: data.features[0].properties,
      geometry: data.features[0].geometry,
      carouselImages: [
        'https://plus.unsplash.com/premium_photo-1689177357836-52c9d90d3d6f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyfHx8ZW58MHx8fHx8&auto=format&fit=crop&w=500&q=60',
        'https://plus.unsplash.com/premium_photo-1689177357836-52c9d90d3d6f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyfHx8ZW58MHx8fHx8&auto=format&fit=crop&w=500&q=60',
        'https://plus.unsplash.com/premium_photo-1681131449465-d5245b9bddfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YmFubmVyfGVufDB8fDB8fHww&auto=format&fit=crop&w=600&q=60',
        'https://plus.unsplash.com/premium_photo-1689177357836-52c9d90d3d6f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyfHx8ZW58MHx8fHx8&auto=format&fit=crop&w=500&q=60',
        'https://plus.unsplash.com/premium_photo-1689177357836-52c9d90d3d6f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyfHx8ZW58MHx8fHx8&auto=format&fit=crop&w=500&q=60',
        'https://plus.unsplash.com/premium_photo-1681131449465-d5245b9bddfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YmFubmVyfGVufDB8fDB8fHww&auto=format&fit=crop&w=600&q=60',
        'https://plus.unsplash.com/premium_photo-1689177357836-52c9d90d3d6f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyfHx8ZW58MHx8fHx8&auto=format&fit=crop&w=500&q=60',
        'https://plus.unsplash.com/premium_photo-1689177357836-52c9d90d3d6f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwyfHx8ZW58MHx8fHx8&auto=format&fit=crop&w=500&q=60',
        'https://plus.unsplash.com/premium_photo-1681131449465-d5245b9bddfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YmFubmVyfGVufDB8fDB8fHww&auto=format&fit=crop&w=600&q=60',
      ],
      facilityDetailsObject: {
        facilityOwner: "Dein Yelmoc",
        facilityDateCreated: "2021-05-25",
        facilityName: "League of Legends",
        facilityLocation: "Pasig City",
        facilityEmail: "deinyelm@gmail.com",
        facilityWebsite: "https://www.ausomemaps.org",
        facilityContactNumber: "09123456789",
        latitudeValue: 12.852673,
        longitudeValue: 121.377034,
        accreditation: true,
        facilityServices: [
          {
            id: 1,
            name: 'Service 1',
            subItems: [
              { id: 1, name: 'Sub Item 1' },
              { id: 2, name: 'Sub Item 2' },
              // Add more sub-items here as needed
            ],
          },
          {
            id: 2,
            name: 'Service 2',
            subItems: [
              { id: 1, name: 'Sub Item 1' },
              { id: 2, name: 'Sub Item 2' },
              // Add more sub-items here as needed
            ],
          },
          // Add more services here as needed
        ],
        facilityAmenities: [
          {
            id: 1,
            name: 'Amenity 1',
            subItems: [
              { id: 1, name: 'Sub Item 1' },
              { id: 2, name: 'Sub Item 2' },
              // Add more sub-items here as needed
            ],
          },
          {
            id: 2,
            name: 'Amenity 2',
            subItems: [
              { id: 1, name: 'Sub Item 1' },
              { id: 2, name: 'Sub Item 2' },
              // Add more sub-items here as needed
            ],
          },
          // Add more amenities here as needed
        ],
        facilityAddress: "123 Main Street, Barangay Kapitolyo,Pasig City, Metro Manila,Philippines",
        listingDescription: "Step into our serene therapy room, a sanctuary designed to foster healing and personal growth. Embrace tranquility as soft hues and soothing aromas envelop you, creating a nurturing atmosphere. Our therapy room provides a safe haven where expert therapists guide you towards self-discovery and emotional well-being. With comfortable furnishings and gentle lighting, it's a space where you can explore your innermost thoughts and feelings, unburden yourself, and embark on a transformative journey towards a happier, healthier you."
      }
      ,
      isMobile: false
    }
  },
  mounted() {
    this.checkIfMobile(); // Initial check
    // console.log(data.features[0].properties);
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
    }
  }
}
</script>
