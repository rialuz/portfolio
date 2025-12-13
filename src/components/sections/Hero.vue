<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Sparkles, ArrowDown, Code2, Palette, Zap } from 'lucide-vue-next'
import configData from '../../data/config.json'

const typedText = ref('')
const fullText = `I'm ${configData.personal.name}`
const typingSpeed = 100

onMounted(() => {
  let i = 0
  const typeWriter = () => {
    if (i < fullText.length) {
      typedText.value += fullText.charAt(i)
      i++
      setTimeout(typeWriter, typingSpeed)
    }
  }
  setTimeout(typeWriter, 500)
})
</script>

<template>
  <section id="home" class="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute top-20 left-10 w-96 h-96 bg-powder-blush/30 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-20 right-10 w-[500px] h-[500px] bg-peach-fuzz/40 rounded-full blur-3xl animate-float" style="animation-delay: 1.5s;"></div>
      <div class="absolute top-1/2 left-1/3 w-72 h-72 bg-almond-silk/30 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 3s;"></div>
      
      <div class="absolute top-1/4 right-1/4 animate-bounce-slow opacity-20">
        <Code2 :size="64" class="text-powder-blush" />
      </div>
      <div class="absolute bottom-1/4 left-1/4 animate-bounce-slow opacity-20" style="animation-delay: 1s;">
        <Palette :size="56" class="text-peach-glow" />
      </div>
      <div class="absolute top-1/3 left-1/5 animate-bounce-slow opacity-20" style="animation-delay: 2s;">
        <Zap :size="48" class="text-almond-silk" />
      </div>
    </div>

    <div class="relative z-10 max-w-screen-2xl w-full">
      <div class="text-center space-y-8 animate-fade-in-up">

        <div class="space-y-4">
          <h2 class="text-2xl md:text-3xl text-gray-700 font-semibold">
            {{ configData.personal.hero.greeting }}
          </h2>
          <h1 class="text-5xl md:text-7xl lg:text-8xl font-bold text-gray-900 min-h-[100px] md:min-h-[120px]">
            <span class="inline-block name-text">
              {{ typedText }}
              <span class="inline-block w-1 h-12 md:h-16 lg:h-20 bg-button-peach-dark animate-blink ml-1 align-middle"></span>
            </span>
          </h1>
          <h3 class="text-3xl md:text-4xl lg:text-5xl font-bold text-button-peach-dark">
            {{ configData.personal.title }}
          </h3>
        </div>

        <p class="text-lg md:text-xl text-gray-700 font-medium max-w-3xl mx-auto leading-relaxed animate-fade-in" style="animation-delay: 0.5s;">
          {{ configData.personal.hero.tagline }}
        </p>

        <div class="flex flex-wrap items-center justify-center gap-6 pt-8 animate-fade-in" style="animation-delay: 0.7s;">
          <a 
            href="#projects" 
            class="group px-8 py-4 bg-button-peach-dark text-white rounded-full font-semibold text-lg shadow-xl hover:bg-button-peach hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-1 hover:scale-105 flex items-center space-x-2"
          >
            <span>View My Work</span>
            <ArrowDown :size="20" class="group-hover:translate-y-1 transition-transform" />
          </a>
          <a 
            :href="configData.personal.linkedin" 
            target="_blank"
            class="px-8 py-4 bg-white text-gray-900 border-2 border-button-peach-dark rounded-full font-semibold text-lg hover:bg-button-peach-dark hover:text-white hover:border-button-peach-dark transition-all duration-500 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
          >
            Connect on LinkedIn
          </a>
        </div>

      </div>
    </div>

    <a 
      href="#stats-section" 
      class="hidden md:flex absolute bottom-8 right-8 items-center space-y-2 animate-bounce-slow group cursor-pointer z-50 bg-white/90 backdrop-blur-sm rounded-full p-4 shadow-lg hover:shadow-xl transition-all duration-500 flex-col"
    >
      <span class="text-gray-900 font-bold text-xs uppercase tracking-wide group-hover:text-button-peach-dark transition-colors duration-500">Scroll</span>
      <div class="flex flex-col items-center">
        <ArrowDown :size="28" class="text-button-peach-dark group-hover:text-button-peach transition-colors duration-500" strokeWidth="3" />
      </div>
    </a>
  </section>
</template>

<style scoped>
.name-text:hover {
  background: linear-gradient(90deg, #fec5bb, #ffb5a7, #e8a598, #d89b8d, #e8a598, #ffb5a7, #fec5bb);
  background-size: 400% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: smoothPeachFlow 8s ease-in-out infinite;
}

@keyframes smoothPeachFlow {
  0% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
  100% {
    background-position: 0% center;
  }
}
</style>

