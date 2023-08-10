<template>
    <div> <input type="text" v-model="address" placeholder="Enter an address" /> <button @click="fetchGeocode">Get
            geocode</button>
        <div v-if="isFetching">Loading…</div>
        <div v-else-if="error">Error: {{ error }}</div>
        <div v-else-if="data">
            <p>Data: {{ data }}</p>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            address: '',
            data: null,
            error: null,
            isFetching: false
        }
    }, methods: {
        async fetchGeocode() {
            // THIS DOESNT WORK
            // const { data, error, isFetching } = useFetch(`${this.$config.geocode}?q=${this.address}`)

            // THIS WORKS
            const { data, error, isFetching } = useFetch('https://jsonplaceholder.typicode.com/todos/1')
            
            this.data = await data
            console.log(this.data)
            this.error = error
            this.isFetching = isFetching
        }
    }
} </script>