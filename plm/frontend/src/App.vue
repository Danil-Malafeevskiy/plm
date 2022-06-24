<template>
  <v-app>
    <v-app-bar
      app
      color="red lighten-1"
      dark
    >
      <v-app-bar-title>
        Кронштадт х IT GANG
      </v-app-bar-title>

      <v-spacer></v-spacer>

    </v-app-bar>
    <v-main>
      <HomePage/>
    </v-main>
  </v-app>
</template>

<script>
import HomePage from './components/HomePage';

export default {
  name: 'App',

  components: {
    HomePage,
  },

  data: () => ({
    //
  }),
};
</script>


<style>

  #title{
    color: black;
  }


</style>