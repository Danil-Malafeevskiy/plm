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

      
      
      <router-view></router-view>
    </v-app-bar>

    <v-main>
      <nav>
          <router-link to='/'>Home</router-link>
            <br>
          <router-link to='/map'>Map</router-link>
        </nav>

      <v-content>

        


      </v-content>
    </v-main>
  </v-app>
</template>

<style>

  #title{
    color: black;
  }

  nav {
  padding: 30px;
  }

  nav a {
    font-weight: bold;
    text-decoration: none;
  }

  nav a.router-link-exact-active {
    color: #EF5350;
    text-decoration: none;
  }

</style>

