<template>
  <div class="container mx-auto">
    <div class="grid gap-4">
      <!-- Column for Services -->
      <div class="">
  <h2 class="text-2xl mb-2 text-red-400 font-semibold">Services</h2>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
    <ul v-for="(service, index) in services" :key="service.id" :class="{ 'col-span-2': index % 2 === 0 }">
      <li>
        <details>
          <summary class="cursor-pointer font-bold">{{ service.label }}</summary>
          <li v-for="(value, key) in service.mode" :key="key">
            <span v-if="value !== 0">
              <span class="list-item-bullet ml-4">&#8226;</span>
              {{ key }}
            </span>
          </li>
        </details>
      </li>
    </ul>
  </div>
</div>



      <!-- Column for Amenities -->
      <!-- <div class="">
          <h2 class="text-2xl mb-2 text-red-400 font-semibold">Facilities</h2>
          <ul>
            <li v-for="amenity in facilityDetails.facilityAmenities" :key="amenity.id">
              <details>
                <summary class="cursor-pointer ">{{ amenity.name }}</summary>
                <ul>
                  <li v-for="subItem in amenity.subItems" :key="subItem.id">
                    <span class="list-item-bullet">&#8226;</span> {{ subItem.name }}
                  </li>
                </ul>
              </details>
            </li>
          </ul>
        </div> -->
    </div>
  </div>
</template>
  
  
<script>
export default {
  props: {
    services: {
      type: Object,
      required: true
    }
  }
}
</script>
  
<style>
details>summary {

  list-style: none;
}

summary::-webkit-details-marker {
  display: none
}

summary::after {
  content: '';
  border: solid;
  border-width: 0 1px 1px 0;
  display: inline-block;
  padding: 0 5px 5px 0;
  transform: rotate(-45deg);
  margin: 5px 5px 2px 8px;
}

details[open] summary:after {
  content: '';
  border: solid;
  border-width: 0 1px 1px 0;
  display: inline-block;
  padding: 0 5px 5px 0;
  transform: rotate(45deg);
  margin: 5px 5px 3px 10px;
}
</style>
  