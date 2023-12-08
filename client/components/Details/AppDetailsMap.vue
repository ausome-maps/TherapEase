<template>
  <div>
    <div class="text-red-400 p-4 text-3xl ">
      Where to Find Us
    </div>
    <div class="h-[400px] rounded-xl mx-4">
      <l-map ref="map" v-model:zoom="zoom" :center="mapCenter" :use-global-leaflet="false">
        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
          name="OpenStreetMap"></l-tile-layer>
        <l-marker :lat-lng="mapCenter" :icon="icon"></l-marker>
      </l-map>
    </div>
  </div>
</template>


<script>
import L from 'leaflet';
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
globalThis.L = L;

import icon_marker from "assets/images/ausome_marker.png"

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
      zoom: 18,
      icon: L.icon({
        iconUrl: icon_marker,
        iconSize: [19.1, 29.67],
        iconAnchor: [10, 30]
      }),
    };
  },
  computed: {

    mapCenter() {
      return [this.longitude, this.latitude];
    },
  },
  created() {
  },
};
</script>

<style></style>
