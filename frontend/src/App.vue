<template>
  <v-app>
    <img alt="Vue logo" src="./assets/bbc_logo.jpg">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <FileUpload />
  </v-app>
</template>

<script>
import FileUpload from './components/FileUpload.vue';

export default {
  components: {
    FileUpload
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
