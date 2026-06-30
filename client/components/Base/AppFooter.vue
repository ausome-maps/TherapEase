<template>
    <footer
        class="fixed bottom-0 left-0 z-20 w-full px-3 py-3 sm:px-4 sm:py-3 bg-white border-t border-gray-200 shadow dark:bg-gray-800 dark:border-gray-600 flex flex-col sm:flex-row items-center justify-between gap-1">
        <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">&copy; {{ copyrightYear }} <a href="https://ausomemaps.org/"
                class="hover:underline">Ausome Maps</a>
        </span>
        <ul class="flex flex-wrap items-center text-xs sm:text-sm font-medium text-gray-500 dark:text-gray-400">
            <li>
                <a href="https://ausomemaps.org/#page-0" class="hover:underline">About</a>
            </li>
        </ul>
    </footer>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const copyrightYear = config.public.copyrightYear
</script>
