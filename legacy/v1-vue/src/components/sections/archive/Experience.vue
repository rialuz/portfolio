<script setup lang="ts">
import { ref } from 'vue'
import experienceData from '../data/workexperience.json'
import { Briefcase, Calendar, ExternalLink } from 'lucide-vue-next'

const data = ref(experienceData.experience);
const selectedCompany = ref(data.value[0]?.company || '');

const regex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;

for (const experience of data.value) {
  let summary = experience.description;
  const arr = summary.split(". ");
  experience.summary = arr;
  
  const url = experience.description.match(regex);
  console.log(url);
}

const selectCompany = (company: string) => {
  selectedCompany.value = company;
}

const getSelectedExperience = () => {
  return data.value.find(exp => exp.company === selectedCompany.value) || data.value[0];
}
</script>

<template>
  <section id="experience" class="min-h-screen px-6 py-20">
    <div class="max-w-6xl mx-auto">
      <!-- Section Title -->
      <div class="text-center mb-16 animate-slide-up">
        <h2 class="text-5xl font-bold text-gray-800 mb-4">
          <span class="bg-gradient-to-r from-light-bronze to-dry-sage bg-clip-text text-transparent">
            Experience
          </span>
        </h2>
        <div class="w-24 h-1 bg-light-bronze mx-auto rounded-full"></div>
      </div>

      <!-- Experience Container -->
      <div class="bg-beige/50 rounded-3xl shadow-2xl overflow-hidden border border-dry-sage/20">
        <div class="grid md:grid-cols-4 gap-0">
          <!-- Company Tabs -->
          <div class="md:col-span-1 bg-papaya-whip/50 border-r border-dry-sage/20">
            <div class="p-4 space-y-2">
              <div
                v-for="exp in data"
                :key="exp.id"
                @click="selectCompany(exp.company)"
                :class="[
                  'p-4 rounded-xl cursor-pointer transition-all duration-300 text-center md:text-left',
                  selectedCompany === exp.company 
                    ? 'bg-light-bronze text-white shadow-lg transform scale-105' 
                    : 'hover:bg-dry-sage/30 text-gray-700'
                ]"
              >
                <p class="font-semibold">{{ exp.company }}</p>
              </div>
            </div>
          </div>

          <!-- Experience Details -->
          <div class="md:col-span-3 p-8">
            <div class="animate-fade-in">
              <div class="mb-6">
                <h3 class="text-3xl font-bold text-gray-800 mb-3 flex items-center flex-wrap">
                  <Briefcase :size="28" class="text-light-bronze mr-3" />
                  {{ getSelectedExperience().title }} 
                  <span class="text-light-bronze mx-2">@</span> 
                  {{ getSelectedExperience().company }}
                </h3>
                <p class="text-gray-600 flex items-center text-lg">
                  <Calendar :size="20" class="mr-2 text-dry-sage" />
                  {{ getSelectedExperience().startDate }} - {{ getSelectedExperience().endDate }}
                </p>
              </div>

              <div class="space-y-4">
                <ul class="space-y-3">
                  <li 
                    v-for="(text, index) in getSelectedExperience().summary" 
                    :key="index"
                    class="flex items-start text-gray-700 text-lg leading-relaxed"
                  >
                    <span class="text-light-bronze mr-3 mt-1 flex-shrink-0">▹</span>
                    <span>
                      {{ text }}
                      <a 
                        v-if="text.includes('Selected')" 
                        href="https://www.catalyte.io/alumni-stories/luz/"
                        target="_blank"
                        class="inline-flex items-center ml-2 text-light-bronze hover:text-dry-sage transition-colors font-semibold"
                      >
                        Read Story
                        <ExternalLink :size="16" class="ml-1" />
                      </a>
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-in-out;
}
</style>