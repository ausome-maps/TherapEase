<template>
    <div>
      <div class="text-red-400 p-4 text-3xl ">
        Where to Find Us
      </div>
      <div class="h-[400px] rounded-xl mx-4">
        <l-map ref="map" v-model:zoom="zoom" :center="mapCenter">
          <l-tile-layer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            layer-type="base"
            name="OpenStreetMap"
          ></l-tile-layer>
          <l-marker :lat-lng="mapCenter"></l-marker>
        </l-map>
      </div>
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
        return [this.latitude, this.longitude];
      },
    },
  };
  </script>
  
  <style></style>
  