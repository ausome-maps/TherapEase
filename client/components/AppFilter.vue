<script setup>
import { onMounted } from 'vue'
import { Modal } from 'flowbite'
onMounted(() => {
    const $buttonElement = document.querySelector('#button');
    const $modalElement = document.querySelector('#modal');
    const $closeButton = document.querySelector('#closeButton');
    const modalOptions = {
        backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40'
    }
    if ($modalElement) {
        const modal = new Modal($modalElement, modalOptions);
        $buttonElement.addEventListener('click', () => modal.toggle());
        $closeButton.addEventListener('click', () => modal.hide());

        // programatically show
        // modal.show();
    }
})
</script>

<script>
export default {
    data() {
        return {
            isPASPChecked: false,
            isPAOTChecked: false
        }
    },
    // rest of your component's options...
}
</script>

<style scoped>
.content-body::-webkit-scrollbar,
.content-body::-webkit-scrollbar-thumb {
    width: 8px;
    border-radius: 13px;
    background-clip: padding-box;
    border: 2px solid transparent;
}

.content-body::-webkit-scrollbar-thumb {
    box-shadow: inset 0 0 0 10px;
}
</style>



<template>
    <div>
        <div class="flex justify-center p-4">
            <button id="button" type="button" class="border shadow-md p-2 px-5 active:shadow-sm rounded-3xl">Filter</button>
        </div>
        <div id="modal" tabindex="-1" aria-hidden="true"
            class="fixed top-0 left-0 right-0 z-50 hidden w-full p-2 overflow-x-hidden overflow-y-auto md:inset-0 h-modal md:h-full ">
            <div class="relative w-full h-full max-w-3xl md:h-auto">
                <!-- Modal content -->
                <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                    <!-- Modal header -->
                    <div class="flex justify-center items-start p-4 border-b rounded-t dark:border-gray-600">
                        <h3 class="text-xl font-semibold text-gray-900 lg:text-2xl dark:text-white">
                            Filter
                        </h3>
                        <button id="closeButton" type="button"
                            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto  absolute right-5 inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd"
                                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                    clip-rule="evenodd"></path>
                            </svg>
                        </button>
                    </div>
                    <!-- Modal body -->
                    <div class="content-body px-4 sm:px-10 py-4 space-y-6 overflow-y-auto max-h-[calc(100vh-12rem)]">
                        <h2 class="font-bold">Accreditation</h2>
                        <div class="flex justify-between border-b pb-6">
                            <div>
                                <AppCheckbox label="Philippine Association of Speech Pathologists" id_="PASP" />
                            </div>

                            <div>
                                <AppCheckbox label="Philippine Academy of Occupational Therapist" id_="PAOT"/>
                            </div>
                        </div>
                        <div>
                            <h2 class="font-bold">Mode of Intervention</h2>
                        </div>
                        <div class="flex space-x-2 sm:space-x-4 md:space-x-6 lg:space-x-6 pb-6 border-b">
                            <!-- Teletherapy Button -->
                            <ul>
                                <input type="checkbox" id="teletherapy-option" value="" class="hidden peer" required="">
                            <label for="teletherapy-option"
                                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border shadow-md rounded-md peer-checked:border-black hover:text-gray-600  peer-checked:text-gray-600 ">
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                    width="43" height="43" viewBox="0 0 43 43" fill="none">
                                    <path d="M43 0H0V43H43V0Z" fill="url(#teletherapy_button)" />
                                    <defs>
                                        <pattern id="teletherapy_button" patternContentUnits="objectBoundingBox" width="1"
                                            height="1">
                                            <use xlink:href="#image0_578_1190" transform="scale(0.01)" />
                                        </pattern>
                                        <image id="image0_578_1190" width="100" height="100"
                                            xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAADJUlEQVR4nO2czW9NQRiHH6JF2gjCRtmIHdbWPiqa0AUWdrZ2VtYkPjYSqcTHRiKKf8HOR1LBQipSRG2ECisLWiQNPTK3o5jOvYk5p2feOL8nmaS97Z2e+3vOO3NOOmdACCGEEEIIIYQQQgghhBBC/GIrcB54BkwBhRqdMpjyWQ0BW6o8jZYCl4AfEkDqSeiyuwh0VyHjjkRQ1Whwu6yUy5JB1UPzhTJzRjhMPQB2Aj1lLDeEHmAX8DDI8DuwOaXDoYiM0mNgA+mOSDmX0tHzoBNXGSKN/iDLsZROPgedaJhKpzfI0mX7z4STUcgB4KMmfcKcJoCBhDxLC/kgGbS7knqbQ4ju1OmYgYRg6yTJLqTpFBJiCwkxhoQYQ0KMISHGkBBjSIgxJMQYEmIMCTFGo4WcBJZhi0YLeQLcApZjh8YLKYB7/r9xFpAQZkMYAVbktiEh/HVGPgZWS0jeOaQI2iiwJqMUDVnMD+EFsE5CbFRI4dtLYH0GKaoQ2kt5DWyUEBsVUvj2BthU4zGpQugs5BNwH1glIfkqZBBYCyyhflQhzIZwDbjqv76SQYSE8LtC3DOPi/wzfO77aWCDhNR/2TsKHAteG/HHcVZC6heyLfLaoT+W+q/MIKXRc0i7J5Xe+2M5Sv1ISIQjwGFdZdmokNyoQowhIcaQEGNIiDEkxBgSYgxzQtSQkMLwiVB7hUwY+NCF0ZZl44AB/4dzf/jCWHOZ7FkIIV+DDrT5THWbz3xJ6WQs6MRtxiXS2B1k+TSlk9NBJ24TLm1glrZv5aMgy1MJ/bQWm01HpPQbWnFumV5fGaEMl2lfpzfu01ZLmNpn652Bg1Fj7gpt3lZ+amTLwC3uay1OlgRMZOBW73M9ePFbxrVNTaIvcq/nFv1xMGLqRu6jbQA3I7nvdz/oAl5Ffng89xH/x5yI5D3uXbRwi5RnIr90F9iu+47K7kt2+CeHw5xd9nvDN5wxMKkVDW3RO/fFXkqsUtRYkAxmvAy3YLwtg348kwQWNIPx2DDVji6/lfiwvzaelCDKCpj0WQ77q6m5CVwIIYQQQgghhBBCCCGEEIIG8RNipb2RS8yLQwAAAABJRU5ErkJggg==" />
                                    </defs>
                                </svg>
                                <span class="mt-2">Teletherapy</span>
                            </label>
                        </ul>
                        <ul>

                            <!-- Onsite Button -->
                            <input type="checkbox" id="onsite-option" value="" class="hidden peer" required="">
                            <label for="onsite-option"
                                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border shadow-md rounded-md peer-checked:border-black hover:text-gray-600  peer-checked:text-gray-600 ">
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                    width="34" height="34" viewBox="0 0 34 34" fill="none">
                                    <path d="M34 0H0V34H34V0Z" fill="url(#onsite_button)" />
                                    <defs>
                                        <pattern id="onsite_button" patternContentUnits="objectBoundingBox" width="1"
                                            height="1">
                                            <use xlink:href="#image0_578_1194" transform="scale(0.01)" />
                                        </pattern>
                                        <image id="image0_578_1194" width="100" height="100"
                                            xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAADYklEQVR4nO2b/4sNURjGX+NLdn3Za5GNiIiIiIhsRP5lERERERERERGRa5dr9+661947urVpe7rOnJk975lzOs+n5qc79zk772feOWfmzooQQgghhBBCSPzkNW69ug8+RCgkMCgkMCgkcCGaZJxDKCQ62CGBQSGRCinar2mRs5w5pM7Fh/bcajzQqvs1KYRCcnYIO0SdWCb13PM1Pfg5xAUZhVBIVdghBfCSVbIguedlb9X92ks+azsYzzmuDjSnEAoZBjtkEXaII1Jb9jZEZNPi1vAwXmlSE2ILhRRAIQpk7JD0Lll5KvchLsgohEIQdsgS2CEJXrJcwTmkAApRIGOHFMNLlkJd8MzzvfUjug/JfdyHrKhZSG75dyYjZFgAhUi9QgZnG4VIOB2yAAErRZc+jDe4bBaR1CqrCwGrRZc+hZjpQIHWKAvpwXiDs7+IpDpkHgLWii49CjEzBwUasTS/pcK/FVSds7KUlr2zELDOciAKURIyAwHrlYX8gf1WWfyNSXVICwI2Wg5EIUpCfkLAmOjSrbDMTmqVNQ0BgxfBNOlSiJkpKNC4spBOhfuepDqkWTA3uKZDIWa+QYG2Kk7qIT/uz0N56+QrBGxTXmXlFGLmCxRogkKk1g75DAHblYX02SFmPkGBdogufctnZ66IbpX1EQJ2it+nvSPK40Un5AME7BJdFijEzHso0G7PQkaVx4uuQ95BwB7PDxdHKx6Yq/uL4FZZbyFgr7KQbsXfX8p+Hq2QNxCwz3IgClES8hoC9isL6VT8Qazs59F2yCsIOCC6/LYU4oplF8j3eC8h4KD4FbJBebzohLyAgEOiyzyFmHkOBTqsLGTO8jf8ZDvkGQQcEV3alkKSndSfQsBR8Stk7D/7JSvkCQQcE11mKcTMYyjQcWUhMxRi5hEU6IRnIQ3l8aKb1B9CwEnR5ReFmHkABTqlLKTl+cW86DrkPgScFl1aFGLmHhTojGVhbZeBRe8SjyufeS6+1/Qw3j/uQsBZZSE/KMTMHSjQpGchmy2/l0yH3IaAc8pCpinEzC0o0HllIVMVX+5OpkNuQsAFy+9RiJKQGxBwUVnId8u37ZPtkOsQcElZSJNCzFwbYpWbOKtBaa5SgGiegKW5QiESlJDLFCJBCSGEEEIIIYQQUeAviEHyq6Ws1NIAAAAASUVORK5CYII=" />
                                    </defs>
                                </svg>
                                <span class="mt-2">Onsite</span>
                            </label>
                        </ul>
                        <ul>

                        
                            <!-- Home Service Button -->
                            <input type="checkbox" id="homeservice-option" value="" class="hidden peer" required="">
                            <label for="homeservice-option"
                                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border shadow-md rounded-md peer-checked:border-black hover:text-gray-600  peer-checked:text-gray-600 ">
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                    width="41" height="41" viewBox="0 0 41 41" fill="none">
                                    <path d="M41 0H0V41H41V0Z" fill="url(#homeservice_button)" />
                                    <defs>
                                        <pattern id="homeservice_button" patternContentUnits="objectBoundingBox" width="1"
                                            height="1">
                                            <use xlink:href="#image0_578_1199" transform="scale(0.01)" />
                                        </pattern>
                                        <image id="image0_578_1199" width="100" height="100"
                                            xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAADHElEQVR4nO2av2oVQRSHPy6ECIaApeIDBNRSrdL4AAaSPEXyFKYwZbQztenT5BEsfAExplMESwkR1MaRhS0uw2bvzp27u2fO/j4YWO7snzPz7ezsnL0ghBBCCCGEEHYIKvTZBxKCrZtMQhhfgoTgWIjIQ0KMISHGkBBjSIgxJMQYEmIMCTGGhBhDQowhIcaQEGNMSsijulhmMkJmwAfgY71tlckIOZyL8QC7TELIA+DnXIzXwENsMgkh5w1xXmAT90L2Wr7G7WIP10I2ge8tQn4A97CFayGnUWx/6zL/W7WPJdwK2Qb+RbG9Ao6i36p9XmAHl0LWgU9RXF+AOwvqLOBSyNGCUXDb6LGAOyFbwJ8opncd5xcLaRVXQmZ1eqTLm1TTG5iFtIorIYeJa42mNcrYaRU3Qu5H6ZGuq/F4FT92WsWNkPMlO3ZZkX3hQshe5qMn9VHXJ8UL2VzB5JzyMtA3xQs5XdHra9fX5b4pWsj2ihd4FtIqxQpZ7yEFYiGtUqyQo57u5rHTKkUK2er5eT9mWqU4IbMB3ojGTKusXMgYZXfgT79DlmTGDviCYf8cISEtnXDdc96pKa0iIS2dcED/HJQm5DZ6O7ETBu8fCWlHQowhIcaQEGNIiDEkxBgSYgxzQoZYMK0B+8AZ8Bn4BdzU22d13dqS7cmNd3JCdoCrDue5qvdNbY+EdBQyA44TO6z6IPV6QXpdQpYcIccZnVdJkZCOj6AuQnYaPr/+Bk6AZ8DdulTbb+q6eKS8zLh+yv7m55Dc8601zBlfgcct53wCfGuYU5omeglJ7JD9hpHRJmNeSvx9vjqXhGQKOYvqq8dUV95Gx76XkHwhl1H90wQhz6NjL5e4fur+7ueQm6h+IyHWjejYmwHidS8kZDawtHjdNzAUFq/7BobC4nXfwFBYvMmkBpRaxhYydrzuGxgKi9d9A0Nh8bpvYCgs3mSGvmDoWciqkZAFSMiKCRohvu64UFi85i8YJERCctAIcTaizV8w6JElITlohDgb0dkXVCEptSIhjHvTSAi2Rq2EMDEhQgghhBBCCEEG/wGEVRusmtYuggAAAABJRU5ErkJggg==" />
                                    </defs>
                                </svg>
                                <span class="mt-2">Home Service</span>
                            </label>
                        </ul>
                        </div>
                        <div>
                            <h2 class="font-bold">Type of Session</h2>
                        </div>
                        <div class="flex space-x-2 sm:space-x-4 md:space-x-6 lg:space-x-6 pb-6 border-b">
                            <!-- Individual Button -->
                            <ul>

                            <input type="checkbox" id="individual-option" value="" class="hidden peer" required="">
                            <label for="individual-option"
                                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border shadow-md rounded-md peer-checked:border-black hover:text-gray-600  peer-checked:text-gray-600 ">
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                    width="40" height="40" viewBox="0 0 40 40" fill="none">
                                    <path d="M40 0H0V40H40V0Z" fill="url(#individual_icon)" />
                                    <defs>
                                        <pattern id="individual_icon" patternContentUnits="objectBoundingBox" width="1"
                                            height="1">
                                            <use xlink:href="#image0_580_1206" transform="scale(0.01)" />
                                        </pattern>
                                        <image id="image0_580_1206" width="100" height="100"
                                            xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFZUlEQVR4nO2dXYhWRRjHf+2qa2VY5GYEfZDdRCRZ9qEUFBWF0EVkEFmBRSxlddOHkZTRpykFFYagGUofNxlYXSh2VRRBXfQlQlhaVKSxWmm1a+rEE7Px9uycd3Xfc87Mnnl+MLDs7jvzP//nPefMmXlmDhiGYRiGYRhGNzAbWASsAzYDu4B9vsjPX/m/PQTMgn8/Y5TMqcAy4EfAHWaRzywFTrGodM5UYJX/9rsOi9SxEjjBAjM6bgF2lxAIXeSydpMF5dCZAKwewdA1wHxgJjAFGO9Lr/+d/G2t/9+ielb6zxhtOBrYWGDgF8CNQM9hOCj/Ow/4sqDODb5No+DM2Bgw7TegD+jqwDXpad3h6woFxc6UAKsDZn0GTCvx63uGP9NCly9D3cCdKh8Akytw6Vjgw0B7cmkzfNd2V+DMmFyhO9IR2Kba7PedguxZFbhnTKvBlenAHtX2ityjcTIwqEzpq7H9BYGHRxkVyJZlga5tV43td/uxr1YNS8iU7sDY1LwIOm5WGn6o+UuRDLMDT+A9EXRMBH5VWi4kQxYpE9ZE1PKq0vIgGfKWMmF+RC23KS1vkiGblQkzI2q5QGmRsa/s6FcmTImopVdp+YUM0c8fEyJq6VFaBsgQPZYUm9T0kLsBLjE95G6AS0wPuRvgEtND7ga4xPSQuwEuMT3kboBLTA+5G+AS00PuBrjE9JC7AS4xPeRugEtMD7kb4BLTUzsDyoCJEbUcqbT8SYbsUCacGFHLSUrLT2SIToC+KKH5fcl+yY43lAl3RtRyt9Iic+zZsVCZsC6h+f37yZBzlAl/RFqrMcnfxFu1SJppluiE57sSuFx9Q8Y8rMzYVnOynLS1XWmQfLFs6Q1cLh6psf1HA88fMbNfkmCJMmUAOLeGds8LPJw+XUO7yTMpkHT9nV/IUxVS9/eBJGvRYgBXAweUQVv8E3QVwdAPpdL2VRaJ//NkYIBPejwzSjRKLoXfBtp5woIxnC6/2F+b9Zdf6dQpC3xdLpB1n+V6kENhHPB6wLQyhsNDdb7m2zTacATweA0Becy3ZYzSwE7JfgIqNQNd7jOCneIsIGnhLCBp4SwgaeEsIGnhLCBp4SwgaeEsIOlwZWDbjU7RO5xeXEKdjafLDwLqiaN3S6h7g6pzj989woZP2pwVnwYuVQdK+jZfXjDA+DFwRQn1NwLJ5721YGNK58sDFc+5DJXPvZYYOxJFZ6pPMND5va6lyJZJcyto+/ZAYkVr+RlYnMuW5NP9drD6HqEvUWv99n9VcSbwThsNQxNjLwNn0zDkpjkH2DSCAYM+EHVmDV4CrA/M57eWg177nCZ0AORm+ckIgZBdSJ+v+IwYidO9hr0jaJV73fVjMTDyLX9/hIOTBIZ7Eku9Oc4ngesUIV0+8nldySPmPgv83eZgZFfp6xJ/88144AbfJS46jv3Acr9TdrLZ7F+3OYD1kRfljJZZXvvBguPanuJx9RWk2Eh5ryG7fJ7f5lUasgHzvSS68KZ1nZ5sst80rgksoxgqy2Pf8JcWCHsFOIbmchTwUsGxr4iVeHdfQMzehp4VRcwteEmMjELUfqPbFxjqkNWsuTED2Bkzeft4n7rfKmB35H13Y3NWICg7Kl5S8R/62indwWvraDhxLvPPJrW+Sum0wEPfi1U3OobQnZz9Vb+c5jnV4O+2Jm/Y0IueKn6BihgXmL94pqrGxjBPKY92VrXk4dJA906GS4zhA6vaJ/GudBarRrZW0UhD2FrHUu+3VSOyeYwRRq8Ck8HJ0tlSYfJB01iovJJ3pZROFa/SzqX0VxGQMl4yn2sZrCIgsQ/KjfFiAaHhATEMwzAMwzAMw6AE/gE10plSBoXPogAAAABJRU5ErkJggg==" />
                                    </defs>
                                </svg>
                                <span class="mt-2 px-2">Individual</span>
                            </label>
                        </ul>

                            <!-- Group Button -->
                            <input type="checkbox" id="group-option" value="" class="hidden peer" required="">
                            <label for="group-option"
                                class="active:shadow-sm flex flex-col items-center justify-center w-[165px] h-[85px] sm:p-2 sm:px-8 border shadow-md rounded-md peer-checked:border-black hover:text-gray-600  peer-checked:text-gray-600 ">
                                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                    width="41" height="41" viewBox="0 0 41 41" fill="none">
                                    <path d="M41 0H0V41H41V0Z" fill="url(#group_button)" />
                                    <defs>
                                        <pattern id="group_button" patternContentUnits="objectBoundingBox" width="1"
                                            height="1">
                                            <use xlink:href="#image0_581_1210" transform="scale(0.01)" />
                                        </pattern>
                                        <image id="image0_581_1210" width="100" height="100"
                                            xlink:href="data:image/png;base64,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" />
                                    </defs>
                                </svg>
                                <span class="mt-2 px-2">Group</span>
                            </label>



                        </div>
                        <div>
                            <h2 class="font-bold">Interventions</h2>
                        </div>
                        <div class="grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-2">
                            <!-- Individual Button -->
                            <AppCheckbox label="Speech-Language Therapy" id_="SLT"/>
                            <AppCheckbox label="Physical Therapy" id_="PT" />
                            <AppCheckbox label="ABA Therapy" id_="ABA"/>
                            <AppCheckbox label="Speech-Language Therapy" id_="SLT" />
                            <AppCheckbox label="Speech-Language Therapy" id_="SLT"  />
                            <AppCheckbox label="Speech-Language Therapy" id_="SLT"  />
                            <AppCheckbox label="Speech-Language Therapy" id_="SLT"  />
                            <AppCheckbox label="Speech-Language Therapy" id_="SLT"  />


                        </div>
                    </div>


                    <!-- Modal footer -->
                    <div
                        class="flex items-center p-6 space-x-2 border-t justify-between border-gray-200 rounded-b dark:border-gray-600">
                        <button type="button" class="">
                            Clear all filters</button>
                        <button type="button" class="border px-4 py-2 bg-black active:bg-gray-700 text-white rounded-lg">
                            Apply filters</button>
                    </div>
                </div>
            </div>
    </div>
</div></template>