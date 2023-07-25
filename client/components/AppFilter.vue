<template>
    <div class="p-4 w-full">
        <div class="flex flex-col justify-center">
            <div class="flex flex-col md:flex-row md:w-[95%] my-4 gap-4">
                <div class="w-full">
                    <input v-model="searchText" type="text" placeholder="Search..."
                        class="shadow appearance-none border w-full rounded-3xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
                </div>

                <div class="items-center flex justify-center ">
                    <div class="items-center flex justify-center gap-4 w-full md:w-[150px] text-[12px]">PASP Accredited
                        <label class="items-center">
                            <input type="checkbox" value="" class="sr-only peer">
                            <div
                                class="w-11 h-6 relative bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-red-100 dark:peer-focus:ring-red-700 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-red-400">
                            </div>
                            <span class="text-sm font-medium text-gray-900 dark:text-gray-300"></span>
                        </label>
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-4 gap-4 my-4">
                <div class="w-full mb-2 md:mb-0">
                    <AppDropdown class="dropdown" :dropdownItems="dropdownItems" :dropdownButton="dropdownId1" :dropdownMenu="dropdownId1"  />

                </div>
                <div class="w-full mb-2 md:mb-0">
                    <AppDropdown class="dropdown" :dropdownItems="dropdownItems" :dropdownButton="dropdownId2" :dropdownMenu="dropdownId2"  />

                </div>
                <div class="w-full mb-2 md:mb-0">
                    <AppDropdown class="dropdown" :dropdownItems="dropdownItems" :dropdownButton="dropdownId3" :dropdownMenu="dropdownId3"  />

                </div>
                <div class="w-full">
                    <AppDropdown class="dropdown" :dropdownItems="dropdownItems" :dropdownButton="dropdownId4" :dropdownMenu="dropdownId4" />

                </div>
            </div>
            <div class="grid grid-cols-3">
                <AppCheckbox />
                <AppCheckbox />
                <AppCheckbox />
            </div>
        </div>
    </div>
</template>


  
  
<script>
export default {
    data() {
        return {
            searchText: '',
            dropdownId1: 'dropdown1',
            dropdownId2: 'dropdown2',
            dropdownId3: 'dropdown3',
            dropdownId4: 'dropdown4',
            dropdownItems: [
  { id: 1, label: 'Dashboardss' },
  { id: 2, label: 'Settings' },
  { id: 3, label: 'Earnings' },
  { id: 4, label: 'Sign out' }
]
        }
    },

}
</script>
  
<style scoped>

    </style>
  