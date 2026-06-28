<template>
  <div class="map-wrapper w-full rounded-lg overflow-hidden border border-gray-200" style="height: 320px">
    <LMap
      ref="mapRef"
      class="h-full w-full"
      :zoom="zoom"
      :center="center"
      :use-global-leaflet="false"
      @ready="onMapReady"
      @click="onMapClick"
    >
      <LTileLayer
        :url="tileUrl"
        :attribution="attribution"
        layer-type="base"
        name="OpenStreetMap"
      />
      <LMarker
        v-if="markerLatLng"
        :lat-lng="markerLatLng"
        :draggable="!readonly"
        :icon="markerIcon"
        @update:latLng="onMarkerDrag"
        @moveend="onMarkerDrag"
      />
    </LMap>
  </div>
  <p v-if="!readonly" class="text-xs text-gray-400 mt-1">
    Click on the map or drag the marker to set the location.
  </p>
  <div v-if="coordinates" class="mt-1 text-xs text-gray-500">
    <span class="font-medium">Lat:</span> {{ coordinates[1]?.toFixed(5) }},
    <span class="font-medium">Lng:</span> {{ coordinates[0]?.toFixed(5) }}
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'

globalThis.L = L

const props = defineProps<{
  coordinates: number[]
  readonly?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:coordinates', value: number[]): void
}>()

const mapRef = ref<any>(null)
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const zoom = ref(13)

const markerIcon = computed(() => {
  return L.divIcon({
    className: 'picker-marker-icon',
    iconSize: [24, 33],
    iconAnchor: [12, 33],
    popupAnchor: [0, -30],
    html: `<svg width="24" height="33" viewBox="0 0 24 33" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 0C5.37 0 0 5.37 0 12c0 8.5 12 21 12 21s12-12.5 12-21C24 5.37 18.63 0 12 0z" fill="#ef4444" stroke="#b91c1c" stroke-width="1.5"/>
      <circle cx="12" cy="12" r="4.5" fill="white"/>
    </svg>`,
  })
})

const center = computed(() => {
  if (props.coordinates && props.coordinates.length === 2) {
    return [props.coordinates[1], props.coordinates[0]] as [number, number]
  }
  return [12.8797, 121.7740] as [number, number]
})

const markerLatLng = computed(() => {
  if (props.coordinates && props.coordinates.length === 2) {
    return [props.coordinates[1], props.coordinates[0]] as [number, number]
  }
  return null
})

const onMapReady = () => {
  nextTick(() => {
    requestAnimationFrame(() => {
      const mapObject = mapRef.value?.leafletObject
      if (mapObject) {
        mapObject.invalidateSize()
      }
    })
  })
}

const onMapClick = (e: any) => {
  if (props.readonly) return
  const latlng = e.latlng
  if (latlng) {
    emit('update:coordinates', [latlng.lng, latlng.lat])
  }
}

const onMarkerDrag = (e: any) => {
  if (props.readonly) return
  let latlng = null
  if (e && typeof e.lat === 'number' && typeof e.lng === 'number') {
    latlng = e
  } else if (e?.latlng) {
    latlng = e.latlng
  } else if (e?.target?.getLatLng) {
    latlng = e.target.getLatLng()
  }
  if (latlng) {
    emit('update:coordinates', [latlng.lng, latlng.lat])
  }
}

watch(() => props.coordinates, () => {
  requestAnimationFrame(() => {
    const mapObject = mapRef.value?.leafletObject
    if (mapObject && props.coordinates?.length === 2) {
      mapObject.panTo([props.coordinates[1], props.coordinates[0]])
    }
  })
}, { deep: true })
</script>

<style scoped>
.map-wrapper :deep(.leaflet-container) {
  height: 100% !important;
  width: 100% !important;
  background: #f0f0f0;
}

.picker-marker-icon {
  background: transparent !important;
  border: none !important;
}
</style>
