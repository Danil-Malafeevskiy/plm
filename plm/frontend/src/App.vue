<template>
  <v-app>
    <v-navigation-drawer 
      v-model="drawer" 
      app color="#DDDDDD" 
      :mini-variant.sync="mini" 
      :mini-variant-width=55

    >

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title >
            <v-icon @click.stop="mini = !mini" left>{{ icon }}</v-icon>
            База объектов
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon>{{ item }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>


    <v-main style="overflow: hidden;">
      <v-toolbar color="#E5E5E5">
        <v-toolbar-title>Your Dashboard</v-toolbar-title>
        <template v-slot:extension>
          <v-tabs v-model="tab" align-with-title>
            <v-tabs-slider color="yellow"></v-tabs-slider>

            <v-tab v-for="item in items" :key="item">
              {{ item }}
            </v-tab>
          </v-tabs>
        </template>
      </v-toolbar>

      <v-tabs-items v-model="tab" style="height: 92%;">
        <v-tab-item>
          <div flat>
            <HomePage />
          </div>
        </v-tab-item>
        <v-tab-item>
          <div flat>
            <MapArea />
          </div>
        </v-tab-item>
      </v-tabs-items>
    </v-main>
  </v-app>
</template>
<script>
import HomePage from './components/HomePage.vue'
import MapArea from './components/Map/MapArea.vue'

import { mdiMenu } from '@mdi/js';
// import { mdiHome } from '@mdi/js';
// import { mdiMapMarker } from '@mdi/js';

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
      mini: true,
      icon: mdiMenu,
    }
  },

}
</script>
<style>

.v-tabs-items{
  background-color: #E5E5E5 !important;
}


html{
  overflow: hidden;
}
.v-application code.code--custom {
  all: unset;
  background-color: #E5E5E5;
}


</style>


