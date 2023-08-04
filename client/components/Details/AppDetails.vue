<template>
  <div class="text-left">
    <div class="flex justify-between">
      <div class="text-xl">{{ facilityDetails.city }}, {{facilityDetails.province}}</div>
      <AppAccBadge :accreditation="facilityDetails.accreditation"/>
    </div>
    <h1 class="text-4xl font-bold mb-4 text-red-400">
      {{ facilityDetails.placename }}
    </h1>
    <div class="pr-12">
      {{ facilityDetails.desc_long }}
    </div>
    <!-- Insert a thick h line-->
    <div class="border-t border-gray-300 my-4 mr-4"></div>
    <AppFeatures :services="filteredServices" :other_services="facilityDetails.other_services" label="Services" />
  </div>
  
</template>

<style>
  .badge {
    background-color: #D1FAE5;
    color: #065F46;
    padding: 2px 10px;
    border-radius: 15px;
    position: relative;
    right: 30px;
  }
</style>

  
  <script>
  export default {
    props: {
        facilityDetails: {
            type: Object,
            required: true
        }
    },
    computed: {
    filteredServices() {
      let services = {...this.facilityDetails.services_offered};
      for (let service in services) {
        let modes = services[service].mode;
        if (Object.values(modes).every(mode => mode === 0)) {
          delete services[service];
        }
      }
      console.log(services);
      return services;
    },
  }

}
  </script>