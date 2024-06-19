<script setup lang="ts">
import ProjectCard from './ProjectCard.vue';
import ToDoApp from '../../data/images/ToDoApp.png'
import Medspot from '../../data/images/MedspotImg.png'

const toDoAppImg = ToDoApp

const projects = [
    {
        title: 'To Do App',
        imgSrc: toDoAppImg,
        description: 'Full-stack To Do List application built with Vue.js, Node.js, Remult, and PSQL. The purpose of building this application is to get familiar with Node.js and Remult. Admin users can utilize full CRUD actions on tasks, while non-admin users have read-only access and can update the completed status of a task.',
        githubLink: 'https://github.com/rialuz/todo-app',
        tech: 'Vue.js, Node.js, Express, Remult, PSQL'
    },
    {
        title: 'MedSpot',
        imgSrc: Medspot,
        description: 'Patient management system full-stack application using React, Java with SpringBoot, PostgreSQL, and JUnit',
        githubLink: 'https://github.com/rialuz/medspot',
        tech: 'React.js, Java, Springboot, JUnit, PSQL'
    },
]

</script>

<template>
    <div id="projects" class="projects-section">
        <div class="container">
            <h1 >Projects</h1>
            <div class="project-cards">
            <div v-for="project of projects" >
               <ProjectCard :img=project.imgSrc :project-name=project.title :description=project.description :github-link=project.githubLink :tech-used=project.tech />  
            </div>                
            </div>
        </div>

    </div>

</template>

<style scoped>

.projects-section {
    margin: 0 auto;
    width: 80vw;
    color: #3d52a0;
}

.container {
    height: fit-content;
    padding: 20px
}

.project-cards {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    overflow-x: scroll;
}

::-webkit-scrollbar {
    width: 5px;
}

</style>