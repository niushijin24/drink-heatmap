<script setup lang="ts">
import HeatCalendar from './components/HeatCalendar.vue'
</script>

<template>
  <div class="app-container">
    <div class="calendar-focused">
       <div class="minimal-header">
          <span class="logo">🍻 Drink Heatmap</span>
       </div>
       <HeatCalendar />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 5px; /* Reduced from 10px */
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
  color: #fff;
  display: flex;
  justify-content: center;
  overflow-y: auto;
}

.calendar-focused {
    width: 100%;
    max-width: 520px;
    display: flex;
    flex-direction: column;
    height: auto;
    min-height: 100%;
    padding: 20px 0;
}

.minimal-header {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 0 10px 0; /* Reduced from 15px */
    gap: 8px;
}

.icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.logo {
  font-size: 2rem; /* Reduced from 2.5rem */
  font-weight: bold;
  background: linear-gradient(135deg, #ff00cc, #3333ff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

@media (max-width: 600px) {
    .logo {
        font-size: 1.2rem; /* Reduced from 1.5rem */
    }
    .calendar-focused {
        padding: 10px 0;
    }
}
</style>

<style>
body {
  background-color: #1a1a1a;
  margin: 0;
}

@media (max-width: 600px) {
    body {
        overflow: hidden !important; /* Force scroll-free on mobile */
    }
}
</style>
