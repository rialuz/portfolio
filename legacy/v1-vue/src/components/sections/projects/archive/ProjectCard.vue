<script setup lang="ts">
import { Github, ExternalLink } from 'lucide-vue-next'

const props = defineProps(['projectName', 'img', 'githubLink', 'description', 'techUsed'])
</script>

<template>
  <div class="group relative bg-beige/50 rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 border border-dry-sage/20 h-full flex flex-col">
    <!-- Image Container -->
    <div class="relative overflow-hidden h-56">
      <img 
        :src="props.img" 
        :alt="props.projectName"
        class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-light-bronze/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-6">
        <a 
          :href="props.githubLink" 
          target="_blank"
          class="bg-white text-light-bronze px-6 py-3 rounded-full font-semibold flex items-center space-x-2 hover:bg-papaya-whip transition-all duration-300 shadow-lg transform translate-y-4 group-hover:translate-y-0"
        >
          <Github :size="20" />
          <span>View Code</span>
          <ExternalLink :size="16" />
        </a>
      </div>
    </div>

    <!-- Content -->
    <div class="p-6 flex-1 flex flex-col">
      <div class="flex items-start justify-between mb-3">
        <h3 class="text-2xl font-bold text-gray-800 group-hover:text-light-bronze transition-colors duration-300">
          {{ props.projectName }}
        </h3>
      </div>

      <p class="text-gray-700 leading-relaxed mb-4 flex-1">
        {{ props.description }}
      </p>

      <!-- Tech Stack Tags -->
      <div class="flex flex-wrap gap-2 mt-auto">
        <span 
          v-for="tech in props.techUsed.split(',')" 
          :key="tech"
          class="px-3 py-1 bg-papaya-whip text-gray-700 text-sm rounded-full font-medium hover:bg-light-bronze hover:text-white transition-colors duration-300"
        >
          {{ tech.trim() }}
        </span>
      </div>
    </div>
  </div>
</template>