<template>
  <v-content id="content">
    <div>
    <vl-map data-projection="EPSG:4326" style="height: 37.5em; width: 75em;">
      <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

      <vl-layer-tile>
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>

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
              Высота: {{ feature.properties.height }}<br>
              <button class="edit" @click="edit(feature)">Редактировать</button>
            </div>
          </vl-overlay>
        </template>
      </vl-interaction-select>

    </vl-map>
    </div>
    <AddGeometryObject :feature="feature" :close="close"/>
  </v-content>
</template>

<script>
import features from '@/components/Map/coordinates.js';
import AddGeometryObject from './AddGeometryObject.vue'
import axios from 'axios'

export default {
  components:{
    AddGeometryObject
  },
    data () {
      return { 
        zoom: 13,
        center: [56.105601504697127, 54.937854572222477],
        rotation: 0,
        cord: [],
        features: features,
        feature: null,
      }
    },
    methods: {
      point(){
        axios.get("/tower")
        .then((response) => {
            this.cord = response.data;
      })
      },
      edit(feature){
        document.querySelector('.edit_window').style.display = "block";
        this.feature = feature;  
        },
        close(){
          document.querySelector('.edit_window').style.display = "none";
        },
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

  .v-main__wrap{
    display: flex;
  }

  #card{
    background: white; 
    border: 1px solid grey; 
    color: black;
    padding: 0.5em;
    border-radius: 8%;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    box-shadow: 0 0 10px rgba(128, 128, 128, 0.5);
  }

  .edit{
    border: 1px solid grey;
    padding: 2px;
  }

  .edit_window{
    border-left: 1px solid black;
    min-width: 20em;
  }

  .save{
    margin-left: 1em;
  }
</style>