<template>
  <AppLayout />
</template>

<script setup>
import AppLayout from './components/AppLayout.vue';
</script>

<style>
/* Ensure Tailwind is imported in your main.js or style block */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background-color: #f9fafb; /* bg-gray-50 */
}
</style>