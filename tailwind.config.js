/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Soft Peachy Delight - Primary Palette
        'powder-blush': '#fec5bb',
        'almond-silk': '#fcd5ce',
        'soft-blush': '#fae1dd',
        'seashell': '#f8edeb',
        'alabaster-grey': '#e8e8e4',
        'alabaster-grey-2': '#d8e2dc',
        'soft-linen': '#ece4db',
        'powder-petal': '#ffe5d9',
        'peach-fuzz': '#ffd7ba',
        'peach-glow': '#fec89a',
        // Subtle Pastel Hues - Blues for accents
        'light-blue': '#bee1e6',
        'azure-mist': '#e2ece9',
        'lavender': '#dfe7fd',
        'periwinkle': '#cddafd',
        // Darker shades for better contrast
        'blue-dark': '#2c5282',
        'teal-dark': '#2c7a7b',
        // Purple theme for name hover
        'purple-light': '#c084fc',
        'purple-medium': '#9333ea',
        'purple-dark': '#6b21a8',
        'purple-darker': '#4c1d95',
        // Custom peachy button colors
        'button-peach-dark': '#d87968',   // Darker peachy pink for better visibility
        'button-peach': '#e8a598',        // Medium peachy pink  
        'button-peach-light': '#ffb5a7',  // Lighter peachy pink
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.8s ease-in-out',
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-in-left': 'slideInLeft 0.6s ease-out',
        'slide-in-right': 'slideInRight 0.6s ease-out',
        'float': 'float 3s ease-in-out infinite',
        'bounce-slow': 'bounceSlow 2s infinite',
        'pulse-slow': 'pulseSlow 3s ease-in-out infinite',
        'typing': 'typing 3.5s steps(40, end)',
        'blink': 'blink 0.75s step-end infinite',
        'scale-in': 'scaleIn 0.5s ease-out',
        'gradient': 'gradient 8s linear infinite',
        'purple-wave': 'purpleWave 3s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-50px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(50px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        bounceSlow: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pulseSlow: {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.05)' },
        },
        typing: {
          'from': { width: '0' },
          'to': { width: '100%' },
        },
        blink: {
          'from, to': { borderColor: 'transparent' },
          '50%': { borderColor: '#fec89a' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        purpleWave: {
          '0%, 100%': { 
            backgroundImage: 'linear-gradient(to right, #c084fc, #9333ea)',
          },
          '50%': { 
            backgroundImage: 'linear-gradient(to right, #6b21a8, #4c1d95)',
          },
        },
      },
      backgroundSize: {
        '300%': '300%',
      },
    },
  },
  plugins: [],
}

