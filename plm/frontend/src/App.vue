<template>
  <div id="app">
    
    <img alt="KT logo" 
      src="https://upload.wikimedia.org/wikipedia/commons/7/7c/AO_Kronstadt_Group_logo.jpg"
      width="297.3"
      height="91.7"
    >
    <HomePage msg="КРОНШТАДТ Х IT GANG"/>
  </div>
</template>

<script>
import HomePage from './components/CommonPages/HomePage.vue'

export default {
  name: 'App',
  components: {
    HomePage
}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
