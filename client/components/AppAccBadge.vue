<template>
    <div>
        <span class="badge pasp relative -z-10 mx-2" v-if="accreditation.pasp === 1">PASP</span>
        <span class="badge paot relative -z-10" v-if="accreditation.paot === 1">PAOT</span>
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
}
</style>
