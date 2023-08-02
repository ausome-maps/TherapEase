<template>
  <div class="mx-auto">
    <button :id="dropdownButtonId" @click="toggleDropdown" class="dropdown w-full bg-gray-200  focus:ring-4 focus:outline-none focus:ring-red-200 font-medium rounded-lg text-sm px-4 py-2.5 text-center inline-flex items-center justify-between" type="button">
      <span class="overflow-hidden overflow-ellipsis whitespace-nowrap">{{ selectedItem.label || 'Dropdown button' }}</span>
      <svg aria-hidden="true" class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>
    <!-- Dropdown menu -->
    <div :id="dropdownMenuId" :class="{ 'hidden': !isDropdownOpen }" class="mt-[10px] absolute z-10  bg-green-400 divide-y divide-gray-100 rounded shadow w-44">
      <ul class="py-1 text-sm text-gray-700" :aria-labelledby="dropdownButtonId">
        <li v-for="item in dropdownItems" :key="item.id">
          <a href="#" @click="selectItem(item)" class="block px-4 py-2 hover:bg-gray-100">{{ item.label }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'


let isDropdownOpen = ref(false)
let selectedItem = ref({})

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function selectItem(item) {
  selectedItem.value = item
  isDropdownOpen.value = false
}
</script>

<script>
export default {
  props: {
    dropdownItems: {
      type: Array,
      required: true
    },
    dropdownButtonId: {
      type: String,
      required: true
    },
    dropdownMenuId: {
      type: String,
      required: true
    }
  },
  }

</script>