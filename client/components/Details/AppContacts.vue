<template>
  <div class="flex h-[fit-content] justify-center pb-[25px] w-[100%] border shadow-lg rounded-3xl">
    <!-- Sidebar -->
    <div class="">
      <div class="pt-4 pb-2 px-8">
        <h1 class="text-2xl text-left font-light">Contact Details</h1>
      </div>
      <ul>
        <li class="px-4">
          <div class="flex">
            <div class="mr-2">
              <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M3.0132 9.15129C3 9.69022 3 10.3021 3 11V13C3 15.8284 3 17.2426 3.87868 18.1213C4.75736 19 6.17157 19 9 19H15C17.8284 19 19.2426 19 20.1213 18.1213C21 17.2426 21 15.8284 21 13V11C21 10.3021 21 9.69022 20.9868 9.15129L12.9713 13.6044C12.3672 13.9399 11.6328 13.9399 11.0287 13.6044L3.0132 9.15129ZM3.24297 7.02971C3.32584 7.05052 3.4074 7.08237 3.48564 7.12584L12 11.856L20.5144 7.12584C20.5926 7.08237 20.6742 7.05052 20.757 7.02971C20.6271 6.55619 20.4276 6.18491 20.1213 5.87868C19.2426 5 17.8284 5 15 5H9C6.17157 5 4.75736 5 3.87868 5.87868C3.57245 6.18491 3.37294 6.55619 3.24297 7.02971Z"
                    fill="#D48180" />
                </svg>
              </span>
            </div>
            <div class="truncate">
  <a href="mailto:example@example.com">Email: {{ facilityDetails.email_address }}</a>
</div>

          </div>
        </li>
        <li class="px-4">
          <div class="flex">
            <div class="mr-2">
              <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M6.67962 3.32038L7.29289 2.70711C7.68342 2.31658 8.31658 2.31658 8.70711 2.70711L11.2929 5.29289C11.6834 5.68342 11.6834 6.31658 11.2929 6.70711L9.50048 8.49952C9.2016 8.7984 9.1275 9.255 9.31653 9.63307C10.4093 11.8186 12.1814 13.5907 14.3669 14.6835C14.745 14.8725 15.2016 14.7984 15.5005 14.4995L17.2929 12.7071C17.6834 12.3166 18.3166 12.3166 18.7071 12.7071L21.2929 15.2929C21.6834 15.6834 21.6834 16.3166 21.2929 16.7071L20.6796 17.3204C18.5683 19.4317 15.2257 19.6693 12.837 17.8777L11.6286 16.9714C9.88504 15.6638 8.33622 14.115 7.02857 12.3714L6.12226 11.163C4.33072 8.7743 4.56827 5.43173 6.67962 3.32038Z"
                    fill="#D48180" />
                </svg>
              </span>
            </div>
            <div>
              <a href="tel:+63{{facilityDetails.facilityContactNumber.replace(/^0+/, '')}}">Contact: {{
                facilityDetails.contact_number_mobile }} </a>
            </div>
          </div>
        </li>
        <li class="px-4">
          <div class="flex">
            <div class="mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="8" stroke="#D48180" stroke-width="2" />
                <ellipse cx="12" cy="12" rx="3" ry="8" stroke="#D48180" stroke-width="2" />
                <path d="M4 12H20" stroke="#D48180" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>
            <div>
              <a :href="facilityDetails.facilityWebsite" target="_blank">
                Website: {{ facilityDetails.website }}
              </a>

            </div>
          </div>
        </li>
        <li class="px-4">
          <div class="flex">
            <div class="mr-2">
              <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path fill-rule="evenodd" clip-rule="evenodd"
                    d="M12.398 19.804C13.881 19.0348 19 16.0163 19 11C19 7.13401 15.866 4 12 4C8.13401 4 5 7.13401 5 11C5 16.0163 10.119 19.0348 11.602 19.804C11.8548 19.9351 12.1452 19.9351 12.398 19.804ZM12 14C13.6569 14 15 12.6569 15 11C15 9.34315 13.6569 8 12 8C10.3431 8 9 9.34315 9 11C9 12.6569 10.3431 14 12 14Z"
                    fill="#D48180" />
                </svg>
              </span>
            </div>Address:
            <div class="text-left pl-2">
              <span>{{ facilityDetails.address }}</span>
            </div>
          </div>
        </li>
      </ul>

      <div class="border-t border-black mx-8 my-6"></div>
      <div class="text-left px-8">
        Contact person:
      </div>
      <!-- <div class="text-left px-8">
        <span class="font-bold">{{ facilityDetails.info_src_name }} </span> on <span class="font-bold">{{
          getDateFromTimestamp(facilityDetails.start) }}</span>
      </div> -->
      <div class="text-left px-8">
        <span class="font-bold">{{ facilityDetails.info_src_name }} </span> 
      </div>
    </div>
  </div>
</template>
  
<script>
export default {
  props: {
    facilityDetails: {
      type: Object,
      required: true,
    },

  },
  methods: {
    getDateFromTimestamp: function(timestamp) {
      try{
        const date = new Date(timestamp);
        return date.toISOString().split('T')[0];
      }catch(error){
        return '';
      }
    }
  },
}
</script>
  
<style scoped>/* Add your custom styles here if needed */</style>
  