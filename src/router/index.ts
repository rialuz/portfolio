import MainContentVue from '@/components/MainContent.vue'
import AboutMe from '@/components/sections/AboutMe.vue'
import Experience from '@/components/sections/Experience.vue'
import Projects from '@/components/sections/projects/Projects.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => {}
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AboutMe
    }, 
    {
      path: '/experience',
      name: 'experience',
      component: Experience
    },
    {
      path: '/projects',
      name: 'projects',
      component: Projects
    }
  ]
})

export default router
