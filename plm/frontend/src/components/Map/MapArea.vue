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
import Draw from "ol/interaction/Draw";
import { Circle as CircleStyle, Fill, Stroke, Style } from 'ol/style';
import { mapMutations } from 'vuex';
import 'ol/ol.css';


export default {
  components: {
  },
  props: ['allFeatures', 'cord', 'visableCard', 'addCardOn', 'infoCardOn'],
  data() {
    return {
      coord: this.cord,
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature_: null,
      showAdd: false,
      showEdit: false,
      drawType: { data: "Point" },
      vectorLayer: null,
      map: null,
      drawLayer: null,
      interactionId: null,
      overlayId: null,
      draw: null,
      addCardOn_: this.addCardOn,
      infoCardOn_: this.indoCardOn,
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
    addCardOn: function () {
      this.addCardOn_ = this.addCardOn;

      if (this.addCardOn) {
        this.map.removeInteraction(this.draw);
        this.addInteraction();
      }
      else {
        this.map.removeInteraction(this.draw);
        this.drawLayer.getSource().refresh();
      }
    }
  },
  methods: {
    ...mapMutations(['updateFeature']),
    getFeature(event) {
      if (this.drawLayer.getSource().getFeatures().length === 1) {
        this.coord.data = this.drawLayer.getSource().getFeatures()[0].getGeometry().getCoordinates();
        this.map.removeInteraction(this.draw);
      }

      this.coord.data = event.coordinate;
      const feature_ = this.map.getFeaturesAtPixel(event.pixel)[0];

      if (feature_ != null && !this.addCardOn) {
        this.feature_ = { properties: feature_.getProperties() };
        this.feature_['id'] = this.feature_.properties.id;
        this.feature_['type'] = "Feature";
        this.feature_["geometry"] = {
          id: this.feature_.id,
          type: feature_.getProperties().geometry.getType(),
          coordinates: toLonLat(feature_.getProperties().geometry.getCoordinates())
        };
        delete this.feature_.properties.geometry;
        this.updateFeature(this.feature_);
        this.visableCard();
      }
    },

    addInteraction() {
      this.drawLayer.getSource().refresh();
      this.draw = new Draw({
        source: this.drawLayer.getSource(),
        type: this.drawType.data,
      });

      this.map.addInteraction(this.draw);
      this.interactionId = this.map.getInteractions().getArray().length - 1;
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
          center: fromLonLat([54, 56]),
          constrainResolution: true,
        })
      });
    this.map.on('click', this.getFeature);

    if (this.addCardOn) {
      this.map.removeInteraction(this.draw);
      this.addInteraction();
    }
    else {
      this.map.removeInteraction(this.draw);
      this.drawLayer.getSource().refresh();
    }

    setTimeout(() => {
      this.map.updateSize();
    }, 400);
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