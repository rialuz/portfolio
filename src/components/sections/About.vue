<script setup lang="ts">
import { Sparkles, Heart, ArrowRight, ComputerIcon } from 'lucide-vue-next'
import configData from '../../data/config.json'
</script>

<template>
  <section id="about" class="relative flex items-center justify-center  overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-powder-blush/20 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-peach-fuzz/30 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
    </div>

    <div class="max-w-screen-2xl w-full relative z-10">
      <div class="text-center mb-16 animate-fade-in-up">
        <h2 class="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
          About <span class="bg-gradient-to-r from-button-peach-dark via-button-peach to-button-peach-dark bg-clip-text text-transparent">Me</span>
        </h2>
        <div class="w-24 h-1.5 bg-gradient-to-r from-button-peach-dark to-button-peach mx-auto rounded-full"></div>
      </div>

      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <div class="flex justify-center lg:justify-end order-1 animate-slide-in-left">
          <div class="relative group">
            <div class="relative">
              <div class="absolute -inset-4 bg-gradient-to-r from-powder-blush via-peach-glow to-peach-fuzz rounded-3xl blur-2xl opacity-50 group-hover:opacity-75 transition-opacity duration-500"></div>
              
              <div class="relative w-80 h-80 rounded-3xl overflow-hidden shadow-2xl transform group-hover:scale-105 transition-all duration-500 border-4 border-white">
                <img 
                  src="../data/images/img.jpg" 
                  alt="Luz Lopez Marcano" 
                  class="w-full h-full object-cover"
                />
                <div class="absolute inset-0 bg-gradient-to-t from-powder-blush/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              </div>
            </div>

            <div class="absolute -bottom-4 -left-4 w-14 h-14 bg-white rounded-full flex items-center justify-center shadow-xl animate-bounce-slow border-2 border-periwinkle" style="animation-delay: 0.5s;">
              <Heart :size="24" class="text-button-peach fill-current" />
            </div>
          </div>
        </div>

        <div class="space-y-6 order-2 animate-slide-in-right">
          <div class="space-y-4">
            <p class="text-lg md:text-xl text-gray-800 font-semibold leading-relaxed">
              <span class="text-3xl font-bold text-button-peach-dark">{{ configData.personal.hero.greeting }}</span>
            </p>
            <p class="text-base md:text-lg text-gray-700 font-semibold leading-relaxed">
              {{ configData.personal.about.introduction }}
            </p>
            <p class="text-base md:text-lg text-gray-700 font-semibold leading-relaxed">
              {{ configData.personal.about.passion }}
            </p>
          </div>

          <div class="glass rounded-2xl p-6 space-y-4 border border-light-blue/30">
            <h3 class="text-xl font-bold text-gray-900 flex items-center">
              <ComputerIcon :size="24" class="text-button-peach-dark mr-2" />
              Tech Stack
            </h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div v-for="tech in configData.techStack" :key="tech" class="skill-badge">
                {{ tech }}
              </div>
            </div>
          </div>

          <div class="glass rounded-2xl p-6 space-y-3 border border-periwinkle/30">
            <h3 class="text-lg font-bold text-gray-900">Key Strengths</h3>
            <ul class="space-y-2">
              <li v-for="strength in configData.personal.about.keyStrengths" :key="strength" class="flex items-start text-gray-700 text-sm font-medium">
                <span class="text-button-peach-dark mr-2 flex-shrink-0">▹</span>
                <span class="text-sm font-semibold">{{ strength }}</span>
              </li>
            </ul>
          </div>

          <div class="glass rounded-2xl p-6 space-y-3 border border-light-blue/30">
            <h3 class="text-lg font-bold text-gray-900">When I am not coding,</h3>
            <ul class="space-y-2">
              <li v-for="fact in configData.personal.about.funFacts" :key="fact" class="flex items-start text-gray-700 text-sm font-semibold">
                <span class="text-button-peach mr-2 flex-shrink-0">▸</span>
                <span class="text-sm font-semibold">{{ fact }}</span>
              </li>
            </ul>
          </div>

          <div class="flex flex-wrap gap-4 pt-4">
            <a 
              href="#projects" 
              class="group px-6 py-3 bg-button-peach-dark text-white rounded-full font-semibold text-base hover:bg-button-peach hover:shadow-xl transition-all duration-500 transform hover:-translate-y-1 flex items-center space-x-2"
            >
              <span>View My Work</span>
              <span class="group-hover:translate-x-1 transition-transform"><ArrowRight :size="16" class="text-white" /></span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.skill-badge {
  background-color: rgba(255, 255, 255, 0.9);
  color: rgb(31, 41, 55);
  padding: 0.625rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.813rem;
  font-weight: 600;
  transition: all 0.3s;
  cursor: default;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  border: 1px solid rgba(190, 225, 230, 0.3);
}

.skill-badge:hover {
  background: #ffb5a7;
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transform: translateY(-0.25rem);
  border-color: transparent;
}
</style>

