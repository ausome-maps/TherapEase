<template>
    <!-- <div class="grid grid-cols-2 gap-5 my-5"> -->
        <div class="grid my-5">
        <!-- <div class="flex justify-center">
            <span @click="openModal(index)"
                class="shadow-xl text-black h-[40px] w-[100%] flex items-center justify-center bg-white rounded-3xl transition-colors duration-300 hover:bg-red-400 hover:text-white cursor-pointer">
                Share
            </span>
        </div> -->
        <div class="flex justify-center">
            <a :href="feedbackUrl" target="_blank" rel="noopener noreferrer" class="shadow-xl text-red-400 h-[40px] w-[100%] flex items-center justify-center bg-white rounded-3xl transition-colors duration-300 hover:bg-red-400 hover:text-white cursor-pointer">
                Submit Feedback
        </a>
        </div>
    </div>
</template>
<script>
export default {
    props: {
    feedbackUrl: {
      type: String,
      required: true,
    },
  },
  async mounted() {
    //console.log(this);
  }
}
</script>
