<template>
  <div id="content" style="width: 100%; height: 100%; position: absolute; overflow-y: scroll;">
    <div id="map_content" style="width: 75%; height: 90%; "></div>
    <OverlayInfo :edit='edit' :feature="feature" :overlay="map === null ? null : map.getOverlays().getArray()[this.overlayId]"/>
    <EditGeometryObject :feature="feature" :close="close" :showEdit="showEdit" />
    <AddGeometryObject :drawType="drawType" :showAdd="showAdd" :close="close" :interaction="interaction"
      :clearDrawLayer="clearDrawLayer" :feature="allFeatures[0]" :coord="coord"/>
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
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';
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
      coord: { data: [NaN, NaN]},
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature: null,
      showAdd: false,
      showEdit: false,
      drawType: { data: "Point" },
      vectorLayer: null,
      map: null,
      drawLayer: null,
      interactionId: null,
      overlayId: null,
      draw: null,
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
        this.showAdd = !this.showAdd;
        this.addInteraction();
      }
      else {
        this.showEdit = !this.showEdit;
      }
      document.querySelector('#card').style.display = 'none';
    },

    close(className) {
      document.querySelector('.add').style.opacity = "1";
      this.drawLayer.getSource().refresh();
      if (className === 'add') {
        this.showAdd = !this.showAdd;
      }
      else {
        this.showEdit = !this.showEdit;
      }
      this.coord.data = [NaN, NaN];

      this.map.removeInteraction(this.draw);

      document.querySelector('#card').style.display = 'block';
    },

    getFeature(event) {
      if (this.drawLayer.getSource().getFeatures().length === 1) {
        this.coord.data = this.drawLayer.getSource().getFeatures()[0].getGeometry().getCoordinates();
        this.map.removeInteraction(this.draw);
      }

      const feature = this.map.getFeaturesAtPixel(event.pixel)[0];
      this.feature = null;

      if (feature != null && !this.showAdd) {
        this.feature = { properties: feature.getProperties() };
        this.feature['id'] = this.feature.properties.id;
        this.feature['type'] = "Feature";
        this.feature["geometry"] = {
          id: this.feature.id,
          type: feature.getProperties().geometry.getType(),
          coordinates: toLonLat(feature.getProperties().geometry.getCoordinates())
        };
        delete this.feature.properties.geometry;
        this.map.getOverlays().getArray()[this.overlayId].setPosition(event.coordinate);
      }
      else {
        this.map.getOverlays().getArray()[this.overlayId].setPosition(undefined);
      }
    },

    addInteraction() {
      this.drawLayer.getSource().refresh();
      if (this.drawType.data != '-') {
        this.draw = new Draw({
          source: this.drawLayer.getSource(),
          type: this.drawType.data,
        });

        this.map.addInteraction(this.draw);
        this.interactionId = this.map.getInteractions().getArray().length - 1;
      }
    },
    interaction() {
      this.map.removeInteraction(this.draw);
      this.addInteraction();
    },
    clearDrawLayer() {
      this.drawLayer.getSource().refresh();
    }
  },

  async mounted() {
    await this.getFeatures();

    this.drawLayer = new VectorLayer({
      source: new VectorSource({
        features: []
      }),
      style: new Style({
        fill: new Fill({
          color: 'rgba(255, 255, 0, 0.2)',
        }),
        stroke: new Stroke({
          color: '#ff0000',
          width: 2,
        }),
        image: new CircleStyle({
          radius: 7,
          fill: new Fill({
            color: '#ff0000',
          }),
        }),
      }),
    });

    this.vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: new GeoJSON().readFeatures(this.features, {
          featureProjection: 'EPSG:3857'
        }),
      })
    }),

      this.map = new Map({
        target: 'map_content',
        layers: [
          new TileLayer({
            source: new OSM()
          }),
          this.vectorLayer,
          this.drawLayer
        ],
        view: new View({
          zoom: 13,
          center: fromLonLat([56.105601504697127, 54.937854572222477]),
          constrainResolution: true,
        })
      });

    this.map.addOverlay(new Overlay({
      element: document.querySelector('#card')
    }));
    this.overlayId = this.map.getOverlays().getArray().length - 1;

    this.map.on('click', this.getFeature);
  }
}
</script>

<style>

#content {
  padding-left: 5em;
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