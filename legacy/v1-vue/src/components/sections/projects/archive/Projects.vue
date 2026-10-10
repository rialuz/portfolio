<script setup lang="ts">
import ProjectCard from './ProjectCard.vue'
import ToDoApp from '../../../data/images/ToDoApp.png'
import Medspot from '../../../data/images/MedspotImg.png'
import SnakeGame from '../../../data/images/SnakeGame.png'
import RPS from '../../../data/images/RPSGame.png'
import { Code2 } from 'lucide-vue-next'

const projects = [
  {
    title: 'To Do App',
    imgSrc: ToDoApp,
    description:
      'Full-stack To Do List application built with Vue.js, Node.js, Remult, and PSQL. The purpose of building this application is to get familiar with Node.js and Remult. Admin users can utilize full CRUD actions on tasks, while non-admin users have read-only access and can update the completed status of a task.',
    githubLink: 'https://github.com/rialuz/todo-app',
    tech: 'Vue.js, Node.js, Express, Remult, PSQL'
  },
  {
    title: 'MedSpot',
    imgSrc: Medspot,
    description:
      'Patient management system full-stack application using React, Java with SpringBoot, PostgreSQL, and JUnit.',
    githubLink: 'https://github.com/rialuz/medspot',
    tech: 'React.js, Java, Springboot, JUnit, PSQL'
  },
  {
    title: "Rock, Paper, Scissor, SHOOT!",
    imgSrc: RPS,
    description:
    'Play a game of Rock, Paper, Scissor against a computer with this cute, aesthetic UI! Local Co-op coming soon. <3',
    githubLink: 'https://github.com/rialuz/rock-paper-scissor',
    tech: 'Vue.js, JavaScript'
  },
  {
    title: 'Snake Game',
    imgSrc: SnakeGame,
    description: 'Have fun eating food and growing your Pacman snake!',
    githubLink: 'https://github.com/rialuz/snake-game',
    tech: 'Java, JFrame'
  }
]
</script>

<template>
  <section id="projects" class="min-h-screen px-6 py-20">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16 animate-slide-up">
        <h2 class="text-5xl font-bold text-gray-800 mb-4 flex items-center justify-center">
          <Code2 :size="48" class="text-light-bronze mr-4" />
          <span class="bg-gradient-to-r from-light-bronze to-dry-sage bg-clip-text text-transparent">
            Projects
          </span>
        </h2>
        <div class="w-24 h-1 bg-light-bronze mx-auto rounded-full"></div>
        <p class="text-gray-600 mt-4 text-lg">Some things I've built</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div 
          v-for="(project, index) in projects" 
          :key="index"
          class="animate-slide-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <ProjectCard
            :img="project.imgSrc"
            :project-name="project.title"
            :description="project.description"
            :github-link="project.githubLink"
            :tech-used="project.tech"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slide-up 0.6s ease-out forwards;
  opacity: 0;
}
</style>
