<template>
    <div>
        <input type="text" v-model="address" placeholder="Enter an address" />
        <button @click="fetchSearch">Get geocode</button>

        <div v-if="isFetching">Loading…</div>
        <div v-else-if="error">Error: {{ error }}</div>
        <div v-else-if="data">
            <div v-for="hit in data.hits.hits" :key="hit._id">
                <p>Placename: {{ hit._source.properties.placename }}</p>
                <p>Address: {{ hit._source.properties.address }}</p>
                <p>Email: {{ hit._source.properties.email_address }}</p>
                <p>Website: {{ hit._source.properties.website }}</p>
                <!-- ... other fields ... -->

                <h3>Services Offered:</h3>
                <ul>
                    <li v-for="(service, key) in hit._source.properties.services_offered" :key="key">
                        {{ service.label }}
                        <ul>
                            <li v-for="(modeValue, modeKey) in service.mode" :key="modeKey" v-if="modeValue">
                                {{ modeKey }}
                            </li>
                        </ul>
                    </li>
                </ul>
                <hr> <!-- horizontal line to separate results -->
            </div>
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
            const { data, error, isFetching } = useFetch(`${this.$config.geocodeURL}?q=${this.address}`)
            this.data = await data
            //console.log(this.data)
            this.error = error
            this.isFetching = isFetching
        },
        async fetchSearch() {
            //   const startIndex = (this.currentPage - 1) * this.paginationSize;
            const queryParameters = {
                q: this.address,
                // size: this.paginationSize,
                // from: startIndex,
                //         "query": {
                //     "match": {
                //       "placename": {
                //         "query": "alternative",
                //         "fuzziness": 2
                //       }
                //     }
                //   }
            };

            const { data, error, isFetching } = await useFetch(this.$config.search, {
                query: queryParameters,
            });
            this.data = data;
            this.error = error;
            this.isFetching = isFetching;
        },
    }
} </script>
