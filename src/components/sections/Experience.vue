<script setup lang="ts">
import { ref } from 'vue'
import experienceData from '../../data/workexperience.json'
import { Briefcase, Calendar, ExternalLink, Award } from 'lucide-vue-next'

interface Experience {
  id: string
  title: string
  company: string
  startDate: string
  endDate: string
  description: string[]
  techStack: string[]
}

const data = ref<Experience[]>(experienceData.experience);
</script>

<template>
  <section id="experience" class="relative py-12 px-6 overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-40 right-20 w-96 h-96 bg-powder-blush/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-20 left-20 w-80 h-80 bg-peach-fuzz/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 1.5s;"></div>
    </div>

    <div class="max-w-screen-xl mx-auto relative z-10">
      <div class="text-center mb-20 animate-fade-in-up">
        <h2 class="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
          My <span class="bg-gradient-to-r from-button-peach-dark via-button-peach to-button-peach-dark bg-clip-text text-transparent">Journey</span>
        </h2>
        <div class="w-24 h-1.5 bg-gradient-to-r from-button-peach-dark to-button-peach mx-auto rounded-full"></div>
        <p class="text-gray-700 font-semibold mt-4 text-base">Professional experience and milestones</p>
      </div>

      <div class="relative">
        <div class="hidden md:block absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-button-peach-dark via-button-peach to-button-peach-dark rounded-full"></div>

        <div class="space-y-12">
          <div 
            v-for="(exp, index) in data" 
            :key="exp.id"
            :class="[
              'relative grid md:grid-cols-2 gap-8 md:gap-16 items-center animate-fade-in-up',
              index % 2 === 0 ? 'md:text-right' : 'md:flex-row-reverse'
            ]"
            :style="{ animationDelay: `${index * 0.2}s` }"
          >
            <div :class="['relative', index % 2 === 0 ? 'md:col-start-1' : 'md:col-start-2']">
              <div class="group glass rounded-3xl p-8 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-light-blue/30">
                <div :class="[
                  'inline-flex items-center space-x-2 px-4 py-2 rounded-full mb-4 bg-gradient-to-r shadow-md',
                  index % 2 === 0 ? 'from-button-peach-dark to-button-peach' : 'from-button-peach to-button-peach-light'
                ]">
                  <Briefcase :size="18" class="text-white" />
                  <span class="text-white font-bold text-sm">{{ exp.company }}</span>
                </div>

                <h3 class="text-2xl font-extrabold text-gray-900 mb-3">
                  {{ exp.title }}
                </h3>

                <div class="flex flex-wrap gap-4 mb-4 text-gray-700">
                  <span class="flex items-center space-x-2 font-semibold text-sm">
                    <Calendar :size="16" />
                    <span class="font-semibold text-sm">{{ exp.startDate }} - {{ exp.endDate }}</span>
                  </span>
                </div>

                <ul class="space-y-3 text-gray-800">
                  <li 
                    v-for="(text, textIndex) in exp.description" 
                    :key="textIndex"
                    class="flex items-start gap-3"
                  >
                    <span class="flex-shrink-0 w-2 h-2 rounded-full bg-button-peach-dark mt-2"></span>
                    <span class="text-left font-semibold text-sm">
                      {{ text }}
                      <a 
                        v-if="text.includes('Selected')" 
                        href="https://www.catalyte.io/alumni-stories/luz/"
                        target="_blank"
                        class="inline-flex items-center ml-2 text-button-peach-dark hover:text-button-peach transition-colors duration-500 font-bold group"
                      >
                        <span class="underline">Read My Story</span>
                        <ExternalLink :size="14" class="ml-1 group-hover:translate-x-1 transition-transform" />
                      </a>
                    </span>
                  </li>
                </ul>

              </div>
            </div>

            <div class="hidden md:block absolute left-1/2 transform -translate-x-1/2 z-20">
              <div class="relative">
                <div :class="[
                  'w-6 h-6 rounded-full border-4 border-white shadow-lg bg-gradient-to-r',
                  index % 2 === 0 ? 'from-button-peach-dark to-button-peach' : 'from-button-peach to-button-peach-light'
                ]"></div>
                <div :class="[
                  'absolute inset-0 w-6 h-6 rounded-full animate-ping opacity-75',
                  index % 2 === 0 ? 'bg-button-peach-dark' : 'bg-button-peach'
                ]" style="animation-duration: 2s;"></div>
              </div>
            </div>

            <div :class="['hidden md:block', index % 2 === 0 ? 'md:col-start-2' : 'md:col-start-1']"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@media (max-width: 768px) {
  .relative.grid {
    grid-template-columns: 1fr;
  }
}
</style>

