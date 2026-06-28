<template>
  <div class="h-full w-full rounded-xl relative">
    <div class="info-card" :style="{ left: cardPosition.x, top: cardPosition.y }" v-if="showCard">
      {{ cardContent }}
    </div>

    <l-map ref="map" v-model:zoom="zoom" :center="mapCenter" :bounds="boundsLocal" :use-global-leaflet="false" @ready="onMapReady">
      <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" layer-type="base"
        name="OpenStreetMap"></l-tile-layer>
      <l-marker v-for="([lat, lng, name, id]) in coordinates" :key="`${id}`" :lat-lng="[lat, lng]"
        @mouseover="showInfoCard($event, name)" @mouseout="hideInfoCard" @click="navigateToDetails(id)"
        :icon="hoveredFacilityId && hoveredFacilityId === id ? hoveredIcon : icon"></l-marker>
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
    },
    hoveredFacilityId: {
      type: String,
      required: false,
      default: null,
    },
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
      hoveredIcon: L.divIcon({
        className: 'green-marker-icon',
        iconSize: [24, 33],
        iconAnchor: [12, 33],
        html: `<svg width="24" height="33" viewBox="0 0 24 33" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 0C5.37 0 0 5.37 0 12c0 8.5 12 21 12 21s12-12.5 12-21C24 5.37 18.63 0 12 0z" fill="#4CAF50" stroke="#388E3C" stroke-width="1.5"/>
          <circle cx="12" cy="12" r="4.5" fill="white"/>
        </svg>`
      }),
      boundsLocal:this.bounds,
      resetControl: null,
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
    resetMap() {
      this.$nextTick(() => {
        let mapObject = this.$refs.map && this.$refs.map.leafletObject;
        if (!mapObject) return;
        mapObject.setView([12.384, 121.67], 6, { animate: true });
      });
    },
    computeBoundsZoom() {
      this.$nextTick(() => {
        let mapObject = this.$refs.map && this.$refs.map.leafletObject;
        if (!mapObject) return;

        let corner1 = L.latLng(19.215291042674977, 116.51879773556522),
        corner2 = L.latLng(5.458624890542083, 127.04232194261539),
        fallbackBounds = L.latLngBounds(corner1, corner2);

        if (!this.boundsLocal.isValid()) {
          this.boundsLocal = fallbackBounds;
        }

        mapObject.fitBounds(this.boundsLocal, { animate: false, padding: [20, 20] });
      })
    },
    onMapReady() {
      this.$nextTick(() => {
        let mapObject = this.$refs.map && this.$refs.map.leafletObject;
        if (!mapObject) return;

        if (this.resetControl) {
          mapObject.removeControl(this.resetControl);
        }

        let ResetControl = L.Control.extend({
          onAdd: () => {
            let div = L.DomUtil.create('div', 'reset-map-control leaflet-bar leaflet-control');
            div.innerHTML = `<a href="#" role="button" title="Reset map view" style="display:flex;align-items:center;justify-content:center;width:34px;height:34px;font-size:16px;line-height:1;text-decoration:none;color:#555;">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="1 4 1 10 7 10"></polyline>
                <polyline points="23 20 23 14 17 14"></polyline>
                <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
              </svg></a>`;
            L.DomEvent.disableClickPropagation(div);
            L.DomEvent.on(div.querySelector('a'), 'click', (e) => {
              L.DomEvent.preventDefault(e);
              this.resetMap();
            });
            return div;
          }
        });
        this.resetControl = new ResetControl({ position: 'topleft' });
        mapObject.addControl(this.resetControl);
      });
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
  height: 100% !important;
  width: 100% !important;
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

<style>
.green-marker-icon {
  background: transparent !important;
  border: none !important;
}

.reset-map-control {
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.4);
}

.reset-map-control a {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  color: #555;
  text-decoration: none;
}

.reset-map-control a:hover {
  background: #f4f4f4;
}
</style>
