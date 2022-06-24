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
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',

  components: {
    HelloWorld,
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