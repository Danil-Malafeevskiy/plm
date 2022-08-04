<template>
  <div id="map_content" style="position: absolute; top: 0; bottom: 0; right: 0; left: 0;"></div>
</template>

<script>
//import { mapGetters, mapActions } from 'vuex';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat, toLonLat } from 'ol/proj';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import { Draw, Modify } from 'ol/interaction';
import { mapMutations, mapActions, mapGetters } from 'vuex';
import 'ol/ol.css';


export default {
  components: {
  },
  props: ['allFeatures', 'visableCard', 'addCardOn', 'infoCardOn', 'notVisableCard', 'editCardOn', 'getFeature'],
  data() {
    return {
      coord: [],
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature: this.getFeature,
      vectorLayer: null,
      map: null,
      drawLayer: null,
      interactionId: null,
      overlayId: null,
      draw: null,
      modify: null,
      addCardOn_: this.addCardOn,
      infoCardOn_: this.infoCardOn,
      editCardOn_: this.editCardOn,
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
    getFeature: function(){
      this.feature = this.getFeature;
    },
    drawType: {
      handler(){
        if (this.addCardOn.data) {
          this.map.removeInteraction(this.draw);
          this.addInteraction();
        }
        else {
          this.map.removeInteraction(this.draw);
          this.drawLayer.getSource().refresh();
          this.map.removeInteraction(this.modify);
        }
      }
    },
    addCardOn: {
      handler() {
        this.addCardOn_ = this.addCardOn;

        if (this.addCardOn.data) {
          this.map.removeInteraction(this.draw);
          this.addInteraction();
        }
        else {
          this.map.removeInteraction(this.draw);
          this.drawLayer.getSource().refresh();
          this.map.removeInteraction(this.modify);
        }
      },
      deep: true
    }
  },
  computed: mapGetters(['drawType']),
  methods: {
    ...mapMutations(['updateOneFeature']),
    ...mapActions(['getOneFeature']),

    async getFeature_(event) {
      if (this.drawLayer.getSource().getFeatures().length === 1) {
        this.map.removeInteraction(this.draw);
      }

      this.coord.push(toLonLat(event.coordinate));
      const feature_ = this.map.getFeaturesAtPixel(event.pixel)[0];

      if (feature_ != null) {
        if (this.addCardOn_.data) {
          if(this.drawType === 'Polygon'){
            this.feature.geometry.coordinates = [this.coord];
          }
          else if (this.drawType === 'LineString'){
            this.feature.geometry.coordinates = this.coord;
          }
          else{
            this.feature.geometry.coordinates = this.coord[0];
          }
          this.feature.properties['Долгота'] = this.coord[0][1];
          this.feature.properties['Широта'] = this.coord[0][0];
          this.feature.type = 'Feature';
          this.feature.geometry.type = this.drawType;
        }
        else {
          await this.getOneFeature(feature_.id_);
          this.infoCardOn_.data = true;
          this.visableCard();
        }
      }
      else if (!this.addCardOn_.data) {
        this.infoCardOn_.data = false;
        this.editCardOn_.data = false;
        this.notVisableCard();
      }
    },

    changeCoordinates(event) {
      this.feature.geometry = {
        coordinates: toLonLat(event.features.getArray()[0].getGeometry().getCoordinates())
      };

      this.feature.properties['Широта'] = this.feature.geometry.coordinates[1];
      this.feature.properties['Долгота'] = this.feature.geometry.coordinates[0];
    },

    addInteraction() {
      this.drawLayer.getSource().refresh();
      this.draw = new Draw({
        source: this.drawLayer.getSource(),
        type: this.drawType,
      });

      this.map.addInteraction(this.draw);
      this.map.addInteraction(this.modify);
      this.interactionId = this.map.getInteractions().getArray().length - 1;
    },
    resizeMap() {
      setTimeout(() => {
        this.map.updateSize();
        if(this.map.getSize()[1] === 0)
          this.resizeMap();
      }, 400);
    }
  },

  mounted() {

    this.drawLayer = new VectorLayer({
      source: new VectorSource({
        features: []
      }),
    });

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
        this.drawLayer
      ],
      view: new View({
        zoom: 13,
        center: fromLonLat([54, 56]),
        constrainResolution: true,
      })
    });

    this.modify = new Modify({
      source: this.drawLayer.getSource(),
    });

    this.modify.on('modifyend', this.changeCoordinates);

    this.map.on('click', this.getFeature_);

    if (this.addCardOn_.data) {
      this.addInteraction();
    }
    this.resizeMap();
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
  transition: all 1s;
}

.animation-leave-active {
  transition: all 1s;
}

.animation-enter,
.animation-leave-to {
  right: 100px;
}
</style>