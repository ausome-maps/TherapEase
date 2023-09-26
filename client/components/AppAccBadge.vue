<template>
    <div>
        <span class="bg-indigo-100 text-indigo-800 text-lg font-medium mr-2 px-2.5 py-0.5 rounded-full dark:bg-indigo-900 dark:text-indigo-300" v-if="accreditation.paot === 1">PAOT</span>
        <span class="bg-yellow-100 text-yellow-800 text-lg font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300" v-if="accreditation.pasp === 1">PASP</span>

    </div>
</template>

<script>

export default {
    props: {
        accreditation: {
            type: Object,
            required: true
        }
    },
    mounted() {
        console.log(this.accreditation)
    }

}
</script>

<style scoped>
.badge {
    color: white;
    padding: 2px 10px;
    border-radius: 15px;
}

.pasp {
    background-color: #00860D;
}

.paot {
    background-color: #9747FF;
}</style>
