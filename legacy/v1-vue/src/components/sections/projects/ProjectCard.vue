<script setup lang="ts">
import { Github, ExternalLink, Star } from 'lucide-vue-next'

const props = defineProps<{
  projectName: string
  img: string
  githubLink: string
  description: string
  techUsed: string[]
  featured?: boolean
}>()
</script>

<template>
  <article class="group relative h-full flex flex-col glass rounded-3xl overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 border border-light-blue/30">
    <div class="relative overflow-hidden h-64">
      <img 
        :src="props.img" 
        :alt="props.projectName"
        class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
      />
      
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-60 group-hover:opacity-80 transition-opacity duration-500"></div>
      
      <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        <a 
          :href="props.githubLink" 
          target="_blank"
          class="px-6 py-3 bg-button-peach-dark text-white rounded-full font-bold text-sm flex items-center space-x-2 hover:bg-button-peach transition-all duration-500 shadow-xl transform scale-90 group-hover:scale-100 mx-2"
        >
          <Github :size="20" />
          <span>View Code</span>
        </a>
      </div>

    </div>

    <div class="flex-1 flex flex-col p-6">
      <h3 class="text-2xl font-bold text-gray-900 mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-button-peach-dark group-hover:to-button-peach group-hover:bg-clip-text transition-all duration-500">
        {{ props.projectName }}
      </h3>

      <p class="text-gray-700 font-semibold text-md leading-relaxed mb-4 flex-1">
        {{ props.description }}
      </p>

      <div class="flex flex-wrap gap-2 pt-4 border-t border-gray-300">
        <span 
          v-for="(tech, index) in props.techUsed" 
          :key="index"
          class="px-3 py-1.5 bg-gray-100 text-gray-800 text-xs rounded-full font-bold hover:bg-button-peach hover:text-white transition-all duration-500 transform hover:scale-105 cursor-default border border-gray-300"
        >
          {{ tech }}
        </span>
      </div>

      <a 
        :href="props.githubLink" 
        target="_blank"
        class="mt-4 flex items-center space-x-2 text-button-peach-dark hover:text-button-peach transition-colors duration-500 group/link font-bold text-sm"
      >
        <Github :size="18" />
        <span>View on GitHub</span>
        <ExternalLink :size="14" class="group-hover/link:translate-x-1 transition-transform" />
      </a>
    </div>

    <div class="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" 
         style="background: linear-gradient(135deg, #bee1e6, #cddafd); padding: 2px;">
      <div class="w-full h-full bg-transparent rounded-3xl"></div>
    </div>
  </article>
</template>

<style scoped>
</style>

