module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      // make custom spacing
      spacing: {
        '8xl': '96rem',
      },

    }
  },
  plugins: [
    require('flowbite')
  ],
}
