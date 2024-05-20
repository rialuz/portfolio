<script setup lang="ts">
import ProjectCard from './ProjectCard.vue';
</script>

<template>
    <div id="projects" class="projects-section">
        <div class="container">
            <h1 >Projects</h1>
            <div>
               <ProjectCard />  
            </div>
              
        </div>

    </div>

</template>

<style scoped>

.projects-section {
    border: 1px solid black;
    margin: 0 auto;
    width: 80vw;
}

.container {
    height: fit-content;
    padding: 20px
}
</style>