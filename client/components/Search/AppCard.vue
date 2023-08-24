<template>
  <div class="relative overflow-ellipsis w-full min-h-[180px] sm:min-h-[250px] max-w-[80vw] lg:min-h-[250px] ">
    <NuxtLink :to="`/details-page?id=${facilityData.id}`">
      <div v-if="loading">
        <!-- Skeleton -->
        <div class="animate-pulse bg-gray-200 h-[220px] rounded-[15px]"></div>
      </div>
      <img v-else class="object-cover mx-auto rounded-[15px] h-[220px] min-w-full sm:w-auto" :src="imageSource"
        :alt="facilityData.properties.placename" @load="handleImageLoad" @error="handleImageError" />
    </NuxtLink>
    <div class="px-5 pb-5">
      <NuxtLink :to="facilityData.properties.url">
        <h5
          class="w-full whitespace-nowrap overflow-hidden overflow-ellipsis font-semibold tracking-tight text-gray-900 ">
          {{ facilityData.properties.placename }}</h5>
      </NuxtLink>
    </div>
  </div>
</template>


<script>
import placeholder from "assets/images/ausome_placeholder.png"
export default {
  props: {
    facilityData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      image_placeholder: placeholder,
      loading: false // Add loading state
    }
  },
  computed: {
    imageSource() {
      let image = this.facilityData.properties.images.find(img => img.img_url && img.img_url.trim() !== "");
      return image ? image.img_url : this.image_placeholder;
    },
  },
  methods: {
    handleImageError() {
      this.loading = false;
      console.error('Image failed to load.');
    },
    handleImageLoad() {
      this.loading = false;
      console.log('Image loaded successfully.');
    },
  },
};
</script>
