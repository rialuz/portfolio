<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Trophy, Code, Briefcase, Lightbulb } from 'lucide-vue-next'
import configData from '../../data/config.json'

const iconMap: { [key: string]: any } = {
  Briefcase,
  Code,
  Trophy,
  Lightbulb
}

const stats = ref(configData.stats.map(stat => ({
  ...stat,
  icon: iconMap[stat.icon],
  value: 0,
  target: stat.value,
  color: 'text-button-peach-dark'
})))

const startCounting = () => {
  stats.value.forEach((stat, index) => {
    const increment = stat.target / 50
    const timer = setInterval(() => {
      if (stat.value < stat.target) {
        stat.value += increment
        if (stat.value >= stat.target) {
          stat.value = stat.target
          clearInterval(timer)
        }
      }
    }, 30)
  })
}

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          startCounting()
          observer.disconnect()
        }
      })
    },
    { threshold: 0.5 }
  )

  const element = document.querySelector('#stats-section')
  if (element) observer.observe(element)
})
</script>

<template>
  <section id="stats-section" class="py-8 px-6">
    <div class="max-w-screen-xl mx-auto">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div 
          v-for="(stat, index) in stats" 
          :key="index"
          class="group relative bg-white/80 backdrop-blur-sm rounded-2xl p-4 shadow-md hover:shadow-xl transition-all duration-500 border border-button-peach/30 hover:border-button-peach-dark/50 transform hover:-translate-y-1"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-light-blue/10 to-periwinkle/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <div class="relative z-10 text-center space-y-2">
            <div class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-light-blue/30 to-periwinkle/30 group-hover:scale-110 transition-transform duration-300">
              <component :is="stat.icon" :size="20" :class="stat.color" />
            </div>
            
            <div class="space-y-1">
              <h3 class="text-3xl font-bold text-gray-900">
                {{ stat.value.toFixed(stat.target < 10 ? 1 : 0) }}{{ stat.suffix }}
              </h3>
              <p class="text-gray-700 font-semibold text-xs">{{ stat.label }}</p>
            </div>
          </div>

          <div class="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" 
               style="background: linear-gradient(135deg, #bee1e6, #cddafd); padding: 2px;">
            <div class="w-full h-full bg-white rounded-3xl"></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
</style>

