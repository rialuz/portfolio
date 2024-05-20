<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainContent from './components/MainContent.vue'
import NavigationBar from './components/NavigationBar.vue';
import   Footer from './components/Footer.vue';
</script>

<template>
    <div class="wrapper">
      <NavigationBar />
      <MainContent />
      <Footer />
    </div>

  <!-- <RouterView /> -->
</template>

<style scoped>
.wrapper {
    /* height: 100vh;
    width: 100vw; */
    text-decoration: none;
}
</style>
