<template>
  <v-content id="content">
    <vl-map data-projection="EPSG:4326" style="height: 37.5em; width: 75em;">
      <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

      <vl-layer-tile>
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>

      <vl-feature>
        <vl-geom-multi-point :coordinates="cord"></vl-geom-multi-point>
      </vl-feature>

      <vl-layer-vector ref="featuresLayer">
        <vl-source-vector :features="features"></vl-source-vector>
      </vl-layer-vector>

      <vl-interaction-select :features.sync="selectedFeatures">
        <template slot-scope="select">
          <vl-overlay v-for="feature in select.features" :key="feature.id" :id="feature.id"
                        :position="feature.geometry.coordinates" :auto-pan="true">
            <div id="card">
              Точка № {{ feature.properties.id }}<br>
              Номер опоры: {{ feature.properties.number_support }} <br>
              ВЛ: {{ feature.properties.VL }} <br>
              Тип опоры: {{ feature.properties.type_support }} <br>
              Шифр опоры: {{ feature.properties.code_support }} <br>
              Материал: {{ feature.properties.material }} <br>
              Угол: {{ feature.properties.corner }} <br>
              Высота: {{ feature.properties.height }}
            </div>
          </vl-overlay>
        </template>
      </vl-interaction-select>

    </vl-map>
  </v-content>
</template>

<script>
import features from '@/components/Map/coordinates.js';
  
import axios from 'axios'
export default {
    data () {
      return { 
        zoom: 13,
        center: [56.105601504697127, 54.937854572222477],
        rotation: 0,
        cord: [],
        features: features,

      }
    },
    methods: {
      point(){
        axios.get("/tower")
        .then((response) => {
          response.data.forEach(element =>
            this.cord.push([element.dolgota, element.shirota]));
          })
      }
    },
    mounted() {
     this.point();
    }
  };
</script>

<style>
  #content{
    margin-top: 40em;
  }

  #card{
    background: white; 
    border: 1px solid grey; 
    color: black;
    padding: 0.5em;
    border-radius: 8%;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
</style>