<script setup>
import GithubIcon from './icons/GithubIcon.vue';
import LinkedInIcon from './icons/LinkedInIcon.vue' 

const redirect = (link) => {
    return window.location.replace(link);
}

</script>

<template>
    <div class="nav">
        <div class="menu-nav-items">
            <h3>Luz Lopez Marcano</h3>
            <div class="nav-links">
            <a href="#about">
                <h4>About</h4>
            </a>
            <a href="#experience">
                <h4>Experience</h4>
            </a>
            <a href="#projects">
                <h4>Projects</h4>
            </a>                
            </div>




        </div>

        <div class="socials">
            <!-- Icons - Email, LinkedIn, Github -->
            <a href="https://github.com/rialuz?tab=repositories" >
            <GithubIcon />
            </a>
            
            <a href="https://www.linkedin.com/in/luzlmarcano/" >
            <LinkedInIcon /> 
            </a>
        </div>
    </div>

</template>

<style scoped>

.nav {
    background: #ede8f5;
    height: 50px;
    display: flex;
    justify-content: space-between;
    position: fixed;
    top: 0;
    width: 100%;
    padding-bottom: 50px;
    z-index: 1;
    

    h3, h4{
        padding-left: 10px;
        align-content: center;
        font-weight: bold;
    }
}

.menu-nav-items {
    display: flex;
    height: 50px;
    align-items: center;

    .nav-links {
    display: flex;
    padding: 10px;
    }

    a {
        color: #3d52a0;
        text-decoration: none;  
    }
}

</style>