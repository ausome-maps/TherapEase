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
              <span class="icon">
                <svg viewBox="0 -54 500 500">
                  <path
                    d="M0,50a40,49 0 01 40-49h420a40,49 0 01 40,49c0,22-28,55-46,70l-171,118.5c-27,15.5-39,15.5-66,0l-171-118.5c-28-15-46-48-46-70z" />

                  <path
                    d="M0,127.5v221.5a45,45 0 00 45,45h415a45,45 0 00 40-45v-221.5c-8,8.5-16,15.5-26,22.5l-162,113c-47,31-77,31-124,0l-162-113c-10-6-18-14-26-22.5z" />
                </svg>
              </span>
            </div>
            <div>
              <a href="mailto:example@example.com">Email: {{ facilityDetails.facilityEmail }}</a>
            </div>
          </div>
        </li>
        <li class="px-8">
          <div class="flex">
            <div class="mr-2">
              <span class="icon">
                <svg viewBox="0 0 500 500">
                  <path
                    d="M128,21q40,75,53,91.5q10,15.5-2,27.5c-10,13-38,32-45,40c-10,9-12,15-3,32q54,105,158,156c18,10,20,5,32-5c8-8,20-27,35-41c10-11,20-12,32-3q14,11,88,51c9,5,11,8,9,27q-7,40-22,51q-67,53-133,29c-180-55-286-195-315-336q-4-62,36-105q10-13,30-17c35-11,42-6,47,2z" />
                </svg>
              </span>
            </div>
            <div>
              <a href="tel:+63{{facilityDetails.facilityContactNumber.replace(/^0+/, '')}}">Contact: {{
                facilityDetails.facilityContactNumber }} </a>
            </div>
          </div>
        </li>
        <li class="px-8">
          <div class="flex">
            <div class="mr-2">
              <svg class="svg-icon" viewBox="0 0 24 24">
                <path
                  d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-2.29-2.333A17.9 17.9 0 0 1 8.027 13H4.062a8.008 8.008 0 0 0 5.648 6.667zM10.03 13c.151 2.439.848 4.73 1.97 6.752A15.905 15.905 0 0 0 13.97 13h-3.94zm9.908 0h-3.965a17.9 17.9 0 0 1-1.683 6.667A8.008 8.008 0 0 0 19.938 13zM4.062 11h3.965A17.9 17.9 0 0 1 9.71 4.333 8.008 8.008 0 0 0 4.062 11zm5.969 0h3.938A15.905 15.905 0 0 0 12 4.248 15.905 15.905 0 0 0 10.03 11zm4.259-6.667A17.9 17.9 0 0 1 15.973 11h3.965a8.008 8.008 0 0 0-5.648-6.667z" />
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
              <span class="icon">
                <svg viewBox="-83.5 0 500 500">
                  <g fill-rule="evenodd">
                    <path
                      d="M166.5,482 C 245,396 328,273 333,181 A166.5,166.5 0 0 0 0,181 C 5,273 88,396 166.5,482 Z M 226,178 A59.5,59.5 0 0 1 107,178 A59.5,59.5 0 0 1 226,178 Z" />
                  </g>
                </svg>
              </span>
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
        <span class="font-bold">{{ facilityDetails.facilityOwner }} </span> on <span class="font-bold">{{
          facilityDetails.facilityDateCreated }}</span>
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
svg {
  margin: auto;
  width: 18px;
  height: 20px;
  fill: rgb(248 113 113);
}

/* Add your custom styles here if needed */</style>
  