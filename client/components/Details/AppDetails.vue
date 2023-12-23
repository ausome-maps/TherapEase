<template>
  <div class="text-left">
    <div class="flex justify-between pb-1">
      <div>
        <span><svg class="w-6 h-6 text-gray-800 dark:text-white inline-block" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 10 25">
    <path d="M8 0a7.992 7.992 0 0 0-6.583 12.535 1 1 0 0 0 .12.183l.12.146c.112.145.227.285.326.4l5.245 6.374a1 1 0 0 0 1.545-.003l5.092-6.205c.206-.222.4-.455.578-.7l.127-.155a.934.934 0 0 0 .122-.192A8.001 8.001 0 0 0 8 0Zm0 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>
  </svg></span> <span v-if="!!facilityDetails.city && !!facilityDetails.province" class="text-xl"> {{ facilityDetails.city }}, {{facilityDetails.province}}</span><span v-if="facilityDetails.city=='' || !!facilityDetails.province" class="text-xl">{{facilityDetails.province}}</span>
<span v-if="!!facilityDetails.city || facilityDetails.province==''" class="text-xl">{{facilityDetails.city}}</span>
      </div>

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
      //console.log(services);
      return services;
    },
  }

}
  </script>
