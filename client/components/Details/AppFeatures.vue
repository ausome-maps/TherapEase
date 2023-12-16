<template>
  <div class="container mx-auto">
    <div class="grid gap-4">
      <!-- Column for Services -->
      <div class="">
        <h2 class="text-2xl mb-2 text-red-400 font-semibold">{{ label }}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <ul v-for="(service, index) in services" :key="service.id" :class="{ 'col-span-2': index % 2 === 0 }">
            <li>

              <h4 class="cursor-pointer font-bold">{{ service.label }}</h4>
            <li v-for="(value, key) in service.mode" :key="key">
              <span v-if="value !== 0">
                <span class="list-item-bullet ml-4">&#8226;</span>
                {{ formatSessionMode(key) }}: {{ getSessionType(value) }}
              </span>
            </li>

            </li>
          </ul>
        </div>
      </div>

      <div v-if="other_services" class="border-t border-gray-300 my-4 mr-4"></div>

      <div>
        <h2 v-if="other_services" class="text-2xl mb-2 text-red-400 font-semibold">Other Services</h2>
        <div v-if="other_services" class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <!-- <ul class="gap-2">
          {{ other_services }}
          <li class="cursor-default font-bold " v-for="(service, index) in other_services.split(',')" :key="index">{{ service.trim() }}</li>
        </ul> -->
          <ul v-for="(service, key, index) in other_services" :key="index">
            <li>
              <h4 class="cursor-pointer font-bold">{{ key }}</h4>
            <li v-for="(value, key) in service" :key="key">
              <span v-if="value !== 0">
                <span class="list-item-bullet ml-4">&#8226;</span>
                {{ formatSessionMode(key) }}: {{ getSessionType(value) }}
              </span>
            </li>

            </li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-300 my-4 mr-4"></div>
    </div>
  </div>
</template>
  
  
<script>
export default {
  props: {
    services: {
      type: Object,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    other_services: {
      type: Object,
      required: true
    }
  },
  methods: {
    getSessionType(value) {
      switch (value) {
        case 0: return "No Offering";
        case 1: return "Individual Sessions";
        case 2: return "Group Sessions";
        case 3: return "Individual and Group Sessions";
        default: return "";
      }
    },
    formatSessionMode(value) {
      switch (value) {
        case 'teletherapy': return "Teletherapy";
        case 'onsite': return "Onsite";
        case 'home_service': return "Home Service";
        default: return "";
      }
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
  