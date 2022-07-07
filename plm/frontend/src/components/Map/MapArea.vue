<template>
  <v-content id="content">
    <vl-map data-projection="EPSG:4326" style="height: 37.5em; width: 75em;" @click="onMapClick">
      <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

      <vl-layer-tile>
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>


      <vl-layer-vector ref="featuresLayer">
        <vl-source-vector ident="drawTarget" :features="features"></vl-source-vector>
      </vl-layer-vector>

      <div v-if="status">
        <vl-interaction-draw source="drawTarget" :type="drawType"></vl-interaction-draw>
        <!-- <vl-interaction-modify source="drawTarget"></vl-interaction-modify> -->
        <vl-interaction-snap source="drawTarget" :priority="10"></vl-interaction-snap>
      </div>


      <OverlayInfo :edit='edit' />

    </vl-map>
    <div v-if="!status">
      <EditGeometryObject :feature="feature" :close="close" />
    </div>
    <AddGeometryObject v-model="drawType" :close="close" :cord="cord" />
    <button class="add edit" @click="edit(feature, '.add_window')">Добавить объект</button>
  </v-content>
</template>

<script>
import axios from 'axios'
import EditGeometryObject from './HelpfulFunctions/EditGeometryObject.vue'
import AddGeometryObject from './HelpfulFunctions/AddGeometryObject.vue'
import OverlayInfo from './HelpfulFunctions/OverlayInfo.vue';



export default {
  components: {
    EditGeometryObject,
    AddGeometryObject,
    OverlayInfo,
  },
  data() {
    return {
      zoom: 13,
      center: [56.105601504697127, 54.937854572222477],
      rotation: 0,
      cord: [],
      features: [],
      feature: null,
      status: false,
      drawType: "Point",
    }
  },
  methods: {
    point() {
      axios.get("/tower")
        .then((response) => {
          this.features = response.data;
          console.log(this.features);
        });
    },
    edit(feature, className) {
      document.querySelector(className).style.display = "block";
      document.querySelector('.add').style.display = "none";
      this.feature = feature;
      if (className === '.add_window') {
        this.status = !this.status
      }
    },

    close(className) {
      document.querySelector(className).style.display = "none";
      document.querySelector('.add').style.display = "block";
      if (className === '.add_window') {
        this.status = !this.status;
      }
      this.cord = [NaN, NaN];
    },

    onMapClick(event) {
      if (this.status) {
        this.cord = event.coordinate;
      }
    },
    
  },
  mounted() {
    this.point();
  }
};
</script>

<style>
#content {
  margin-top: 40em;
}

.v-main__wrap {
  display: flex;
}

#card {
  background: white;
  border: 1px solid grey;
  color: black;
  padding: 0.5em;
  border-radius: 8%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 0 10px rgba(128, 128, 128, 0.5);
}

.edit {
  border: 1px solid grey;
  padding: 2px;
}

.add {
  min-width: 5em;
  max-height: 2.5em;

}

.edit_window {
  border-left: 1px solid black;
  min-width: 20em;
}

.save {
  margin-left: 1em;
}
</style>