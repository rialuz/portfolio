<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainContent from './components/MainContent.vue'
import NavigationBar from './components/NavigationBar.vue';
import Footer from './components/Footer.vue';
import ScrollToTop from './components/ScrollToTop.vue';
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-seashell via-soft-blush to-powder-petal">
    <NavigationBar />
    <MainContent />
    <Footer />
    <ScrollToTop />
  </div>
  <!-- <RouterView /> -->
</template>

<style scoped>
</style>
