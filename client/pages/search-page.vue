<template>
  <div class="relative z-1 w-full flex flex-col justify-center rounded">
      <div class="relative z-20 max-w-[850px] w-[60%] border shadow-md rounded-3xl mx-auto">
          <AppFilter />
      </div>
      <div class="flex flex-col sm:flex-row mt-8 h-[100%] min-h-[800px] gap-4">
          <div class="w-full lg:max-w-[850px] flex-grow">
              <AppListingHeader />
              <AppCardList />
          </div>
          <div class="w-full lg:flex-grow mr-8 h-[99vh] z-10">
              <AppMap :latitude="12.852673" :longitude="121.377034" />
          </div>
      </div>
  </div>
  <div class="h-[100px]"></div>
</template>
  
  
  
<script>

export default {
  data() {
    return {
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
  