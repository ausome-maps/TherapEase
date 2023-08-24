<template>
    <div class="tile flex overflow-ellipsis w-full py-2 overflow-hidden">
        <div class="w-[250px] h-[200px] relative">
            <NuxtLink :to="`/details-page?id=${facilityData.id}`">
                <img class="tile-image object-cover rounded-[15px] h-full sm:min-w-[150px] md:min-w-[165px] lg:min-w-[230px] xl:min-w-[250px]"
                    :src="imageSource" :alt="facilityData.properties.placename" style="width:260px;" />
            </NuxtLink>
        </div>
        <div class="ml-5 flex flex-col justify-center w-full overflow-hidden">
            <NuxtLink :to="`/details-page?id=${facilityData.id}`" class="overflow-hidden">
                <div class="flex">
                    <div class="icons">
                        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%"
                            height="100%" viewBox="0 0 72 72" fill="none">
                            <path d="M72 0H0V72H72V0Z" fill="url(#pattern0)" />
                            <defs>
                                <pattern id="pattern0" patternContentUnits="objectBoundingBox" width="1" height="1">
                                    <use xlink:href="#image0_527_2498" transform="scale(0.01)" />
                                </pattern>
                                <image id="image0_527_2498"
                                    xlink:href="data:image/png;base64,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" />
                            </defs>
                        </svg>
                    </div>
                    <h2 class="overflow-hidden overflow-ellipsis tracking-tight text-gray-900 w-full">
                        {{ facilityData.properties.address }}</h2>
                </div>
                <h3 class="overflow-hidden overflow-ellipsis font-semibold tracking-tight text-gray-900 w-full">
                    {{ facilityData.properties.placename }}</h3>
                <div class="flex mt-1 gap-1">
                    <div class="icons">
                        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%"
                            height="100%" viewBox="0 0 16 17" fill="none">
                            <path d="M15.424 0.286621H0.0864258V16.7197H15.424V0.286621Z" fill="url(#pattern1)" />
                            <defs>
                                <pattern id="pattern1" patternContentUnits="objectBoundingBox" width="1" height="1">
                                    <use xlink:href="#image0_531_2507"
                                        transform="matrix(0.01 0 0 0.00933333 0 0.0333333)" />
                                </pattern>
                                <image id="image0_531_2507" width="100" height="100"
                                    xlink:href="data:image/png;base64,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" />
                            </defs>
                        </svg>
                    </div>
                    <h2 class="overflow-hidden overflow-ellipsis tracking-tight text-gray-900 w-full">
                        {{ servicesWithNonZeroModeLength }} interventions on offer</h2>
                </div>

            </NuxtLink>
            <div class="justify-center flex mt-5">
                <button @click="openModal(index)"><svg class="arrow_down" xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink" width="22" height="20" viewBox="0 0 22 20" fill="none">
                        <path d="M22 0H0V20H22V0Z" fill="url(#arrow_down)" />
                        <defs>
                            <pattern id="arrow_down" patternContentUnits="objectBoundingBox" width="1" height="1">
                                <use xlink:href="#image0_540_2520" transform="matrix(0.00909091 0 0 0.01 0.0454545 0)" />
                            </pattern>
                            <image id="image0_540_2520" width="100" height="100"
                                xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAABWklEQVR4nO3bPWoDMRCG4WlziWBys+ly6ASzB3GcxoIU+QHbMZ9WzwvbqpiHKVagKkmSJEmSJEmSJEmSJEmSVE9mkDPD56p6q6rXex24YF1Vx6p6uQfGe1Wdq+oDytUYp8sMt1tQvmKMD8r1GOdbUL7DgHI7xtUov4HYlNsw/mVLoDwYYwQlCGMEJQhjBCUIYwQlCGMEJQhjBCUIY7Q6SidhrI7SiRironQyxmooPQPGKig9E8beUXpGjL2i9MwYe0PpPWDsBaX3hDE7Su8RY1aU3jPGbCi9AsYsKL0SRjpKr4iRitIrY6ShNIwclIaRg9IwclAaRg5Kw8hBaRg5KA0jB6Vh5KA0jByUhpGD0jByUBpGDkrDeFyHyzvvn1BOf9zaHi9n6IGbcl75Cn0WlA1GDsoGIwdlg5GDssHIQdlg5KBsMHI6+M+QJEmSJEmSJEmSJEmSJKny+wQrgMS1KLj4wAAAAABJRU5ErkJggg==" />
                        </defs>
                    </svg></button>
            </div>

            <!-- Rear view of the tile  -->
            <transition name="slide">
                <div v-if="showModal" class="inset-0 rounded-[15px] flex overflow-y-auto bg-white ease-in-out absolute">
                    <div class="slide-enter-active slide-leave-active w-full">
                        <div class="grid-cols-3 grid h-full w-full">
                            <div class="col-span-2">
                                <header class="text-black px-4 w-full">
                                    <div class="mt-5 flex">
                                        <svg @click="closeModal" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                            viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                            stroke-linecap="round" stroke-linejoin="round"
                                            class="cursor-pointer feather feather-arrow-left">
                                            <polyline points="12 19 5 12 12 5"></polyline>
                                        </svg>
                                        <div>
                                            <div class="flex">
                                                <div class="icons">
                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                        xmlns:xlink="http://www.w3.org/1999/xlink" width="100%"
                                                        height="100%" viewBox="0 0 72 72" fill="none">
                                                        <path d="M72 0H0V72H72V0Z" fill="url(#pattern0)" />
                                                        <defs>
                                                            <pattern id="pattern0" patternContentUnits="objectBoundingBox"
                                                                width="1" height="1">
                                                                <use xlink:href="#image0_527_2498"
                                                                    transform="scale(0.01)" />
                                                            </pattern>
                                                            <image id="image0_527_2498"
                                                                xlink:href="data:image/png;base64,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" />
                                                        </defs>
                                                    </svg>
                                                </div>
                                                <h2
                                                    class="overflow-hidden overflow-ellipsis tracking-tight text-gray-900 w-full">
                                                    {{ facilityData.properties.address }}</h2>
                                            </div>
                                            <h3
                                                class="overflow-hidden overflow-ellipsis font-semibold tracking-tight text-gray-900 w-full">
                                                {{ facilityData.properties.placename }}</h3>
                                        </div>
                                    </div>
                                </header>
                                <div class="flex mt-1 gap-1 px-5">
                                    <div class="icons">
                                        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                            width="100%" height="100%" viewBox="0 0 16 17" fill="none">
                                            <path d="M15.424 0.286621H0.0864258V16.7197H15.424V0.286621Z"
                                                fill="url(#pattern1)" />
                                            <defs>
                                                <pattern id="pattern1" patternContentUnits="objectBoundingBox" width="1"
                                                    height="1">
                                                    <use xlink:href="#image0_531_2507"
                                                        transform="matrix(0.01 0 0 0.00933333 0 0.0333333)" />
                                                </pattern>
                                                <image id="image0_531_2507" width="100" height="100"
                                                    xlink:href="data:image/png;base64,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" />
                                            </defs>
                                        </svg>
                                    </div>
                                    <h2 class="overflow-hidden overflow-ellipsis tracking-tight text-gray-900 w-full">
                                        {{ servicesWithNonZeroModeLength }} interventions on offer</h2>
                                </div>
                            </div>
                            <div class="flex flex-col ">
                                <h2 class="mt-5 font-extrabold">Contact Information</h2>
                                <div class="h-full flex flex-col justify-end">
                                    <div class="flex justify-end">
                                        <button class="bg-black px-5 py-2 rounded-tl-[15px]">
                                            <h2 class="text-white ">More Details</h2>
                                        </button>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import placeholder from "assets/images/ausome_placeholder.png"

