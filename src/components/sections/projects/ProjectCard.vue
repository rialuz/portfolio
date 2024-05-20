<script setup lang="ts">
import GithubIcon from '@/components/icons/GithubIcon.vue';
/**
 * Should have Title, description, tech used, imgSrc
 */

</script>

<template>
    <div id="project-card">
        <div class="img-container">
          <img src="" />  
        </div>
        
        <div class="project-description">
            <div class="project-title">
            <h3>Project Name</h3>
            <GithubIcon />                
            </div>

            <div>
                This project is about this, this and that. Built using react, and shit
            </div>

        </div>
    </div>

</template>

<style scoped>

img {

}

.img-container {
    border: 1px solid gold;
    width: inherit;
    height: 150px;
}

.project-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#project-card {
    width: 300px;
    height: 300px;
    border: 1px solid red;
    margin-top: 10px;
}

</style>