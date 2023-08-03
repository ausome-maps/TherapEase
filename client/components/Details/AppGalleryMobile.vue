<template>
  <div class="max-w-2xl p-4 mx-auto">
    <div class="relative">
      <!-- Carousel wrapper -->
      <div class="relative h-56 overflow-hidden rounded-3xl sm:h-64 xl:h-80 2xl:h-96">
        <!-- Render carousel items based on the images prop -->
        <div v-for="(image, index) in images" :key="index" :id="'carousel-item-' + (index + 1)" class="hidden">
          <span class="absolute text-2xl font-semibold text-white -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 sm:text-3xl dark:text-gray-800">Slide {{ index + 1 }}</span>
          <img :src="image.img_url" :alt="image.img_name" class="absolute block w-full -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2" alt="...">
        </div>
      </div>

      <!-- Slider indicators -->
      <div class="absolute z-30 flex space-x-3 -translate-x-1/2 bottom-5 left-1/2">
        <button v-for="(image, index) in images" :key="index" :id="'carousel-indicator-' + (index + 1)" type="button" class="w-3 h-3 rounded-full" :aria-current="index === activeIndex ? 'true' : 'false'" :aria-label="`Slide ${index + 1}`"></button>
      </div>

      <!-- Slider controls -->
      <button id="data-carousel-prev" type="button" class="absolute top-0 left-0 z-30 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none" @click="prevSlide">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-full sm:w-10 sm:h-10 bg-white/30 dark:bg-gray-800/30 group-hover:bg-white/50 dark:group-hover:bg-gray-800/60 group-focus:ring-4 group-focus:ring-white dark:group-focus:ring-gray-800/70 group-focus:outline-none">
          <svg class="w-5 h-5 text-white sm:w-6 sm:h-6 dark:text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          <span class="hidden">Previous</span>
        </span>
      </button>
      <button id="data-carousel-next" type="button" class="absolute top-0 right-0 z-30 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none" @click="nextSlide">
        <span class="inline-flex items-center justify-center w-8 h-8 rounded-full sm:w-10 sm:h-10 bg-white/30 dark:bg-gray-800/30 group-hover:bg-white/50 dark:group-hover:bg-gray-800/60 group-focus:ring-4 group-focus:ring-white dark:group-focus:ring-gray-800/70 group-focus:outline-none">
          <svg class="w-5 h-5 text-white sm:w-6 sm:h-6 dark:text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
          <span class="hidden">Next</span>
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue'
import { Carousel } from 'flowbite'

// Declare a prop for the images
const props = defineProps({
  images: {
    type: Array,
    required: true
  }
})

const activeIndex = ref(0)

onMounted(() => {
  const items = props.images.map((image, index) => ({
    position: index,
    el: document.getElementById(`carousel-item-${index + 1}`)
  }));

  const indicatorItems = props.images.map((_, index) => ({
    position: index,
    el: document.getElementById(`carousel-indicator-${index + 1}`)
  }));

  const options = {
    defaultPosition: 1,
    indicators: {
      activeClasses: 'bg-white dark:bg-gray-800',
      inactiveClasses: 'bg-white/50 dark:bg-gray-800/50 hover:bg-white dark:hover:bg-gray-800',
      items: indicatorItems
    },

    // callback functions
    onNext: () => {
      console.log('next slider item is shown');
    },
    onPrev: () => {
      console.log('previous slider item is shown');
    },
    onChange: () => {
      console.log('new slider item has been shown');
    }
  };

  if (document.getElementById('carousel-item-1')) {
    const carousel = new Carousel(items, options);

    // set event listeners for prev and next buttons
    const prevButton = document.getElementById('data-carousel-prev');
    const nextButton = document.getElementById('data-carousel-next');
    prevButton.addEventListener('click', () => {
      carousel.prev();
    });
    nextButton.addEventListener('click', () => {
      carousel.next();
    });
  }
})
</script>