export default {
    data() {
        return {
            image_placeholder: placeholder,
            showModal: false,
            loading: false,

        }
    },

    props: {
        facilityData: {
            type: Object,
            required: true
        }
    },
    methods: {
        openModal(index) {
            this.showModal = true;
        },
        closeModal() {
            this.showModal = false;
        },
        handleImageError() {
      this.loading = false;
      console.error('Image failed to load.');
    },
    handleImageLoad() {
      this.loading = false;
      console.log('Image loaded successfully.');
    },
    
},
  computed: {
    imageSource() {
  let image = this.facilityData.properties.images.find(img => img.img_url && img.img_url.trim() !== "");
  return image ? image.img_url : this.image_placeholder;
},servicesWithNonZeroModeLength() {
      // Filter services with at least one mode not equal to 0 and calculate the length
      return Object.keys(this.facilityData.properties.services_offered).filter(
        serviceKey =>
          Object.values(this.facilityData.properties.services_offered[serviceKey].mode).some(modeValue => modeValue !== 0)
      ).length;
    }},
mounted() {
    console.log(this.servicesWithNonZeroModeLength)
}

};
</script>



<style scoped>
.tile {
    border-radius: 15px;
    background: #FFF;
    box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
    padding: 5px;
}

.tile-image {

    border-radius: 15px 0px 0px 15px;
}

