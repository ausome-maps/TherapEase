<template>
    <div class="h-full w-full rounded-xl -z-10 relative">
      <l-map ref="map" v-model:zoom="zoom" :center="mapCenter" :use-global-leaflet="false">
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        ></l-tile-layer>
        <l-marker :lat-lng="mapCenter"></l-marker>
      </l-map>
    </div>
</template>


<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  props: {
    latitude: {
      type: Number,
      required: true,
    },
    longitude: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      zoom: 12,
    };
  },
  computed: {
    mapCenter() {
      return [this.latitude, this.longitude]; // Swap the order of latitude and longitude.
    },
  },
  created() {
    console.log("Latitude:", this.latitude);
    console.log("Longitude:", this.longitude);
  },
};
</script>

<style scoped>
.leaflet-container {
    border-radius: 15px;
}</style>
