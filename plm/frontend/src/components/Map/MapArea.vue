<template>
  <div id="map_content" style="position: absolute; top: 0; bottom: 0; right: 0; left: 0;"></div>
</template>

<script>
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
import { Icon, Style } from 'ol/style';
import Select from 'ol/interaction/Select';
import { Canvg } from 'canvg';

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
      canvas: document.getElementById('png_icon_of_type'),
      svg: document.querySelector('#svg_icon_of_type svg'),
    }
  },
  watch: {
    allFeatures: {
      async handler() {
        this.features = {
          type: 'FeatureCollection',
          features: this.allFeatures,
        }

        if (this.map != null) {
          await this.deleteOldLayers();
          this.addNewLayers();
        }
      }
    },
    arrayEditMode: {
      handler() {
        let arraysOfNewObject = this.createSubArrays();
        let arrayOfLayers = this.map.getAllLayers();

        for (let i in arraysOfNewObject) {
          const layer = arrayOfLayers.find(el => `${el.get('typeId')}` === i);
          let feature = layer.getSource().getFeatures();
          feature = this.deleteNewObjectFromMap(feature, arraysOfNewObject[i]);
          const source = new VectorSource({
            features: [...feature, ...new GeoJSON().readFeatures(
              {
                type: 'FeatureCollection',
                features: arraysOfNewObject[i]
              },
              {
                featureProjection: 'EPSG:3857'
              })],
          });
          layer.setSource(source);
        }
      },
      deep: true,
    },
    getFeature: function () {
      this.feature = this.getFeature;
    },
    oneType: {
      handler() {
        this.resetInteractions();
      }
    },
    addCardOn: {
      handler() {
        this.addCardOn_ = this.addCardOn;
        this.resetInteractions();
      },
      deep: true
    },

  },
  computed: mapGetters(['drawType', 'allType', 'typeForLayer', 'getObjectForCard', 'arrayEditMode', 'oneType', 'allTypeForMap']),
  methods: {
    ...mapMutations(['updateOneFeature', 'upadateEmptyObject', 'updateObjectForCard']),
    ...mapActions(['getOneFeature', 'getOneTypeObject', 'getAllType']),
    updateLonLat(cord) {
      this.feature.properties['Долгота'] = cord[1];
      this.feature.properties['Широта'] = cord[0];
    },
    deleteNewObjectFromMap(feature, arr) {
      feature = feature.filter(function (element) {
        return !(element != undefined && typeof element.id_ === 'string' && !arr.filter(el => el.id_ === element.id_).length);
      })
      return feature;
    },
    resetInteractions() {
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
      let item = this.arrayEditMode.put.find(el => el.id === id);

      if (item === undefined) {
        item = this.arrayEditMode.delete.find(el => el.id === id);
      }
      if (item === undefined) {
        item = this.arrayEditMode.post.find(el => el.id_ === id)
      }

      if (item === undefined) {
        return false;
      }
      return item;
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
      this.feature.geometry.coordinates = toLonLat(event.features.getArray()[0].getGeometry().getCoordinates());
    },
    createSubArrays() {
      let subArrays = {};
      for (let i in this.allType) {
        subArrays[`${this.allType[i].id}`] = [];
        for (let j in this.arrayEditMode.post) {
          if (this.arrayEditMode.post[j].name == this.allType[i].id) {
            let obj = JSON.parse(JSON.stringify(this.arrayEditMode.post[j]));
            obj.id = obj.id_;
            subArrays[`${this.allType[i].id}`].push(obj);
          }
        }
      }
      return subArrays;
    },
    async addInteraction() {
      this.map.removeInteraction(this.modify);
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
            src:  document.getElementById('png_icon_of_one_type').toDataURL('image/png')
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
    deleteOldLayers() {
      let arrayOfLayers = this.map.getAllLayers();
      arrayOfLayers.forEach(element => {
        if (element.get('typeId') !== undefined) {
          this.map.removeLayer(element);
        }
      })
    },
    updataDomElements() {
      this.canvas = document.getElementById('png_icon_of_type');
      this.svg = document.querySelector('#svg_icon_of_type svg');
    },
    addNewLayers() {
      this.allTypeForMap.forEach(async element => {
        let features = {
          type: 'FeatureCollection',
          features: this.features.features.filter(el => el.name === element.id),
        };

        let layer = new VectorLayer({
          source: new VectorSource({
            features: new GeoJSON().readFeatures(features,
              {
                featureProjection: 'EPSG:3857'
              }),
          }),
        });
        layer.set('typeId', element.id);
        this.map.addLayer(layer);
        await this.getOneTypeObject({ id: element.id, forFeature: true });

        if (this.typeForLayer.type === 'Point' && !(this.typeForLayer.image === '')) {
          this.updataDomElements()

          this.canvas.height = 24;
          this.canvas.width = 24;

          let v = await Canvg.from(this.canvas.getContext('2d'), this.svg.parentNode.innerHTML.trim());
          v.start();
          v.stop();
          let blackIcon = this.canvas.toDataURL('image/png');

          this.canvas.getContext("2d").fillStyle = window.getComputedStyle(this.svg, null).getPropertyValue('color');
          v = await Canvg.from(this.canvas.getContext('2d'), this.svg.parentNode.innerHTML.trim());
          v.start();
          v.stop();
          let redIcon = this.canvas.toDataURL('image/png');

          let style = new Style({
            image: new Icon({
              anchor: [0.5, 0, 5],
              anchorXUnits: 'fraction',
              anchorYUnits: 'pixels',
              src: blackIcon,
            }),
          });
          layer.setStyle(style)

          let selectStyle = new Style({
            image: new Icon({
              anchor: [0.5, 0.5],
              anchorXUnits: 'fraction',
              anchorYUnits: 'pixels',
              src: redIcon,
            }),
          });

          this.selectInteraction = new Select({
            style: selectStyle,
            layers: [layer]
          });
          this.map.addInteraction(this.selectInteraction)

          if (features.features.length && features.features[0].geometry.type === 'Point' && !(this.typeForLayer.image === '')) {
            this.modifyEdit = new Modify({
              features: this.selectInteraction.getFeatures(),
              style: selectStyle
            })
            this.map.addInteraction(this.modifyEdit)

            this.modifyEdit.on('modifyend', this.changeCoordinatesEdit);
          } else {
            this.modifyEdit = new Modify({
              features: this.selectInteraction.getFeatures(),
            })
            this.map.addInteraction(this.modifyEdit)
            this.modifyEdit.on('modifyend', this.changeCoordinatesEdit);
          }
        }
      });
    },
  },
  async mounted() {
    await this.getAllType();
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