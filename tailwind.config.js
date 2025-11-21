/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './my_website/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          base: '#0f0f12',
          baseAlt: '#1a1a1f',
          baseMuted: '#2a2a33',
          text: '#f1f1f2',
          textMuted: '#c1c1c7',
          accentSky: '#7dd3fc',
          accentLavender: '#c4b5fd',
          accentMint: '#99f6e4',
        },
      },
    },
  },
  plugins: [],
};
