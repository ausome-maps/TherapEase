<template>
    <div class="flex justify-center w-full">
        <div class="bg-transparent grid mx-autogrid-cols-1 sm:grid-cols-1 md:grid-cols-1 xl:grid-cols-2 2xl:grid-cols-3 gap-2 sm:gap-4 p-2 sm:p-4 md:p-6 xl:p-8">
            <div v-for="facility in facilities" :key="facility.id" class="transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-110">
                <AppCard :facilityData="facility" class="relative max-h-[300px] rounded-lg hover:shadow-xl transition-shadow duration-300 ease-in-out"/>
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
    
    .hover\:shadow-xl:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
</style>

  
<script>

export default {
    data() {
        return {
            facilities: [
                {
                    "id": 1,
                    "facilityUrl": "https://example.com/facility1",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "Harmony - Accessible Accommodations",
                    "averageRating": 4.5,
                    "facilityRate": 120.99
                }
                ,
                {
                    "id": 2,
                    "facilityUrl": "https://example.com/facility2",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "Red Tomato",
                    "averageRating": 4.8,
                    "facilityRate": 60.0
                }
                ,
                {
                    "id": 3,
                    "facilityUrl": "https://example.com/facility3",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "AccessTech - Assistive Technology Center",
                    "averageRating": 4.2,
                    "facilityRate": null
                }
                ,
                {
                    "id": 4,
                    "facilityUrl": "https://example.com/facility4",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "Aquatic Haven - Swimming Facility",
                    "averageRating": 4.6,
                    "facilityRate": 30.0
                }
                ,
                {
                    "id": 5,
                    "facilityUrl": "https://example.com/facility5",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "Paws & Partners - Service Animals Welcome",
                    "averageRating": 4.9,
                    "facilityRate": null
                }
                ,
                {
                    "id": 6,
                    "facilityUrl": "https://example.com/facility6",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "SoundSense - Hearing Loop System",
                    "averageRating": 4.4,
                    "facilityRate": 80.0
                }
                ,
                {
                    "id": 7,
                    "facilityUrl": "https://example.com/facility7",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "FlexFit - Fitness Center",
                    "averageRating": 4.7,
                    "facilityRate": 50.0
                }
                ,
                {
                    "id": 8,
                    "facilityUrl": "https://example.com/facility8",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "AscendElevate",
                    "averageRating": 4.3,
                    "facilityRate": null
                }
                ,
                {
                    "id": 9,
                    "facilityUrl": "https://example.com/facility9",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "ParkEase",
                    "averageRating": 4.1,
                    "facilityRate": 10.0
                }
                ,
                {
                    "id": 10,
                    "facilityUrl": "https://example.com/facility10",
                    "facilityImage": "https://plus.unsplash.com/premium_photo-1664392032070-80073c185d1f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=738&q=80",
                    "facilityName": "BraillePath",
                    "averageRating": 4.5,
                    "facilityRate": null
                }
            ]

        };
    },
};
</script>