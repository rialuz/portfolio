<script setup lang="ts">
import ProjectCard from './ProjectCard.vue';
import ToDoApp from '../../data/images/ToDoApp.png'

const toDoAppImg = ToDoApp

const projects = [
    {
        title: 'To Do App',
        imgSrc: toDoAppImg,
        description: 'Full-stack Task List application built with Vue.js, Node.js, and PSQL. A user is able to view to do tasks, create new tasks, update existing tasks, and delete tasks. Set up authorization and authentication so a user has a simple login with their username and if they are an admin user, they can utilize full CRUD actions.',
        githubLink: 'https://github.com/rialuz/todo-app   ',
        tech: 'Vue.js, Node.js, Remult, PSQL'
    },
    {
        title: '',
        imgSrc: '',
        description: '',
        githubLink: '',
        tech: ''
    },
]

</script>

<template>
    <div id="projects" class="projects-section">
        <div class="container">
            <h1 >Projects</h1>
            <div class="project-cards">
            <div v-for="project of projects" >
                <!-- 'projectName', 'img', 'githubLink', 'description', 'techUsed' -->
               <ProjectCard :img=project.imgSrc :project-name=project.title :description=project.description :github-link=project.githubLink :tech-used=project.tech />  
            </div>                
            </div>

              
        </div>

    </div>

</template>

<style scoped>

.projects-section {
    border: 1px solid black;
    margin: 0 auto;
    width: 80vw;
    color: #3d52a0;
}

.container {
    height: fit-content;
    padding: 20px
}

.project-cards {
    display: flex;
}
</style>