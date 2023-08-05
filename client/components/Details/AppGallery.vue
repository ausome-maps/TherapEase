<template>
  <div>
    <div class="relative ">
      <div class="grid grid-cols-3 gap-3">
        <div v-for="(image, index) in images.slice(0, 3)" :key="index" class="cursor-pointer">
          <img :src="image.img_url" :alt="image.img_name" :class="[
            'w-full',
            'h-[350px]',
            'object-cover',
            { 'rounded-l-xl': index === 0 },
            { 'rounded-r-xl': index === 2 },
          ]" @click="openModal(index)" />
        </div>
      </div>
      <!-- Align button to right -->
      <div class="absolute bottom-[20px] right-0 pr-[30px]">
        <span @click="openModal(index)"
          class="shadow-xl text-red-400 h-10 w-40 flex items-center justify-center bg-white rounded-3xl transition-colors duration-300 hover:bg-red-400 hover:text-white cursor-pointer">
          View All Images
        </span>
      </div>



    </div>

    <transition name="slide">
      <div v-if="showModal" class=".scrollable-element fixed inset-0 w-full z-10 flex justify-center overflow-y-auto bg-white transition ease-in-out">
        <div class="slide-enter-active slide-leave-active w-8xl">
          <header class="text-black text-2xl cursor-pointer border h-6 flex items-center px-4 w-full" @click="closeModal">
            <span>&larr; Go Back</span>
          </header>
          <!-- <div class="grid grid-cols-4 gap-2 mt-4 px-4 ">
            <div v-for="(image, index) in images" :key="index" class="">
              <img :src="image" :alt="image.alt" class="rounded-xl object-cover h-[100%] w-[100%]" @click="openModal(index)" />
            </div>
          </div> -->
          <v-viewer :options="{ navbar: false, toolbar: false, tooltip: true }">
            <div class="grid grid-cols-4 gap-2 mt-4 px-4 ">
              <div v-for="(image, index) in images" :key="index" class="">
                <img :src="image.img_url" :alt="image.img_name" class="rounded-xl object-cover h-[100%] w-[100%]"
                  @click="openModal(index)" />
              </div>
            </div>
          </v-viewer>

        </div>
      </div>
    </transition>
  </div>
</template>

  
  
  
<script>
import 'viewerjs/dist/viewer.css'
import { viewer as VViewer } from 'v-viewer'

export default {
  props: {
    images: {
      type: Array,
      required: true,
    },
  },
  components: {
    VViewer,
  },
  data() {
    return {
      showModal: false,
      currentImageIndex: 0,
    };
  },
  methods: {
  openModal(index) {
    this.showModal = true;
    this.currentImageIndex = index;
    document.body.style.overflow = 'hidden'; // add this line
  },
  closeModal() {
    this.showModal = false;
    document.body.style.overflow = 'auto'; // add this line
  },
  setCurrentImage(index) {
    this.currentImageIndex = index;
  },
},

};
</script>
  
<style scoped>

/* Works on Firefox */
.scrollable-element {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}

/* Works on Chrome, Edge, and Safari */
.scrollable-element::-webkit-scrollbar {
  width: 12px;       
}

.scrollable-element::-webkit-scrollbar-track {
  background: transparent;        
}

.scrollable-element::-webkit-scrollbar-thumb {
  background-color: transparent;    
  border-radius: 20px;               
  border: 3px solid transparent;  
}

.ease-in-out {
  transition: ease 0.3s;
}

.slide-enter-active {
  transform: translateY(100%);
  opacity: 0;
}

.slide-leave-active {
  transform: translateY(0);
  opacity: 1;
}

.slide-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

.slide-enter-to {
  transform: translateY(100%);
  opacity: 1;
}
</style>
  