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

import {Icon, Style} from 'ol/style';
import Select from 'ol/interaction/Select';
import Stroke from 'ol/style/Stroke';

import Feature from 'ol/Feature';
// import Translate from 'ol/interaction/Translate';
import LineString from 'ol/geom/LineString';


export default {
  components: {
  },
  props: ['allFeatures', 'visableCard', 'addCardOn', 'infoCardOn', 'notVisableCard', 'editCardOn', 'getFeature'],
  data() {
    return {
      coord: [],
      coordEdit: [],
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature: this.getFeature,
      featurePoint: {},
      featureLine: {},
      featurePolygon: {},
      vectorLayerPoint: null,
      vectorLayerLine: null,
      vectorLayerPolygon: null,
      selectInteractionLineString: null,
      map: null,
      drawLayer: new VectorLayer({
        source: new VectorSource()
      }),
      interactionId: null,
      overlayId: null,
      draw: null,
      modify: null,
      modifyEdit: null,
      addCardOn_: this.addCardOn,
      infoCardOn_: this.infoCardOn,
      editCardOn_: this.editCardOn,
      selectInteraction: null,
      editFeatures: null,
      objectForCard: {},
      editedPointCoordinates: null,
      editedTypeId: null,
    }
  },
  watch: {
    allFeatures: {
      handler() {
        this.features = {
          type: 'FeatureCollection',
          features: this.allFeatures,
        }
        if (this.map != null) {
          this.addNewLayers();
        }
      }
    },

    getObjectForCard: {
      handler() {
        this.objectForCard = this.getObjectForCard;
      }
    },

    getFeature: function () {
      this.feature = this.getFeature;
    },
    drawType: {
      handler() {
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
    },

  },
  computed: mapGetters(['drawType', 'allType', 'typeForLayer', 'getObjectForCard', 'arrayEditMode', 'oneType']),
  methods: {
    ...mapMutations(['updateOneFeature', 'upadateEmptyObject', 'updateObjectForCard']),
    ...mapActions(['getOneFeature', 'getOneTypeObject']),
    updateLonLat(cord) {
      this.feature.properties['Долгота'] = cord[1];
      this.feature.properties['Широта'] = cord[0];
    },

    updateCoordinates() {
      if (this.drawLayer.getSource().getFeatures().length === 1) {
        this.map.removeInteraction(this.draw);
        this.coord = this.drawLayer.getSource().getFeatures()[0].getGeometry().getCoordinates();
        if (typeof this.coord[0] === 'object') {
          for (let i in this.coord) {
            if (typeof this.coord[i][0] === 'object') {
              for (let j in this.coord[i]) {
                this.coord[i][j] = toLonLat(this.coord[i][j]);
                this.updateLonLat(this.coord[0][0]);
              }
            }
            else {
              this.coord[i] = toLonLat(this.coord[i]);
            }
          }
        }
        else {
          this.coord = toLonLat(this.coord);
          this.updateLonLat(this.coord);
          this.map.removeInteraction(this.modifyEdit)
        }

        this.feature.geometry.coordinates = this.coord;
        this.feature.type = 'Feature';
        this.feature.geometry.type = this.drawType;
      }
    },

    findItem(id) {
      let item = this.arrayEditMode.put.filter(el => el.id === id);
      if (item.length) {
        return item[0];
      }
      else {
        return false;
      }
    },

    async getFeature_(event) {
      this.updateCoordinates();
      const feature_ = this.map.getFeaturesAtPixel(event.pixel)[0];

      if (feature_ != null && !this.addCardOn_.data) {
        let item = this.findItem(feature_.id_)
        if (item) {
          this.updateObjectForCard(JSON.parse(JSON.stringify(item)));
        }
        else {
          await this.getOneFeature(feature_.id_);
        }
        this.infoCardOn_.data = true;
        this.visableCard();
      }
      else if (!this.addCardOn_.data) {
        this.infoCardOn_.data = false;
        this.editCardOn_.data = false;
        this.notVisableCard();
      }
    },

    changeCoordinates(event) {
      this.feature.geometry.coordinates = toLonLat(event.features.getArray()[0].getGeometry().getCoordinates())
    },

    changeCoordinatesEdit(event) {

      this.map.getLayers().forEach(element => {

        if (element.get('typeId') != undefined) {
          element.getSource().getFeatures().forEach(el => {
            if (el.getGeometry().getType() === 'LineString') {

              el.getGeometry().getCoordinates().forEach((coord, index) => {
                coord = toLonLat(coord)
                coord[0] = parseFloat(coord[0].toFixed(6))
                coord[1] = parseFloat(coord[1].toFixed(6))
                
                if (coord.includes(this.editedPointCoordinates[0]) && coord.includes(this.editedPointCoordinates[1])){
                  this.editedTypeId = element.get('typeId')

                  let feature = el.getGeometry().getCoordinates()
                  feature[index] = event.features.getArray()[0].getGeometry().getCoordinates()
                  feature.forEach((element, index) => {
                    feature[index] = fromLonLat(element)
                    feature[index][0] = parseFloat(element[0].toFixed(6))
                    feature[index][1] = parseFloat(element[1].toFixed(6))
                  });


                  const newFeature = new Feature({
                    geometry: new LineString(feature),
                  });

                  console.log(feature)


                  let features = {
                    type: 'FeatureCollection',
                    features: newFeature,
                  };
                
                  let layer = new VectorLayer({
                    source: new VectorSource({
                      features: new GeoJSON().readFeatures(features,
                        {
                          featureProjection: 'EPSG:3857'
                        }),
                    }),
                  });

                  let arrayOfLayers = this.map.getAllLayers();
                  arrayOfLayers.forEach(element => {
                    if (element.get('typeId') === this.editedTypeId) {
                      this.map.removeLayer(element)
                    }
                  })
                  this.map.addLayer(layer)

                  console.log(this.map.getLayers())
                }
              });
            }
          });
        }
      });

      this.objectForCard.geometry.coordinates = toLonLat(event.features.getArray()[0].getGeometry().getCoordinates())
      this.objectForCard.geometry.type = 'Point'
    },

    async addInteraction() {
      this.drawLayer.getSource().refresh();
      await this.getOneTypeObject({ id: this.oneType.id, forFeature: true });

      this.drawLayer = new VectorLayer({
        source: new VectorSource({
          features: []
        }),
      });

      if (this.drawType === 'Point') {
        this.drawLayer.setStyle(new Style({
          image: new Icon({
            anchor: [0.5, 0, 5],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: document.getElementById('2').toDataURL('image/png'),
          }),
        }));
      }
      this.modify = new Modify({
        source: this.drawLayer.getSource(),
        style: this.drawLayer.getStyle()
      });

      this.modify.on('modifyend', this.changeCoordinates);

      this.draw = new Draw({
        source: this.drawLayer.getSource(),
        type: this.drawType,
        style: this.drawLayer.getStyle(),
      });

      this.map.addLayer(this.drawLayer);
      this.map.addInteraction(this.draw);
      this.map.addInteraction(this.modify);
      this.interactionId = this.map.getInteractions().getArray().length - 1;
    },

    resizeMap() {
      setTimeout(() => {
        this.map.updateSize();
        if (this.map.getSize()[1] === 0)
          this.resizeMap();
      }, 400);
    },


    addNewLayers() {
      this.allType.forEach(async element => {
        let features = {
          type: 'FeatureCollection',
          features: this.features.features.filter(el => el.name === element.id),
        };
        await this.getOneTypeObject({ id: element.id, forFeature: true });
        let layer = new VectorLayer({
          source: new VectorSource({
            features: new GeoJSON().readFeatures(features,
              {
                featureProjection: 'EPSG:3857'
              }),
          }),
        });
        layer.set('typeId', element.id);
        
        
        this.map.addLayer(layer)

        if (features.features.length && features.features[0].geometry.type === 'LineString') {
          let selectStyle = new Style({
            stroke: new Stroke({ color: "red" })
          });

          this.selectInteractionLineString = new Select({
            style: selectStyle,
            layers: [layer],
            multi: true,
          });
        
          this.map.addInteraction(this.selectInteractionLineString) 

          this.modifyEdit = new Modify({
            features: this.selectInteractionLineString.getFeatures(),
            style: selectStyle
          })
          this.map.addInteraction(this.modifyEdit)

        }
        else if (features.features.length && features.features[0].geometry.type === 'Point' && !(this.typeForLayer.image === '')) {
          let style = new Style({
            image: new Icon({
              anchor: [0.5, 0, 5],
              anchorXUnits: 'fraction',
              anchorYUnits: 'pixels',
              src: `static/${this.typeForLayer.image}`,
            }),
          });
          layer.setStyle(style)

          let selectStyle = new Style({
            image: new Icon({
              anchor: [0.5, 0.5],
              anchorXUnits: 'fraction',
              anchorYUnits: 'pixels',
              src: `static/${this.typeForLayer.image.slice(0, -4) + '-selected.png'}`,
            }),
          });

          this.selectInteraction = new Select({
            style: selectStyle,
            layers: [layer], 
            multi: true,
          });

          this.map.addInteraction(this.selectInteraction)

          this.modifyEdit = new Modify({
            features: this.selectInteraction.getFeatures(),
            style: selectStyle
          })
          this.map.addInteraction(this.modifyEdit)
          this.modifyEdit.on('modifyend', this.changeCoordinatesEdit);
          this.modifyEdit.on('modifystart', this.takeCoordinates)
        }
        else if (features.features.length && features.features[0].geometry.type === 'Point' && (this.typeForLayer.image === '')) {

          this.selectInteraction = new Select({
            layers: [layer],
            multi: true,
          });

          this.modifyEdit = new Modify({
            features: this.selectInteraction.getFeatures(),
          })
          this.map.addInteraction(this.modifyEdit)
          this.modifyEdit.on('modifyend', this.changeCoordinatesEdit);
        }

        console.log(this.map.getLayers())
      });
    },

    takeCoordinates(event){
      this.editedPointCoordinates = toLonLat(event.features.getArray()[0].getGeometry().getCoordinates())
      this.editedPointCoordinates[0] = parseFloat(this.editedPointCoordinates[0].toFixed(6))
      this.editedPointCoordinates[1] = parseFloat(this.editedPointCoordinates[1].toFixed(6))
    }, 
  },
  mounted() {
    this.map = new Map({
      target: 'map_content',
      layers: [
        new TileLayer({
          source: new OSM()
        }),
      ],
      view: new View({
        zoom: 13,
        center: fromLonLat([56.177483, 54.924307]),
        constrainResolution: true,
      })
    });

    this.addNewLayers();

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