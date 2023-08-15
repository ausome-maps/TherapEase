<template>
  <div class="h-full w-full rounded-xl -z-10 relative">
    <l-map ref="map" v-model:zoom="zoom" :center="mapCenter" :use-global-leaflet="false">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>
      <l-marker v-for="coord in coordinates" :key="coord.toString()" :lat-lng="coord"></l-marker>
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
  coordinates: {
    type: Array,
    required: true,
    default: () => []
  },
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
    return [this.latitude, this.longitude];
  },
},
created() {
  console.log("Latitude:", this.latitude);
  console.log("Longitude:", this.longitude);
  console.log("Coordinates:", this.coordinates);
},
};
</script>

<style scoped>
.leaflet-container {
  border-radius: 15px;
}
</style>
