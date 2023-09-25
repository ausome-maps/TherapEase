<template>
  <div class="h-full w-full rounded-xl -z-10 relative">
    <div class="info-card" :style="{ left: cardPosition.x, top: cardPosition.y }" v-if="showCard">
  {{ cardContent }}
</div>



    <l-map ref="map" v-model:zoom="zoom" :center="mapCenter" :use-global-leaflet="false">
      <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
        name="OpenStreetMap"></l-tile-layer>
      <l-marker v-for="([lat, lng, name, id]) in coordinates" :key="`${lat},${lng}`" :lat-lng="[lat, lng]"
        @mouseover="showInfoCard($event, name)" @mouseout="hideInfoCard" @click="navigateToDetails(id)"></l-marker>
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
    id: {
      type: String,
      required: false,
    }
  },
  data() {
    return {
      zoom: 12,
      showCard: false,
      cardContent: '',
      cardPosition: { x: '50px', y: '20px' },
    };
  },
  methods: {
    showInfoCard(event, content) {
    this.cardContent = content;
    this.$nextTick(() => {
        this.showCard = true;
    });
}

,
    hideInfoCard() {
      this.showCard = false;
    },
    navigateToDetails(id) {
      this.$router.push(`/details-page?id=${id}`);
    },
  }
  ,
  computed: {
    mapCenter() {
      return [this.latitude, this.longitude];
    },
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
