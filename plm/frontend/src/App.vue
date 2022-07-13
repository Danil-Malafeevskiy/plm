<template>

  <v-app :style="{background: $vuetify.theme.themes.light.background}">
    <v-main style="overflow: hidden;">
      <v-toolbar>
        <v-toolbar-title>Your Dashboard</v-toolbar-title>
        <template v-slot:extension>
          <v-tabs
            v-model="tab"
            align-with-title
          >
            <v-tabs-slider color="yellow"></v-tabs-slider>
  
            <v-tab
              v-for="item in items"
              :key="item"
            >
              {{ item }}
            </v-tab>
          </v-tabs>
        </template>
      </v-toolbar>
  
      <v-tabs-items v-model="tab" style="height: 92%;">
        <v-tab-item>
          <div flat>
            <HomePage/>
          </div>
        </v-tab-item >
        <v-tab-item>
          <div flat >
            <MapArea/>
          </div>
        </v-tab-item>
      </v-tabs-items>
      </v-main>
  </v-app>
</template>
<script>
import HomePage from './components/HomePage.vue'
import MapArea from './components/Map/MapArea.vue'

export default {
  components:{
    HomePage,
    MapArea
  },
  data () {
    return {
      tab: null,
      items: [
        'Home', 'Map'
      ],
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    }
  },
}
</script>
<style>
html{
  overflow: hidden;
}
.v-application code.code--custom {
  all: unset;
  background-color: #E5E5E5;
}


</style>


