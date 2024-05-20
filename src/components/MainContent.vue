<script setup lang="ts">
import AboutMe from './sections/AboutMe.vue'
import Experience from './sections/Experience.vue';
import Projects from './sections/projects/Projects.vue';
</script>

<template>
  <div class="main-content">
    <AboutMe />
    <Experience class="experience  " />
    <Projects />

    
  </div>
</template>
  
<style scoped>
.main-content {
    display: flex;
    flex-direction: column;  
    row-gap: 25px;
    justify-content: center;
    padding-top: 100px;
    margin-bottom: 100px;

}
</style>
