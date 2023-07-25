<template>
    <div class="grid grid-cols-4 gap-4 px-5">
        <div class="items-center flex justify-center">
            Showing {{ filteredFacilities.length }} of {{ facilities.length }} results
        </div>
        <div class="w-50%">
            <AppDropdown class="dropdown" :dropdownItems="sortByItems" :dropdownButtonId="sortByButton"
                :dropdownMenuId="sortByMenu" />
        </div>
        <div class="items-center flex justify-center gap-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                <rect width="9" height="9" rx="2" fill="#D48180" />
                <rect x="11" width="9" height="9" rx="2" fill="#D48180" />
                <rect x="11" y="11" width="9" height="9" rx="2" fill="#D48180" />
                <rect y="11" width="9" height="9" rx="2" fill="#D48180" />
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" width="29" height="28" viewBox="0 0 29 28" fill="none">
                <ellipse cx="14.5" cy="14" rx="14.5" ry="14" fill="#D48180" />
                <rect x="7" y="6" width="15" height="3" rx="1.5" fill="white" />
                <rect x="7" y="19" width="15" height="3" rx="1.5" fill="white" />
                <rect x="7" y="13" width="15" height="3" rx="1.5" fill="white" />
            </svg>
        </div>
        <div class="justify-center flex max-w-100">
            <button class="bg-gray-400 rounded-xl p-2">Hide Map</button>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            filteredFacilities: [{}],
            facilities: [{


            }],
            sortByButton: 'sortByButton',
            sortByMenu: 'sortByDropdownMenu',
            sortByItems: [
                { id: 1, label: 'Dashboard' },
                { id: 2, label: 'Settings' },
                { id: 3, label: 'Earnings' },
                { id: 4, label: 'Sign out' }
            ]
        }
    },
    methods: {
        togglePASPAccreditation() {
            this.isPASPAccredited = !this.isPASPAccredited;
        }
    }
}
</script>

<style scoped>
.dropdown>>>.dropdown {
    border-radius: 25px;
}
</style>
