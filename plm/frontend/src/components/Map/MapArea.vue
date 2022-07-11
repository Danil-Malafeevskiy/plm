<template>
  <div id="content" style="width: 100%; height: 100%">
    <p></p>
    <div id="map_content" style="width: 75%; height: 90%"></div>
    <!-- <vl-map data-projection="EPSG:4326" style="height: 50em; width: 65%;" @click="onMapClick">
      <vl-view :zoom.sync="zoom" :center.sync="center" :rotation.sync="rotation"></vl-view>

      <vl-layer-tile>
        <vl-source-osm></vl-source-osm>
      </vl-layer-tile>

      <vl-layer-vector ref="featuresLayer">
        <vl-source-vector ident="drawTarget" :features="allFeatures"></vl-source-vector>
      </vl-layer-vector>

      <div v-if="status && drawType != 'Point'">
        <vl-interaction-draw source="drawTarget" :type="drawType"></vl-interaction-draw>
         <vl-interaction-modify source="drawTarget"></vl-interaction-modify> 
        <vl-interaction-snap source="drawTarget" :priority="10"></vl-interaction-snap>
      </div> 
      <vl-feature v-else-if="status">
        <vl-geom-point :coordinates="cord"></vl-geom-point>
      </vl-feature>

      <OverlayInfo :edit='edit' v-if="!status" />

    </vl-map> -->
    <div v-if="!status">
      <EditGeometryObject :feature="feature" :close="close" :showEdit="showEdit" />
    </div>
    <AddGeometryObject v-model="drawType" :showAdd="showAdd" :close="close" :cord="cord" />
    <button class="add edit " style="margin-left: 0.5em; padding: 5px;" @click="add()">Добавить
      объект</button>
  </div>

</template>

<script>
import EditGeometryObject from './HelpfulFunctions/EditGeometryObject.vue'
import AddGeometryObject from './HelpfulFunctions/AddGeometryObject.vue'
//import OverlayInfo from './HelpfulFunctions/OverlayInfo.vue';
import { mapGetters, mapActions } from 'vuex';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';

import 'ol/ol.css';

export default {
  components: {
    EditGeometryObject,
    AddGeometryObject,
    //OverlayInfo,
  },
  data() {
    return {
      zoom: 13,
      center: [56.105601504697127, 54.937854572222477],
      rotation: 0,
      cord: [NaN, NaN],
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature: null,
      status: false,
      showAdd: false,
      showEdit: false,
      drawType: "Point",
      vectorLayer: null,
      map: null,
    }
  },
  watch: {
    allFeatures: function () {
      this.features = {
        type: 'FeatureCollection',
        features: this.allFeatures,
      }
      
      if (this.map != null) {
        this.map.removeLayer(this.vectorLayer);
        
        this.vectorLayer = new VectorLayer({
          source: new VectorSource({
            features: new GeoJSON().readFeatures(this.features, {
              featureProjection: 'EPSG:3857'
            })
          })
        });

        this.map.addLayer(this.vectorLayer);
      }
    },
  },
  computed: mapGetters(['allFeatures', 'getMap']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature']),
    add() {
      const feature = [{ "type": "Feature", "properties": { "name_tap": "", "number_support": 1, "VL": "НПЗ-ГПП-2 1Т УНХ", "type_support": "Анкерная", "code_support": "не определен", "material": "Металлическая", "corner": 0.7071064293676279, "X": -393.959439006409, "Y": -181.1536460213778, "Z": 221.62639012939093, "shirota": 54, "dolgota": 56, "height": 206.62639012939093, "TPV_photo": "", "UF_photo": "", "photo": "0_12992_DSC01525.JPG;0_13404_DSC01937.JPG;", "v_defects": "Наличие ДКР на земле, отведенной под опору;Cущественные повреждения изоляторов;Cущественные повреждения изоляторов;Cущественные повреждения изоляторов", "u_defects": "", "code_support_in_1C": "", "guid": "", "flag_defects": true, "comment_in_TOiR": "" }, "geometry": { "type": "Point", "coordinates": [56, 54] } }];
      this.postFeature(feature);
    },
    edit(feature, className) {
      document.querySelector('.add').style.opacity = "0";
      this.feature = feature;

      if (className === 'add') {
        this.status = !this.status;
        this.showAdd = !this.showAdd;
      }
      else {
        this.showEdit = !this.showEdit;
      }
    },

    close(className) {
      document.querySelector('.add').style.opacity = "1";

      if (className === 'add') {
        this.status = !this.status;
        this.showAdd = !this.showAdd;
      }
      else {
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
  async mounted() {
    await this.getFeatures();

    this.vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: new GeoJSON().readFeatures(this.features, {
          featureProjection: 'EPSG:3857'
        })
      })
    });

    this.map = new Map({
      target: 'map_content',
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        this.vectorLayer,
      ],
      view: new View({
        zoom: 13,
        center: fromLonLat([56, 54]),
        constrainResolution: true,
      })
    });
  }
}
</script>

<style>
.v-main__wrap {
  display: flex;
}

#content {
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

.edit:hover {
  border: 1px solid #EF5350;
  box-shadow: 0 0 10px rgba(239, 83, 80, 0.5);
}

.add {
  min-width: 5em;
  max-height: 2.5em;
}

.add_window,
.edit_window {
  padding-left: 1em;
  margin-left: 1em;
  border-left: 1px solid black;
  transition: all 1s;
}

.edit_window {
  min-height: 800px;
}

.slow {
  max-height: 2000px;
}

.save {
  margin-left: 1em;
}

.v_content {
  min-width: 100%;
}

.animation-enter-active {
  transition: all .3s ease;
}

.animation-leave-active {
  transition: all .3s;
}

.animation-enter,
.animation-leave-to {
  transform: translateX(10em);
  opacity: 0;
}
</style>