<template>
  <div>
    <div class="relative ">
  <div class="grid grid-cols-3 gap-3">
    <div v-for="(image, index) in images.slice(0, 3)" :key="index" class="cursor-pointer">
      <img
        :src="image"
        :alt="image.alt"
        :class="[
          'w-full',
          'h-[350px]',
          'object-cover',
          { 'rounded-l-xl': index === 0 },
          { 'rounded-r-xl': index === 2 },
        ]"
        @click="openModal(index)"
      />
    </div>
  </div>
  <!-- Align button to right -->
  <div class="absolute bottom-[20px] right-0 pr-[30px]">
    <span @click="openModal(index)" class="shadow-xl text-red-400 h-10 w-40 flex items-center justify-center bg-white rounded-3xl transition-colors duration-300 hover:bg-red-400 hover:text-white cursor-pointer">
  View All Images
</span>
  </div>



    </div>

    <transition name="slide ">
      <div v-if="showModal" class="fixed inset-0 flex justify-center overflow-y-auto bg-white transition ease-in-out">
        <div class="slide-enter-active slide-leave-active w-8xl">
          <header class="text-black text-2xl cursor-pointer border h-6 flex items-center px-4 w-full" @click="closeModal">
            <span>&larr; Go Back</span>
          </header>
          <div class="grid grid-cols-4 gap-2 mt-4 px-4 ">
            <div v-for="(image, index) in images" :key="index" class="">
              <img :src="image" :alt="image.alt" class="rounded-xl object-cover h-[100%] w-[100%]" @click="openModal(index)" />
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

  
  
  
<script>
export default {
  props: {
    images: {
      type: Array,
      required: true,
    },
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
    },
    closeModal() {
      this.showModal = false;
    },
    setCurrentImage(index) {
      this.currentImageIndex = index;
    },
  },
};
</script>
  
<style scoped>
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
  