<script setup lang="ts">
import { ref, computed } from 'vue'
import ProjectCard from './ProjectCard.vue'
import projectsData from '../../../data/projects.json'
import { Code2 } from 'lucide-vue-next'

// Import images
import ToDoApp from '../../data/images/ToDoApp.png'
import Medspot from '../../data/images/MedspotImg.png'
import SnakeGame from '../../data/images/SnakeGame.png'
import RPS from '../../data/images/RPSGame.png'

const imageMap: { [key: string]: string } = {
  'ToDoApp.png': ToDoApp,
  'MedspotImg.png': Medspot,
  'SnakeGame.png': SnakeGame,
  'RPSGame.png': RPS
}

const projects = projectsData.projects.map(project => ({
  ...project,
  imgSrc: imageMap[project.image]
}))

const selectedFilter = ref('All')
const filters = ['All', ...Array.from(new Set(projects.map(p => p.category)))]

const filteredProjects = computed(() => {
  if (selectedFilter.value === 'All') {
    return projects
  }
  return projects.filter(project => project.category === selectedFilter.value)
})
</script>

<template>
  <section id="projects" class="relative py-12 px-6 overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-20 left-10 w-96 h-96 bg-almond-silk/20 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-20 right-10 w-80 h-80 bg-peach-fuzz/20 rounded-full blur-3xl animate-float" style="animation-delay: 2s;"></div>
    </div>

    <div class="max-w-screen-2xl mx-auto relative z-10">
      <div class="text-center mb-12 animate-fade-in-up">
        <h2 class="text-5xl md:text-6xl font-bold text-gray-900 mb-4 flex items-center justify-center">
          <Code2 :size="56" class="text-button-peach-dark mr-4" />
          <span class="bg-gradient-to-r from-button-peach-dark via-button-peach to-button-peach-dark bg-clip-text text-transparent">
            Projects
          </span>
        </h2>
        <div class="w-24 h-1.5 bg-gradient-to-r from-button-peach-dark to-button-peach mx-auto rounded-full"></div>
        <p class="text-gray-700 font-semibold mt-4 text-base">Personal projects</p>
      </div>

      <div class="flex flex-wrap justify-center gap-3 mb-12 animate-fade-in" style="animation-delay: 0.2s;">
        <button
          v-for="filter in filters"
          :key="filter"
          @click="selectedFilter = filter"
          :class="[
            'px-6 py-3 rounded-full font-bold text-sm transition-all duration-500 transform hover:-translate-y-1',
            selectedFilter === filter
              ? 'bg-button-peach-dark text-white shadow-lg scale-105'
              : 'bg-white text-gray-800 hover:bg-button-peach-light/50 shadow-md hover:shadow-lg border-2 border-gray-300'
          ]"
        >
          {{ filter }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="(project, index) in filteredProjects" 
          :key="project.title"
        >
          <ProjectCard
            :img="project.imgSrc"
            :project-name="project.title"
            :description="project.description"
            :github-link="project.githubLink"
            :tech-used="project.technologies"
            :featured="project.featured"
          />
        </div>
      </div>

      <div v-if="filteredProjects.length === 0" class="text-center py-20">
        <p class="text-gray-700 font-semibold text-lg">No projects found in this category yet</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
</style>

