<template>
    <div class="flex justify-center w-full">
        <div
            class="bg-transparent grid mx-autogrid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg: xl:grid-cols-3 2xl:grid-cols-4 gap-1 sm:gap-1 p-4">
            <div v-for="facility in facilities.hits"
                class="transition duration-500 ease-in-out p-2 transform hover:-translate-y-1 hover:scale-110">
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
            type: Object,
            required: true
        }
    },
    mounted() {
        console.log("Initial value:", this.facilities)
    },
    watch: {
        'facilities.hits': {
            deep: true, // this is necessary if you want to watch nested properties
            handler(newVal, oldVal) {
                console.log("Updated value:", newVal);
            }
        }
    }
};
</script>
