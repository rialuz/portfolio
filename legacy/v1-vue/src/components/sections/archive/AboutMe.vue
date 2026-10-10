<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
</script>

<template>
  <section id="about" class="relative min-h-screen flex items-center justify-center px-6 py-20 animate-fade-in overflow-hidden">
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-dry-sage/20 rounded-full blur-3xl animate-float"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-papaya-whip/30 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-light-bronze/10 rounded-full blur-3xl animate-float" style="animation-delay: 2s;"></div>
    </div>

    <div class="max-w-6xl w-full relative z-10">
      <div class="grid md:grid-cols-2 gap-12 items-center">
        <div class="flex justify-center md:justify-end order-1 md:order-1">
          <div class="relative group">
            <div class="absolute -top-4 -left-4 w-full h-full bg-dry-sage/30 rounded-full blur-xl group-hover:bg-light-bronze/40 transition-all duration-500"></div>
            <div class="relative w-72 h-72 rounded-full overflow-hidden border-4 border-light-bronze shadow-2xl transform group-hover:scale-105 transition-all duration-500">
              <img 
                src="../data/images/img.jpg" 
                alt="Luz Lopez Marcano" 
                class="w-full h-full object-cover"
              />
            </div>
       
            <div class="absolute -bottom-2 -right-2 w-20 h-20 bg-papaya-whip rounded-full flex items-center justify-center shadow-lg animate-float">
              <Sparkles :size="32" class="text-light-bronze" />
            </div>
          </div>
        </div>

 
        <div class="space-y-6 order-2 md:order-2">
          <div>
            <p class="text-light-bronze font-semibold text-lg mb-2">👋 Hey there! I'm</p>
            <h1 class="text-5xl md:text-6xl font-bold text-gray-800 mb-4">
              <span class="bg-gradient-to-r from-light-bronze to-dry-sage bg-clip-text text-transparent hover:from-dry-sage hover:to-light-bronze transition-all duration-500">
                Luz Lopez Marcano
              </span>
            </h1>
            <p class="text-xl text-gray-600 font-medium">Software Engineer</p>
          </div>

          <p class="text-lg text-gray-700 leading-relaxed">
            I am a passionate software engineer based in <span class="font-semibold text-light-bronze">Maryland</span> with 1.5 years of hands-on work
            experience developing new features as well as improving on existing features. I enjoy the
            challenge of finding effective solutions to problems I face. I've learned a lot in my past
            experiences and am confident in my ability to be a reliable asset to any team I am in.
          </p>


          <div class="flex flex-wrap gap-4 mt-6">
            <a 
              href="#projects" 
              class="px-6 py-3 bg-light-bronze text-white rounded-full font-semibold hover:bg-dry-sage transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center space-x-2"
            >
              <span>View My Work</span>
              <span>→</span>
            </a>

          </div>

          <div class="bg-beige/50 p-6 rounded-2xl shadow-lg border border-dry-sage/20">
            <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <span class="mr-2"></span> Tech Stack
            </h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
              <div class="tech-badge">HTML, CSS, JS</div>
              <div class="tech-badge">TypeScript</div>
              <div class="tech-badge">Vue.js</div>
              <div class="tech-badge">React.js</div>
              <div class="tech-badge">Playwright</div>
              <div class="tech-badge">Jest</div>
              <div class="tech-badge">Java</div>
              <div class="tech-badge">Git/GitLab</div>
              <div class="tech-badge">CI/CD</div>
              <div class="tech-badge">New Relic</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
</style>
