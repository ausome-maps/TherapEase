<template>
    <div class="flex justify-center w-full">
        <div
            class="bg-transparent grid mx-autogrid-cols-1 sm:grid-cols-1 md:grid-cols-1 xl:grid-cols-2 2xl:grid-cols-3 gap-2 sm:gap-4 p-4">
            <div v-for="facility in facilities" :key="facility.id"
                class="transition duration-500 ease-in-out transform hover:-translate-y-1 hover:scale-110">
                <AppCard :facilityData="facility"
                    class="relative max-h-[300px] rounded-lg hover:shadow-xl transition-shadow duration-300 ease-in-out" />
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
    props: {
        facilities: {
            type: Array,
            required: true
        }
    }

};
</script>