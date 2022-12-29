/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./flaskr/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
