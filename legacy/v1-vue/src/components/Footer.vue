<script setup lang="ts">
import { Github, Linkedin, Code } from 'lucide-vue-next'
import configData from '../data/config.json'
</script>

<template>
  <footer class="relative glass border-t border-light-blue/40 py-12 mt-20 overflow-hidden">
    <div class="absolute inset-0 pointer-events-none opacity-20">
      <div class="absolute bottom-0 left-10 w-64 h-64 bg-light-blue/40 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-10 w-64 h-64 bg-periwinkle/40 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-screen-2xl mx-auto px-6 relative z-10">
      <div class="flex flex-col items-center space-y-8">
        <div class="flex items-center space-x-2">
          <Code :size="20" class="text-button-peach-dark" />
          <div class="w-16 h-1 bg-gradient-to-r from-button-peach-dark to-button-peach rounded-full"></div>
          <Code :size="20" class="text-button-peach" />
        </div>

        <div class="flex items-center space-x-6">
          <a 
            :href="configData.personal.github" 
            target="_blank"
            class="p-4 rounded-full bg-button-peach-light/40 hover:bg-button-peach hover:text-white transition-all duration-500 shadow-lg hover:shadow-xl transform hover:-translate-y-2 group border border-button-peach/30"
            aria-label="GitHub"
          >
            <Github :size="24" class="text-gray-800 group-hover:text-white transition-colors" />
          </a>
          <a 
            :href="configData.personal.linkedin" 
            target="_blank"
            class="p-4 rounded-full bg-button-peach-light/40 hover:bg-button-peach hover:text-white transition-all duration-500 shadow-lg hover:shadow-xl transform hover:-translate-y-2 group border border-button-peach/30"
            aria-label="LinkedIn"
          >
            <Linkedin :size="24" class="text-gray-800 group-hover:text-white transition-colors" />
          </a>
        </div>

        <div class="text-center space-y-3">
          <p class="text-gray-800 font-bold text-base">
            <span class="bg-gradient-to-r from-button-peach-dark to-button-peach bg-clip-text text-transparent">
              {{ configData.personal.name }}
            </span>
          </p>
          <p class="text-gray-700 font-semibold text-sm">
            &copy; {{ new Date().getFullYear() }} All Rights Reserved
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
</style>