<script setup>
import { Github, Linkedin, Menu, X } from 'lucide-vue-next'
import { ref } from 'vue'
import configData from '../data/config.json'

const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}
</script>

<template>
  <nav class="fixed top-0 left-0 right-0 z-50 glass shadow-lg">
    <div class="max-w-screen-2xl mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <a href="#home" class="text-2xl font-bold text-gray-900 hover:text-button-peach-dark transition-colors duration-500">
          {{ configData.personal.name }}
        </a>

        <div class="hidden md:flex items-center space-x-8">
          <a href="#home" class="nav-link text-md font-semibold text-gray-800 hover:text-button-peach-dark transition-colors duration-500 relative group">
            <span class="text-base font-medium">Home</span>
            <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-button-peach-dark to-button-peach transition-all duration-500 group-hover:w-full"></span>
          </a>
          <a href="#about" class="nav-link text-base font-semibold text-gray-800 hover:text-button-peach-dark transition-colors duration-500 relative group">
            <span class="text-base font-medium">About</span>
            <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-button-peach-dark to-button-peach transition-all duration-500 group-hover:w-full"></span>
          </a>
          <a href="#skills" class="nav-link text-base font-semibold text-gray-800 hover:text-button-peach-dark transition-colors duration-500 relative group">
            <span class="text-base font-medium">Skills</span>
            <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-button-peach-dark to-button-peach transition-all duration-500 group-hover:w-full"></span>
          </a>
          <a href="#experience" class="nav-link text-base font-semibold text-gray-800 hover:text-button-peach-dark transition-colors duration-500 relative group">
            <span class="text-base font-medium">Experience</span>
            <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-button-peach-dark to-button-peach transition-all duration-500 group-hover:w-full"></span>
          </a>
          <a href="#projects" class="nav-link text-base font-semibold text-gray-800 hover:text-button-peach-dark transition-colors duration-500 relative group">
            <span class="text-base font-medium">Projects</span>
            <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-button-peach-dark to-button-peach transition-all duration-500 group-hover:w-full"></span>
          </a>
        </div>

        <div class="flex items-center space-x-4">
          <a 
            :href="configData.personal.github" 
            target="_blank"
            class="hidden sm:block p-2 rounded-full bg-button-peach-light/30 hover:bg-button-peach transition-all duration-500 group"
            aria-label="GitHub"
          >
            <Github :size="22" class="text-gray-800 group-hover:text-white transition-colors duration-500" />
          </a>
          <a 
            :href="configData.personal.linkedin" 
            target="_blank"
            class="hidden sm:block p-2 rounded-full bg-button-peach-light/30 hover:bg-button-peach transition-all duration-500 group"
            aria-label="LinkedIn"
          >
            <Linkedin :size="22" class="text-gray-800 group-hover:text-white transition-colors duration-500" />
          </a>

          <button 
            @click="toggleMobileMenu"
            class="md:hidden p-2 rounded-lg hover:bg-light-blue/20 transition-colors"
            aria-label="Toggle menu"
          >
            <Menu v-if="!mobileMenuOpen" :size="24" class="text-gray-800" />
            <X v-else :size="24" class="text-gray-800" />
          </button>
        </div>
      </div>

      <Transition name="slide-down">
        <div v-if="mobileMenuOpen" class="md:hidden mt-4 pt-4 border-t border-light-blue/40 space-y-3">
          <a @click="closeMobileMenu" href="#home" class="block text-center py-2 text-gray-800 hover:text-button-peach-dark font-semibold transition-colors duration-500">Home</a>
          <a @click="closeMobileMenu" href="#about" class="block text-center py-2 text-gray-800 hover:text-button-peach-dark font-semibold transition-colors duration-500">About</a>
          <a @click="closeMobileMenu" href="#skills" class="block text-center py-2 text-gray-800 hover:text-button-peach-dark font-semibold transition-colors duration-500">Skills</a>
          <a @click="closeMobileMenu" href="#experience" class="block text-center py-2 text-gray-800 hover:text-button-peach-dark font-semibold transition-colors duration-500">Experience</a>
          <a @click="closeMobileMenu" href="#projects" class="block text-center py-2 text-gray-800 hover:text-button-peach-dark font-semibold transition-colors duration-500">Projects</a>
          
          <div class="flex justify-center space-x-4 pt-4">
            <a :href="configData.personal.github" target="_blank" class="p-2 rounded-full bg-button-peach-light/30 hover:bg-button-peach transition-all duration-500 group">
              <Github :size="20" class="text-gray-800 group-hover:text-white transition-colors" />
            </a>
            <a :href="configData.personal.linkedin" target="_blank" class="p-2 rounded-full bg-button-peach-light/30 hover:bg-button-peach transition-all duration-500 group">
              <Linkedin :size="20" class="text-gray-800 group-hover:text-white transition-colors" />
            </a>
          </div>
        </div>
      </Transition>
    </div>
  </nav>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