.right-bottom-button {
    border-radius: 35px 0px 35px 0px;
    text-align: fit-content;
}



.ease-in-out {
    transition: 0.2s;
}

.slide-enter-active {
    transform: translateY(100%);
    opacity: 0;

}

.slide-leave-active {
    transform: translateY(0);
    opacity: 1;
    border: none
}

.slide-leave-to {
    transform: translateY(100%);
    opacity: 0;
}

.arrow_down {
    transform: rotate(180deg);
}


.arrow_down {
    transition: 0.2s;
    transform: rotate(180deg);
}

.slide-leave-to .arrow_down,
.slide-enter-to .arrow_down {
    transform: rotate(0deg);
}




/* Styles for screens larger than 1200px */
@media screen and (min-width: 1300px) {
    h2 {
        font-style: normal;
        font-size: 1rem;
        /* Increase the font-size */
        line-height: 1.4em;
        letter-spacing: 0.2px;
    }

    h3 {
        font-style: normal;
        font-size: 1.6rem;
        /* Increase the font-size */
        font-weight: 700;
        line-height: 1.12em;
        letter-spacing: 0.2px;
    }

    .icons {
        width: 1rem;
        padding-bottom: 2px;
        margin-right: 2px;
    }
}

/* Styles for screens smaller than 1200px but larger than 768px */
@media screen and (min-width: 768px) and (max-width: 1299px) {
    h2 {
        font-style: normal;
        font-size: 0.5rem;
        /* Adjust the font-size */
        line-height: 1.4em;
        letter-spacing: 0.2px;
    }

    h3 {
        font-style: normal;
        font-size: 1rem;
        /* Adjust the font-size */
        font-weight: 700;
        line-height: 1.12em;
        letter-spacing: 0.2px;
    }

    .icons {
        width: 0.5rem;
        padding-bottom: 2px;
        margin-right: 2px;
    }
}

@media screen and (max-width: 767px) {
    h2 {
        font-style: normal;
        font-size: 0.5rem;
        /* Adjust the font-size */
        line-height: 1.4em;
        letter-spacing: 0.2px;
    }

    h3 {
        font-style: normal;
        font-size: 1rem;
        /* Adjust the font-size */
        font-weight: 700;
        line-height: 1.12em;
        letter-spacing: 0.2px;
    }

    .icons {
        width: 0.5rem;
        padding-bottom: 2px;
        margin-right: 2px;
    }

}

.badge {
    border-radius: 35px 0px 0px 35px;
}
</style>


  



