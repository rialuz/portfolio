<script setup lang="ts">
import { ref } from 'vue'
import { Code2, Database, Wrench, TestTube } from 'lucide-vue-next'
import configData from '../../data/config.json'

const iconMap: { [key: string]: any } = {
  Code2,
  Database,
  TestTube,
  Wrench
}

const skillCategories = ref(configData.skills.map(category => ({
  ...category,
  icon: iconMap[category.icon]
})))

const selectedCategory = ref(0)
</script>

<template>
  <section id="skills" class="py-12 px-6">
    <div class="max-w-screen-2xl mx-auto">
      <div class="text-center mb-16 animate-fade-in-up">
        <h2 class="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
          My <span class="bg-gradient-to-r from-button-peach-dark via-button-peach to-button-peach-dark bg-clip-text text-transparent">Skills</span>
        </h2>
        <div class="w-24 h-1.5 bg-gradient-to-r from-button-peach-dark to-button-peach mx-auto rounded-full"></div>
        <p class="text-gray-700 font-semibold mt-4 text-base">Technologies & tools I work with / have worked with</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div 
          v-for="(category, index) in skillCategories" 
          :key="index"
          class="group glass rounded-3xl p-8 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 animate-fade-in-up border border-light-blue/30"
          :style="{ animationDelay: `${index * 0.15}s` }"
        >
          <div class="flex items-center space-x-4 mb-6">
            <div :class="[
              'w-16 h-16 rounded-2xl flex items-center justify-center bg-gradient-to-br shadow-lg group-hover:scale-110 transition-transform duration-300',
              category.color
            ]">
              <component :is="category.icon" :size="32" class="text-white" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900">{{ category.category }}</h3>
          </div>

          <div class="flex flex-wrap gap-3">
            <span 
              v-for="(skill, skillIndex) in category.skills" 
              :key="skillIndex"
              :class="['px-4 py-2 rounded-full font-semibold text-sm text-gray-800 bg-gradient-to-r shadow-md hover:shadow-lg hover:scale-105 transition-all duration-500 cursor-default border border-gray-300', category.color]"
            >
              {{ skill }}
            </span>
          </div>
        </div>
      </div>

      <div v-if="configData.worksInProgress.length > 0" class="mt-16 text-center animate-fade-in" style="animation-delay: 0.8s;">
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Actively Upskilling In</h3>
        <div class="flex flex-wrap justify-center gap-3">
          <span 
            v-for="skill in configData.worksInProgress" 
            :key="skill"
            class="px-5 py-2 bg-white/90 backdrop-blur-sm rounded-full text-gray-800 font-semibold text-sm shadow-md hover:shadow-lg hover:bg-gradient-to-r hover:from-button-peach-dark hover:to-button-peach hover:text-white transition-all duration-500 transform hover:-translate-y-1 cursor-default border border-light-blue/30"
          >
            {{ skill }}
          </span>
        </div>
      </div>

      <div v-if="configData.additionalSkills.length > 0" class="mt-16 text-center animate-fade-in" style="animation-delay: 0.8s;">
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Also Familiar With</h3>
        <div class="flex flex-wrap justify-center gap-3">
          <span 
            v-for="skill in configData.additionalSkills" 
            :key="skill"
            class="px-5 py-2 bg-white/90 backdrop-blur-sm rounded-full text-gray-800 font-semibold text-sm shadow-md hover:shadow-lg hover:bg-gradient-to-r hover:from-button-peach-dark hover:to-button-peach hover:text-white transition-all duration-500 transform hover:-translate-y-1 cursor-default border border-light-blue/30"
          >
            {{ skill }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
</style>

