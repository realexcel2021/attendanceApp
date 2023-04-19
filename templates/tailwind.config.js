/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.{html,js}"],
  theme: {
    extend: {
      colors : {
        'green-color' : '#044801'
      },
      screens : {
        'sm': {'max': '639px'}
      }
    },
    
  },
  plugins: [],
}

