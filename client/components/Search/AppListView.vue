<template>
        <div class="w-full">
            <div class="bg-transparent mx-auto p-2 sm:p-4 md:p-6 xl:p-2">
                <div v-for="facility in facilities.hits" :key="facility.id"
                    class="transition duration-100 ease-in-out transform hover:-translate-y-1">
                    <AppListTile :facilityData="facility"
                        class="relative max-h-[300px] mb-2" />
                </div>
            </div>
        </div>
    </template>
    
    <style scoped>
    .transition {
        transition: all .2s ease-in-out;
    }
    
    .hover\:scale-110:hover {
        transform: scale(1.02);
    }
    
    
    .mb-2 {
        margin-bottom: 0.5rem;
    }
    </style>
      
    <script>
    
    export default {
        props: {
            facilities: {
                type: Object,
                required: true
            }
        },
    };
    </script>
    