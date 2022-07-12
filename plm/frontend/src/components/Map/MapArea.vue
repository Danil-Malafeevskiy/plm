<template>
  <div id="content" style="width: 100%; height: 100%">
    <p>{{ drawType.data }}</p>
    <div id="map_content" style="width: 75%; height: 90%"></div>
    <OverlayInfo :edit='edit' :feature="feature" />

    <EditGeometryObject :feature="feature" :close="close" :showEdit="showEdit" />
    <AddGeometryObject :drawType="drawType" :showAdd="showAdd" :close="close" :cord="cord"
      :addInteraction="addInteraction" />
    <button class="add edit " style="margin-left: 0.5em; padding: 5px;" @click="edit(feature, 'add')">Добавить
      объект</button>
  </div>

</template>

<script>
import EditGeometryObject from './HelpfulFunctions/EditGeometryObject.vue'
import AddGeometryObject from './HelpfulFunctions/AddGeometryObject.vue'
import OverlayInfo from './HelpfulFunctions/OverlayInfo.vue';
import { mapGetters, mapActions } from 'vuex';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat, toLonLat } from 'ol/proj';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { Overlay } from 'ol';
import Draw from "ol/interaction/Draw";

import 'ol/ol.css';

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
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature: null,
      status: false,
      showAdd: false,
      showEdit: false,
      drawType: { data: "-" },
      vectorLayer: null,
      map: null,
      drawSource: new VectorSource({ wrapX: true }),
      drawLayer: new VectorLayer({
        source: this.drawSource,
      }),
      interactionId: null,
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
            }),
          }),
        });

        this.map.addLayer(this.vectorLayer);
      }
    },
  },
  computed: mapGetters(['allFeatures']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature']),

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
      document.querySelector('#card').style.display = 'none';
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
      this.map.addOverlay(new Overlay({
        element: document.querySelector('#card')
      }))

      this.drawSource.clear();
      this.map.getInteractions().getArray()[this.interactionId].finishDrawing();

      document.querySelector('#card').style.display = 'block';
    },

    onMapClick(event) {
      if (this.status) {
        this.cord = event.coordinate;
      }
    },

    getFeature(event) {
      const feature = this.map.getFeaturesAtPixel(event.pixel)[0];
      this.feature = null;

      if (feature != null) {
        this.feature = { properties: feature.getProperties() };
        this.feature['id'] = this.feature.properties.id;
        this.feature['type'] = "Feature";
        this.feature["geometry"] = {
          id: this.feature.id,
          type: feature.getProperties().geometry.getType(),
          coordinates: toLonLat(feature.getProperties().geometry.getCoordinates())
        };
        delete this.feature.properties.geometry;
      }
    },

    addInteraction() {
      if (this.drawType.data != '-') {
        const draw = new Draw({
          source: this.drawSource,
          type: this.drawType.data,
          features: new GeoJSON().readFeatures(this.features, {
            featureProjection: 'EPSG:3857'
          }),
        });
        this.map.removeInteraction(draw);

        this.map.addInteraction(draw);
        this.interactionId = this.map.getInteractions().getArray().length - 1;
      }
    }
  },

  async mounted() {
    await this.getFeatures();

    this.vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: new GeoJSON().readFeatures(this.features, {
          featureProjection: 'EPSG:3857'
        }),
      }),
    });

    this.map = new Map({
      target: 'map_content',
      layers: [
        new TileLayer({
          source: new OSM()
        }),
        this.vectorLayer,
        this.drawLayer,
      ],
      view: new View({
        zoom: 13,
        center: fromLonLat([56, 54]),
        constrainResolution: false,
      })
    });

    this.map.addOverlay(new Overlay({
      element: document.querySelector('#card')
    }));

    this.map.on('click', this.getFeature);

    this.map.on('click', function (event) {
      let overlay = this.getOverlays().getArray()[0];
      overlay.setPosition(undefined);

      this.forEachFeatureAtPixel(event.pixel, function () {
        overlay.setPosition(event.coordinate);
      })
    });
    console.log(this.map.getOverlays().getArray()[0]);
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