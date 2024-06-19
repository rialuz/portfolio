<script setup lang="ts">
import GithubIcon from '@/components/icons/GithubIcon.vue';
/**
 * Should have Title, description, tech used, imgSrc
 */

 const props = defineProps(['projectName', 'img', 'githubLink', 'description', 'techUsed'])

</script>

<template>
    <div id="project-card">
        <div class="img-container">
          <img :src=props.img />  
        </div>
        
        <div class="project-description">
            <div class="project-title">
            <h3>{{ props.projectName }}</h3>
            <a :href=props.githubLink target=”_blank”><GithubIcon  />  </a>
                          
            </div>

            <div>{{ props.description }}</div>
        </div>
        <div class="techStack"><span>TechStack:</span> {{ props.techUsed }}</div>
    </div>

</template>

<style scoped>

#project-card {
    width: 300px;
    height: 450px;
    margin: auto 10px;
    border: 1px solid grey;
    box-shadow: 5px 5px grey;
    display: flex;
    flex-direction: column;
}

img {
    width: -webkit-fill-available;
    height: inherit;
}

.techStack {
    margin-left: 5px;
    margin-right: 5px;

    span {
        font-weight: 600;
    }
}

.project-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    h3{
        font-weight: 500;
    }
    
}

.project-description {
    height: -webkit-fill-available;
    margin-left: 5px;
    margin-right: 5px;
}



</style>