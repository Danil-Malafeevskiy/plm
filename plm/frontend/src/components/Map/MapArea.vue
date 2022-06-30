<template>
  <v-content id="content">
    <vl-map data-projection="EPSG:4326" style="height: 37.5em; width: 75em;">
      <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

      <vl-layer-tile>
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>

      <vl-feature>
        <vl-geom-point :coordinates="[38.726634,9.003391]"></vl-geom-point>
      </vl-feature>
    </vl-map>
  </v-content>
</template>

<script>
import axios from 'axios'

export default {
    data () {
      return { 
        zoom: 17,
        center: [38.7241, 9.0048],
        rotation: 0,
      }
    },
  };

  function point(){
    axios.
        get("/tower")
        .then( (response) => console.log(response.data[0].shirota))
        

  }
  point();
</script>

<style>
  #content{
    margin-top: 40em;
  }
</style>