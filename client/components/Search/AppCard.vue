<template>
    <div class="relative overflow-ellipsis w-full min-h-[180px] sm:min-h-[250px] lg:min-h-[250px] ">
      <a :href="facilityData.facilityUrl">
        <img class=" object-cover mx-auto rounded-[20px] h-[220px] w-full sm:w-auto " :src="facilityData.facilityImage" :alt="facilityData.facilityName" />
      </a>
      <div class="px-5 pb-5">
        <a :href="facilityData.facilityUrl">
          <h5 class="w-full whitespace-nowrap overflow-hidden overflow-ellipsis font-semibold tracking-tight text-gray-900 ">{{ facilityData.facilityName }}</h5>
        </a>
      </div>
    </div>
</template>

  
  <script>
  export default {
    props: ['facilityData'],
  };
  </script>
  