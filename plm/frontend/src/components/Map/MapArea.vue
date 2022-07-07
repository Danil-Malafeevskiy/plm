<template>
  <div id="content">
    <vl-map data-projection="EPSG:4326" style="height: 50em; width: 75em;" @click="onMapClick">
      <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

      <vl-layer-tile>
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>


      <vl-layer-vector ref="featuresLayer">
        <vl-source-vector ident="drawTarget" :features="features"></vl-source-vector>
      </vl-layer-vector>

      <!-- <div v-if="status">
        <vl-interaction-draw source="drawTarget" :type="drawType"></vl-interaction-draw>
         <vl-interaction-modify source="drawTarget"></vl-interaction-modify> 
        <vl-interaction-snap source="drawTarget" :priority="10"></vl-interaction-snap>
      </div>  -->
      
      <vl-feature v-if="status">
        <vl-geom-point :coordinates="cord"></vl-geom-point>
      </vl-feature>

      <OverlayInfo :edit='edit' v-if="!status"/>

    </vl-map>
    <div v-if="!status">
      <EditGeometryObject :feature="feature" :close="close" :showEdit="showEdit"/>
    </div>
    <AddGeometryObject v-model="drawType" :showAdd="showAdd" :close="close" :cord="cord" />
    <button  class="add edit hidden" style="margin-left: 1em; padding: 5px;" @click="edit(feature, 'add')">Добавить объект</button>
  </div>
  
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
      cord: [NaN, NaN],
      features: [],
      feature: null,
      status: false,
      showAdd: false,
      showEdit: false,
      drawType: "Point",
    }
  },
  methods: {
    point() {
      axios.get("/tower")
        .then((response) => {
          this.features = response.data;});
    },
    edit(feature, className) {
      document.querySelector('.add').style.display = "none";
      this.feature = feature;
      
      if (className === 'add') {
        this.status = !this.status;
        this.showAdd = !this.showAdd;
      }
      else{
        this.showEdit = !this.showEdit;
      }
    },

    close(className) {
      document.querySelector('.add').style.display = "block";
      
      if (className === 'add') {
        this.status = !this.status;
        this.showAdd = !this.showAdd;
      }
      else{
        this.showEdit = !this.showEdit;
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

.v-main__wrap {
  display: flex;
}

#content{
  display: flex;
  padding-left: 5em;
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
  margin-bottom: 5px;
  border-radius: 7px;
  transition: .3s;
}

.edit:hover{
  border: 1px solid #EF5350;
  box-shadow: 0 0 10px rgba(239, 83, 80, 0.5); 
}

.add {
  min-width: 5em;
  max-height: 2.5em;

}

.add_window, .edit_window{
    padding-left: 1em;
    margin-left: 1em;
    border-left: 1px solid black;
    transition: all 1s;
}

.edit_window{
  min-height: 800px;
}

.slow{
  max-height: 2000px;
}

.save {
  margin-left: 1em;
}

.v_content{
  min-width: 100%;
}

.animation-enter-active {
  transition: all .3s ease;
}
.animation-leave-active {
  transition: all .3s;
}
.animation-enter, .animation-leave-to {
  transform: translateX(10em);
  opacity: 0;
}
</style>