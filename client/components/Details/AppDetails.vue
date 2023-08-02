<template>
  <div class="text-left">
    <div class="flex justify-between">
      <div class="text-xl">{{ facilityDetails.city }}, {{facilityDetails.province}}</div>
      <span class="badge relative -z-10" v-if="facilityDetails.accreditation">Accredited</span>
    </div>
    <h1 class="text-4xl font-bold mb-4 text-red-400">
      {{ facilityDetails.placename }}
    </h1>
    <div class="pr-12">
      {{ facilityDetails.desc_long }}
    </div>
    <!-- Insert a thick h line-->
    <div class="border-t border-gray-300 my-4 mr-4"></div>
    
    <AppFeatures :services="facilityDetails.services_offered" />
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
}
  </script>