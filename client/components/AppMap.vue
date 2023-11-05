<template>
  <div class="h-full w-full rounded-xl -z-10 relative">
    <div class="info-card" :style="{ left: cardPosition.x, top: cardPosition.y }" v-if="showCard">
      {{ cardContent }}
    </div>



    <l-map ref="map" v-model:zoom="zoom" :center="mapCenter" :bounds="boundsLocal" :use-global-leaflet="false">
      <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
        name="OpenStreetMap"></l-tile-layer>
      <l-marker v-for="([lat, lng, name, id]) in coordinates" :key="`${id}`" :lat-lng="[lat, lng]"
        @mouseover="showInfoCard($event, name)" @mouseout="hideInfoCard" @click="navigateToDetails(id)" :icon="icon"></l-marker>
    </l-map>
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
    id: {
      type: String,
      required: false,
    },
    bounds: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      zoom: 6,
      showCard: false,
      cardContent: '',
      cardPosition: { x: '50px', y: '20px' },
      icon: L.icon({
        iconUrl: icon_marker,
        iconSize: [19.1, 29.67],
        iconAnchor: [10, 30]
      }),
      boundsLocal:this.bounds,
    };
  },
  methods: {
    showInfoCard(event, content) {
      this.cardContent = content;
      this.$nextTick(() => {
        this.showCard = true;
      });
    },
    hideInfoCard() {
      this.showCard = false;
    },
    navigateToDetails(id) {
      this.$router.push(`/details-page?id=${id}`);
    },
    computeBoundsZoom() {
      this.$nextTick(() => {
        this.$nextTick(()=>{
          setTimeout((a) => {
            let mapObject = this.$refs.map.leafletObject;

            let corner1 = L.latLng(19.215291042674977, 116.51879773556522),
            corner2 = L.latLng(5.458624890542083, 127.04232194261539),
            fallbackBounds = L.latLngBounds(corner1, corner2);

            if(this.boundsLocal.isValid()){
              this.zoom = 9;
            }else{
              this.boundsLocal = fallbackBounds;
              this.zoom = 9;
            }
              
            
          }, 3000);
        })
      })
    },
  },
  computed: {
    mapCenter() {
      return [this.latitude, this.longitude];
    },
  },
  mounted() {
    this.computeBoundsZoom();
  },
};
</script>

<style scoped>
.leaflet-container {
  border-radius: 15px;
}

.info-card {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 10px;
  background-color: #D48180;
  color: white;
  font-weight: bold;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}
</style>
