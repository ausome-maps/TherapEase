<template>
    <div class="flex h-[fit-content] pb-[25px] w-[100%] border shadow-lg rounded-3xl">
      <!-- Sidebar -->
      <div class="">
        <div class="pt-4 pb-2 px-8">
          <h1 class="text-2xl text-left font-light">Contact Details</h1>
        </div>
        <ul>
          <li class="px-8">
            <div class="flex">
              <div class="mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <!-- Replace the path below with your desired email icon SVG code -->
                  <path d="M10 1C4.48 1 0 5.48 0 10s4.48 9 10 9 10-4.48 10-9S15.52 1 10 1zm5 8.37l-4 2.67-4-2.67V5h8v4.37zM2 6.92l6 4 6-4V5l-6 4-6-4v1.92zM2 15h16v-2H2v2zm0-4h16V5H2v6z" />
                </svg>
              </div>
              <div>
                <a href="mailto:example@example.com">Email: {{facilityDetails.facilityEmail}}</a>
              </div>
            </div>
          </li>
          <li class="px-8">
            <div class="flex">
              <div class="mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <!-- Replace the path below with your desired phone icon SVG code -->
                  <path d="M15 2H5C3.897 2 3 2.897 3 4v12c0 1.103.897 2 2 2h10c1.103 0 2-.897 2-2V4c0-1.103-.897-2-2-2zm-1 14H6V4h8v12zm-4-2a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0-3a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                </svg>
              </div>
              <div>
                <a href="tel:+63{{facilityDetails.facilityContactNumber.replace(/^0+/, '')}}">Contact: {{ facilityDetails.facilityContactNumber }} </a>
              </div>
            </div>
          </li>
          <li class="px-8">
            <div class="flex">
              <div class="mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <!-- Replace the path below with your desired phone icon SVG code -->
                  <path d="M15 2H5C3.897 2 3 2.897 3 4v12c0 1.103.897 2 2 2h10c1.103 0 2-.897 2-2V4c0-1.103-.897-2-2-2zm-1 14H6V4h8v12zm-4-2a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0-3a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                </svg>
              </div>
              <div>
                <a :href="facilityDetails.facilityWebsite" target="_blank">
      Website: {{ facilityDetails.facilityWebsite }}
    </a>

              </div>
            </div>
          </li>
          <li class="px-8">
            <div class="flex">
              <div class="mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <!-- Replace the path below with your desired address icon SVG code -->
                  <path d="M10 2C5.582 2 2 5.582 2 10c0 4.418 3.582 8 8 8s8-3.582 8-8c0-4.418-3.582-8-8-8zm0 14.667c-2.789 0-5.333-2.545-5.333-4.667 0-1.746 1.29-3.95 3.333-6.521 2.043 2.57 3.333 4.774 3.333 6.521 0 2.122-2.544 4.667-5.333 4.667zm1.333-8a2.667 2.667 0 1 1 0-5.334 2.667 2.667 0 0 1 0 5.334z"/>
                </svg>
              </div>Address:  
              <div class="text-left pl-2">
                <span>{{ facilityDetails.facilityAddress }}</span>
              </div>
            </div>
          </li>
        </ul>

        <div class="border-t border-black mx-8 my-6"></div>
        <div class="text-left px-8">
            CREATED by
        </div>
        <div class="text-left px-8">
            <span class="font-bold">{{facilityDetails.facilityOwner}} </span> on <span class="font-bold">{{ facilityDetails.facilityDateCreated }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      facilityDetails: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  
  <style>
  /* Add your custom styles here if needed */
  </style>
  