<!-- <template>
    <div class="tile flex overflow-ellipsis w-full py-2">
        <div class="w-[250px] relative">
            <a :href="facilityData.facilityUrl">
                <img class="tile-image object-cover rounded-[10px] h-full sm:min-w-[150px] md:min-w-[165px] lg:min-w-[230px] xl:min-w-[250px]"
                    :src="facilityData.facilityImage" :alt="facilityData.facilityName" style="width:260px;" />
            </a>
        </div>
        <div class="ml-5 flex flex-col justify-center w-full overflow-hidden">
            <a :href="facilityData.facilityUrl" class="overflow-hidden">
                <div class="flex">
                    <div class="icons">
                        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%"
                            height="100%" viewBox="0 0 72 72" fill="none">
                            <path d="M72 0H0V72H72V0Z" fill="url(#pattern0)" />
                            <defs>
                                <pattern id="pattern0" patternContentUnits="objectBoundingBox" width="1" height="1">
                                    <use xlink:href="#image0_527_2498" transform="scale(0.01)" />
                                </pattern>
                                <image id="image0_527_2498"
                                    xlink:href="data:image/png;base64,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" />
                            </defs>
                        </svg>
                    </div>
                    <h2 class="overflow-hidden overflow-ellipsis tracking-tight text-gray-900 w-full">
                        {{ facilityData.facilityLocation }}</h2>
                </div>
                <h3 class="overflow-hidden overflow-ellipsis font-semibold tracking-tight text-gray-900 w-full">
                    {{ facilityData.facilityName }}</h3>
                <div class="flex mt-1 gap-1">
                    <div class="icons">
                        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%"
                            height="100%" viewBox="0 0 16 17" fill="none">
                            <path d="M15.424 0.286621H0.0864258V16.7197H15.424V0.286621Z" fill="url(#pattern1)" />
                            <defs>
                                <pattern id="pattern1" patternContentUnits="objectBoundingBox" width="1" height="1">
                                    <use xlink:href="#image0_531_2507"
                                        transform="matrix(0.01 0 0 0.00933333 0 0.0333333)" />
                                </pattern>
                                <image id="image0_531_2507" width="100" height="100"
                                    xlink:href="data:image/png;base64,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" />
                            </defs>
                        </svg>
                    </div>
                    <h2 class="overflow-hidden overflow-ellipsis tracking-tight text-gray-900 w-full">
                        {{ facilityData.services.length - 1 }} interventions on offer</h2>
                </div>

            </a>
            <div class="justify-center flex mt-5">
                <button><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="22"
                        height="20" viewBox="0 0 22 20" fill="none">
                        <path d="M22 0H0V20H22V0Z" fill="url(#arrow_down)" />
                        <defs>
                            <pattern id="arrow_down" patternContentUnits="objectBoundingBox" width="1" height="1">
                                <use xlink:href="#image0_540_2520" transform="matrix(0.00909091 0 0 0.01 0.0454545 0)" />
                            </pattern>
                            <image id="image0_540_2520" width="100" height="100"
                                xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAABWklEQVR4nO3bPWoDMRCG4WlziWBys+ly6ASzB3GcxoIU+QHbMZ9WzwvbqpiHKVagKkmSJEmSJEmSJEmSJEmSVE9mkDPD56p6q6rXex24YF1Vx6p6uQfGe1Wdq+oDytUYp8sMt1tQvmKMD8r1GOdbUL7DgHI7xtUov4HYlNsw/mVLoDwYYwQlCGMEJQhjBCUIYwQlCGMEJQhjBCUIY7Q6SidhrI7SiRironQyxmooPQPGKig9E8beUXpGjL2i9MwYe0PpPWDsBaX3hDE7Su8RY1aU3jPGbCi9AsYsKL0SRjpKr4iRitIrY6ShNIwclIaRg9IwclAaRg5Kw8hBaRg5KA0jB6Vh5KA0jByUhpGD0jByUBpGDkrDeFyHyzvvn1BOf9zaHi9n6IGbcl75Cn0WlA1GDsoGIwdlg5GDssHIQdlg5KBsMHI6+M+QJEmSJEmSJEmSJEmSJKny+wQrgMS1KLj4wAAAAABJRU5ErkJggg==" />
                        </defs>
                    </svg></button>
            </div>
        </div>
    </div>
</template> -->
