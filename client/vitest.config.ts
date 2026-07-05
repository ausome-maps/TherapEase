import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '~': path.resolve(__dirname),
      'assets': path.resolve(__dirname, 'assets'),
      '@': path.resolve(__dirname),
    },
  },
  test: {
    environment: 'happy-dom',
    globals: true,
    include: ['**/*.{test,spec}.{ts,js}'],
    setupFiles: [],
  },
})
