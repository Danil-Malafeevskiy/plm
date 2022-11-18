<template>
  <div id="map_content" style="position: absolute; top: 0; bottom: 0; right: 0; left: 0;">
    <v-btn icon style="position: absolute; z-index: 1; right: 0" @click="isFilter = !isFilter">
      <v-icon color="#A5A5A6">
        mdi-filter
      </v-icon>
    </v-btn>
    <v-scroll-x-reverse-transition>
      <v-card v-if="isFilter" style="position: absolute; z-index: 2; right: 0; margin: 16px 24px 16px 0px" width="310"
        height="400">
        <v-btn text style="position: absolute; z-index: 1; right: 0" @click="isFilter = !isFilter">
          <v-icon color="#A5A5A6">
            mdi-close
          </v-icon>
        </v-btn>
        <p style="font-weight: 500; margin: 25px 0 0 24px">Типы объектов</p>
        <div style="margin: 15px 0 0 24px; overflow-y: scroll; max-height: 70%;">
          <v-checkbox v-model="allTypesSelected" class="ma-2" color="#E93030" label="все"></v-checkbox>

          <v-checkbox v-for="(el) in allType" :key="el.id" v-model="filteredTypes" class="ma-2" color="#E93030"
            :value="el" :label="el.name">
          </v-checkbox>
        </div>
        <v-divider style="position: absolute; bottom: 60px; width: 100%;"></v-divider>
        <div
          style="display: flex; justify-content: flex-end; align-items: center; position: absolute; bottom: 0; right: 0;">
          <v-btn class="mt-2" color="#787878" text @click="closeFilter">
            отмена
          </v-btn>
          <v-btn class="mt-2" color="#787878" text @click="filteredLayer">
            примеить
          </v-btn>
        </div>
      </v-card>

    </v-scroll-x-reverse-transition>
  </div>
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
import { Draw, Modify, Snap } from 'ol/interaction';
import { mapMutations, mapActions, mapGetters } from 'vuex';
import 'ol/ol.css';
import { Icon, Style } from 'ol/style';
import Circle from 'ol/geom/Circle';
import Select from 'ol/interaction/Select';
import { Canvg } from 'canvg';
import Stroke from 'ol/style/Stroke';
import Fill from 'ol/style/Fill';
import { toStringXY } from 'ol/coordinate';
export default {
  components: {
  },
  props: ['allFeatures', 'visableCard', 'addCardOn', 'infoCardOn', 'notVisableCard', 'editCardOn', 'getFeature', 'changeElements', 'cardVisable'],
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
      draw: null,
      modify: null,
      modifyEdit: null,
      addCardOn_: this.addCardOn,
      infoCardOn_: this.infoCardOn,
      editCardOn_: this.editCardOn,
      selectInteraction: null,
      objectForCard: {},
      canvas: document.getElementById('png_icon_of_type'),
      svg: document.querySelector('#svg_icon_of_type svg'),
      editedPointCoordinates: null,
      counter: 0,
      oldFeature: null,
      arrFeatureForDraw: [],
      isFilter: false,
      filteredTypes: this.allType,
      deletedLayers: [],
      allTypesSelected: true,
      oldDrawCoordinates: null,
      indexDraw: null,
      drawCoord: null,
      drawFeature: null,
      oneFeature_: this.oneFeature,
      arrayEdit_: this.arrayEdit,
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
    arrayEdit: {
      async handler() {
        this.arrayEdit_ = this.arrayEdit
        let arraysOfNewObject = this.createSubArrays();
        let arrayOfLayers = this.map.getAllLayers();
        for (let i in arraysOfNewObject) {
          const layer = arrayOfLayers.find((el) => { return `${el.get('typeId')}` === i });
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
    getObjectForCard: {
      handler() {
        if (this.editCardOn.data) {
          this.oldFeature = this.objectForCard;
        }
        else {
          this.oldFeature = this.getObjectForCard;
        }
        this.objectForCard = this.getObjectForCard;
        if (this.editCardOn_.data && 'geometry' in this.getObjectForCard) {
          if (this.oldFeature.id !== this.getObjectForCard.id || this.oldFeature.id_ !== this.getObjectForCard.id_) {
            this.editCardOn_.data = false;
          }
          else {
            this.returnCoordinateForPoint('id_' in this.objectForCard ? this.objectForCard.id_ : this.objectForCard.id,
              this.objectForCard.name, this.objectForCard.geometry.coordinates);
          }
        }
        if ('name' in this.objectForCard && typeof this.objectForCard.name === 'number') {
          this.map.getAllLayers().filter(el => el.get('typeId') === this.objectForCard.name).forEach(el => {
            el.getSource().getFeatures().forEach(element => {
              if (element.getId() === this.getObjectForCard.id) {
                let interaction = this.map.getInteractions().getArray().filter(this.clearFeaturesInInteractionAndFindInteraction);
                if (interaction.length && (interaction[0].getFeatures().getArray().length && interaction[0].getFeatures().getArray()[0].getId() != this.objectForCard.id) || !(interaction[0].getFeatures().getArray().length)) {
                  interaction[0].getFeatures().push(element);
                }
              }
            })
          })
        }
      }
    },
    changeElements: {
      handler() {
        const arrayIdLayer = [...new Set(this.changeElements.map(el => el.name))];
        arrayIdLayer.forEach(async el => {
          await this.filterForFeatureForMap(el);
          const layer = this.map.getAllLayers().find(element => {
            console.log(element.get('typeId'), el);
            return element.get('typeId') === el && element.get('typeId') != undefined;
          });
          const source = new VectorSource({
            features: new GeoJSON().readFeatures(
              {
                type: 'FeatureCollection',
                features: this.featureForMap
              },
              {
                featureProjection: 'EPSG:3857'
              }),
          });
          layer.setSource(source);
        })
      },
      deep: true,
    },
    getFeature: function () {
      this.feature = this.getFeature;
    },
    drawType: {
      handler() {
        if (this.map) {
          this.resetInteractions();
        }
      }
    },
    addCardOn: {
      handler() {
        this.addCardOn_ = this.addCardOn;
        if (!this.addCardOn_.data) {
          console.log(this.emptyObject)
          const checkFeature = this.map.getFeaturesAtPixel(this.map.getPixelFromCoordinate(fromLonLat(this.emptyObject.geometry.coordinates)))
          if (checkFeature.length && checkFeature[0].getGeometry().getType() === 'LineString'){
            console.log(this.emptyObject)
            console.log(checkFeature[0].getGeometry().getType())
            console.log(this.arrayEdit_)
          }
        }
        if (this.map) {
          this.resetInteractions();
        }
      },
      deep: true
    },
    editCardOn: {
      async handler() {
        this.editCardOn_ = this.editCardOn
        this.map.getInteractions().getArray().forEach(element => {
          if (element instanceof Modify) {
            element.setActive(!element.getActive())
          }
        });
        if (!this.editCardOn.data && !this.infoCardOn.data) {
          await this.returnCoordinates();
        }
      },
      deep: true
    },
    cardVisable: {
      handler() {
        if (!this.cardVisable.data) {
          this.map.getInteractions().getArray().filter(el => el.get('typeId') !== undefined).forEach(element => element.getFeatures().clear())
        }
      },
      deep: true,
    },
    allType: {
      handler() {
        this.filteredTypes = this.allType.map(el => el);
      }
    },
    allTypesSelected: {
      handler() {
        if (this.allTypesSelected) {
          this.filteredTypes = this.allType;
        }
        else {
          this.filteredTypes = [];
        }
      }
    },
    getOneFeatureId: {
      handler() {
        this.oneFeature_ = this.oneFeature
      }
    }
  },
  computed: mapGetters(['drawType', 'oneFeature', 'allType', 'typeForLayer', 'getObjectForCard', 'arrayEdit', 'oneType', 'allTypeForMap', 'featureForMap', 'featureInMap', 'newData', 'emptyObject']),
  methods: {
    ...mapMutations(['updateOneFeature', 'upadateEmptyObject', 'updateObjectForCard', 'updateArrayEditMode']),
    ...mapActions(['getOneFeature', 'getOneFeatureId', 'getOneTypeObject', 'getAllType', 'getOneObject', 'filterForFeatureForMap', 'getFeatureForMap']),
    updateLonLat(cord) {
      this.feature.properties['Долгота'] = cord[1];
      this.feature.properties['Широта'] = cord[0];
    },
    async returnCoordinates() {
      let object;
      if ('id_' in this.oldFeature) {
        object = JSON.parse(JSON.stringify(this.arrayEdit.post.find(el => el.id_ === this.oldFeature.id_)));
        object.id = object.id_;
      }
      else {
        object = this.arrayEdit.put.find(el => el.id === this.oldFeature.id);
        object = object === null ? this.arrayEdit.delete.find(el => el.id === this.oldFeature.id) : object;
      }
      if (!object) {
        await this.getFeatureForMap(this.oldFeature.id)
        object = this.featureInMap;
      }
      this.returnCoordinateForPoint('id_' in object ? object.id_ : object.id, object.name, object.geometry.coordinates)
      if (this.oldFeature !== this.objectForCard) {
        this.oldFeature = this.objectForCard;
      }
    },
    returnCoordinateForPoint(id, typeId, coordinates) {
      const layer = this.map.getAllLayers().find(el => el.get('typeId') === typeId);
      const features = layer.getSource().getFeatures();
      let feature = features.find(el => { return el.getId() === id });
      const oldCoordinates = feature.getGeometry().getCoordinates();
      const newCoordinates = fromLonLat(coordinates);
      feature.getGeometry().setCoordinates(newCoordinates);
      this.returnCoordinateForLineString(oldCoordinates, newCoordinates);
    },
    returnCoordinateForLineString(oldCoordinates, newCoordinates) {
      const geom = this.map.getFeaturesAtPixel(this.map.getPixelFromCoordinate(oldCoordinates), {
        filterLayer: el => el.get('type') === 'LineString',
      });
      geom.forEach((element) => {
        element.getGeometry().getCoordinates().forEach((coord, index) => {
          if (toStringXY(coord, 7) === toStringXY(oldCoordinates, 7)) {
            let lineStingCooradinates = element.getGeometry().getCoordinates();
            lineStingCooradinates[index] = newCoordinates;
            element.getGeometry().setCoordinates(lineStingCooradinates);
            if (typeof element.getId() === 'string') {
              this.changeNewLineString(element.getId(), element.getGeometry().getCoordinates());
            }
          }
        });
      })
    },
    clearFeaturesInInteractionAndFindInteraction(el) {
      if (el.get('typeId') != undefined && el.getFeatures().getArray().length && el.getFeatures().getArray()[0].getId() != this.objectForCard.id) {
        el.getFeatures().clear();
      }
      return el.get('typeId') === this.getObjectForCard.name
    },
    deleteNewObjectFromMap(feature, arr) {
      feature = feature.filter(function (element) {
        return !(element != undefined && typeof element.id_ === 'string' && !arr.filter(el => el.id_ === element.id_).length);
      })
      return feature;
    },
    resetInteractions() {
      this.map.removeInteraction(this.draw);
      this.map.removeLayer(this.drawLayer);
      this.drawLayer.getSource().refresh();
      if (this.addCardOn.data) {
        this.addInteraction();
      }
      else {
        this.map.removeInteraction(this.modify);
      }
    },
    changeNewLineString(id, coordinates) {
      let lineSting = this.arrayEdit.post.find(el => id === el.id_);
      for (let i in coordinates) {
        coordinates[i] = toLonLat(coordinates[i]);
      }
      lineSting.geometry.coordinates = coordinates;
      this.updateArrayEditMode({ item: lineSting, type: 'put' });
    },
    updateCoordinates() {
      if (this.drawLayer.getSource().getFeatures().length === 1 || (this.arrFeatureForDraw.length && this.drawLayer.getSource().getFeatures().length === this.arrFeatureForDraw.length + 1)) {
        this.map.removeInteraction(this.draw);
        if (this.drawLayer.getSource().getFeatures().length === 1) {
          this.coord = this.drawLayer.getSource().getFeatures()[0].getGeometry().getCoordinates();
        }
        else {
          this.coord = this.drawLayer.getSource().getFeatures().find(el => el.getGeometry().getType() === 'LineString').getGeometry().getCoordinates();
        }
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
        }
        this.feature.geometry.coordinates = this.coord;
        this.feature.type = 'Feature';
        this.feature.geometry.type = this.drawType;
      }
    },
    findItem(id) {
      let item = this.arrayEdit.put.find(el => el.id === id);
      if (item === undefined) {
        item = this.arrayEdit.delete.find(el => el.id === id);
      }
      if (item === undefined) {
        item = this.arrayEdit.post.find(el => el.id_ === id)
      }
      if (item === undefined) {
        return false;
      }
      return item;
    },
    async getFeature_(event) {
      const feature_ = this.map.getFeaturesAtPixel(event.pixel)[0];
      if (feature_ && !this.addCardOn_.data) {
        let item = this.findItem(feature_.id_)
        if (item) {
          this.updateObjectForCard(JSON.parse(JSON.stringify(item)));
        }
        else {
          await this.getOneFeature(feature_.id_);
        }
        setTimeout(() => {
          const interacion = this.map.getInteractions().getArray().find(el => el.get('typeId') === this.objectForCard.name);
          if (interacion && !interacion.getFeatures().getArray().length) {
            interacion.getFeatures().push(feature_);
          }
        }, 100);
        this.infoCardOn_.data = true;
        this.visableCard();
      }
      else if (!this.addCardOn_.data) {
        this.notVisableCard();
        setTimeout(() => {
          this.infoCardOn_.data = false;
          this.editCardOn_.data = false;
        }, 500)
      }
      else {
        this.updateCoordinates();
      }
    },
    changeCoordinates(event) {
      if (this.addCardOn_.data) {
        this.feature.geometry.coordinates = toLonLat(event.features.getArray()[0].getGeometry().getCoordinates());
      }
      else {
        this.returnCoordinateForLineString(this.editedPointCoordinates, event.features.getArray()[0].getGeometry().getCoordinates())
        this.objectForCard.geometry.coordinates = toLonLat(event.features.getArray()[0].getGeometry().getCoordinates())
      }
    },
    createSubArrays() {
      let subArrays = {};
      for (let i in this.allType) {
        subArrays[`${this.allType[i].id}`] = [];
        for (let j in this.arrayEdit.post) {
          if (this.arrayEdit.post[j].name == this.allType[i].id) {
            let obj = JSON.parse(JSON.stringify(this.arrayEdit.post[j]));
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
      if (this.drawType === 'Point') {
        await this.getOneTypeObject({ id: this.oneType.id, forFeature: true });
        this.drawLayer = new VectorLayer({
          source: new VectorSource({
            features: []
          }),
        });
        if (this.drawType === 'Point') {
          const interaction = this.map.getInteractions().getArray().find(el => el.get('typeId') === this.oneType.id);
          this.drawLayer.setStyle(interaction.get('style'));
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
        this.draw.on('drawstart', this.checkDrawCoordinates)
        this.arrFeatureForDraw = []
        const layerOfLineString = this.map.getAllLayers().filter(el => el.get('type') === 'LineString')
        for (let i in layerOfLineString) {
          this.arrFeatureForDraw = [...this.arrFeatureForDraw, ...layerOfLineString[i].getSource().getFeatures()];
        }
        const source = new VectorSource({ features: this.arrFeatureForDraw });
        const snap = new Snap({ source: source });
        this.map.addLayer(this.drawLayer);
        this.map.addInteraction(this.draw);
        this.map.addInteraction(this.modify);
        this.map.addInteraction(snap);
      }
      else if (this.drawType === 'LineString') {
        this.arrFeatureForDraw = [];
        const layerOfPoint = this.map.getAllLayers().filter(el => el.get('type') === 'Point' && el.get('group') === this.oneType.group);
        for (let i in layerOfPoint) {
          this.arrFeatureForDraw = [...this.arrFeatureForDraw, ...layerOfPoint[i].getSource().getFeatures()];
        }
        const source = new VectorSource({ features: this.arrFeatureForDraw });
        this.drawLayer = new VectorLayer({
          source: source
        });
        this.draw = new Draw({
          source: source,
          type: this.drawType,
        });
        this.modify = new Modify({
          source: this.drawLayer.getSource(),
          style: this.drawLayer.getStyle()
        });
        this.modifyEdit.on('modifystart', this.takeCoordinates);
        this.modifyEdit.on('modifyend', this.changeCoordinates);
        const snap = new Snap({ source: source });
        this.map.addLayer(this.drawLayer);
        this.map.addInteraction(this.modify);
        this.map.addInteraction(this.draw);
        this.map.addInteraction(snap);
      }
      else {
        this.drawLayer = new VectorLayer({
          source: new VectorSource({
            features: []
          }),
        });
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
      }
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
      this.map.getAllLayers().filter(el => el.get('typeId') !== undefined).forEach(element => {
        this.map.removeLayer(element);
      });
      this.map.getInteractions().getArray().filter(el => el.get('typeId') !== undefined).forEach(element => {
        this.map.removeInteraction(element);
      });
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
        if (layer.getSource().getFeatures().length && layer.getSource().getFeatures()[0].getGeometry().getType() === 'Point') {
          layer.setZIndex(Infinity)
        } else if (layer.getSource().getFeatures().length && layer.getSource().getFeatures()[0].getGeometry().getType() === 'LineString') {
          layer.setZIndex(2)
        } else if (layer.getSource().getFeatures().length && layer.getSource().getFeatures()[0].getGeometry().getType() === 'Polygon') {
          layer.setZIndex(0)
        }
        await this.getOneTypeObject({ id: element.id, forFeature: true });
        layer.set('typeId', this.typeForLayer.id);
        layer.set('type', this.typeForLayer.type);
        layer.set('group', this.typeForLayer.group);
        this.map.addLayer(layer);
        this.canvas.height = 25;
        this.canvas.width = 25;
        this.addModify(layer);
      });
    },
    takeCoordinates(event) {
      this.editedPointCoordinates = event.features.getArray()[0].getGeometry().getCoordinates()
    },
    async checkDrawCoordinates(event) {
      this.drawCoord = event.feature.getGeometry().getCoordinates()
      if (this.map.getFeaturesAtPixel(this.map.getPixelFromCoordinate(this.drawCoord)).length) {
        this.drawFeature = this.map.getFeaturesAtPixel(this.map.getPixelFromCoordinate(this.drawCoord))[0]
        this.oldDrawCoordinates = this.drawFeature.getGeometry().getCoordinates()
        this.indexDraw = -1
        for (let i = 0; i < this.oldDrawCoordinates.length - 1; i++) {
          this.drawFeature.getGeometry().setCoordinates([this.drawFeature.getGeometry().getCoordinates()[i], this.drawFeature.getGeometry().getCoordinates()[i + 1]])
          let checkCoord = this.oldDrawCoordinates[i][0] === this.drawCoord[0] && this.oldDrawCoordinates[i][1] === this.drawCoord[1]
          let checkCoord1 = this.oldDrawCoordinates[i + 1][0] === this.drawCoord[0] && this.oldDrawCoordinates[i + 1][1] === this.drawCoord[1]
          if (this.drawFeature.getGeometry().intersectsCoordinate(this.drawCoord) && !(checkCoord || checkCoord1)) {
            this.indexDraw = i + 1
          }
          this.drawFeature.getGeometry().setCoordinates(this.oldDrawCoordinates)
        }
        if ((this.indexDraw != -1) && (this.indexDraw != 0) && (this.indexDraw != this.oldDrawCoordinates.length)) {
          this.oldDrawCoordinates.splice(this.indexDraw, 0, this.drawCoord)
          this.drawFeature.getGeometry().setCoordinates(this.oldDrawCoordinates)
          if (Number.isInteger(this.drawFeature.getId())) {
            for (let i = 0; i < this.oldDrawCoordinates.length; i++) {
              this.oldDrawCoordinates[i] = toLonLat(this.oldDrawCoordinates[i])
            }
            await this.getOneFeatureId(this.drawFeature.getId())
            this.oneFeature.geometry.coordinates = this.oldDrawCoordinates
            this.updateArrayEditMode({ item: this.oneFeature, type: 'put' });
          } else {
            this.changeNewLineString(this.drawFeature.getId(), this.oldDrawCoordinates)
          }
        }
      }
    },
    async svgToSpan() {
      let v = await Canvg.from(this.canvas.getContext('2d'), this.svg.parentNode.innerHTML.trim());
      v.start();
      v.stop();
    },
    async addModify(layer) {
      let selectStyle;
      if (this.typeForLayer.type === 'LineString') {
        selectStyle = new Style({
          stroke: new Stroke({ color: "red" }),
          zIndex: Infinity,
        });

      }
      else if (this.typeForLayer.type === 'Point' && !(this.typeForLayer.image === '')) {
        this.updataDomElements();
        await this.svgToSpan();
        const blackIcon = this.canvas.toDataURL('image/png');
        this.canvas.getContext("2d").fillStyle = window.getComputedStyle(this.svg, null).getPropertyValue('color');
        await this.svgToSpan();
        const redIcon = this.canvas.toDataURL('image/png');
        let style = new Style({
          image: new Icon({
            anchor: [0.5, 0, 5],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: blackIcon,
          }),
          zIndex: Infinity,
        });
        layer.setStyle(style)
        selectStyle = new Style({
          image: new Icon({
            anchor: [0.5, 0.5],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: redIcon,
          }),
          zIndex: Infinity,
        });
      }
      else if (this.typeForLayer.type === 'Point' && (this.typeForLayer.image === '')) {
        selectStyle = new Style({
          image: new Circle({
            stroke: new Stroke({ color: "red" }),
            radius: 7,
            fill: new Fill({ color: 'rgba(255,255,255,0.4)' })
          }),
          stroke: new Stroke({ color: "red" }),
          fill: new Fill({ color: 'rgba(255,255,255,0.4)' }),
          zIndex: Infinity,
        });
      }
      this.selectInteraction = new Select({
        style: selectStyle,
        layers: [layer],
      });

      this.map.addInteraction(this.selectInteraction);
      if (this.typeForLayer.type !== 'LineString') {
        this.modifyEdit = new Modify({
          features: this.selectInteraction.getFeatures(),
          style: selectStyle
        })
        this.map.addInteraction(this.modifyEdit);
        this.modifyEdit.on('modifystart', this.takeCoordinates);
        this.modifyEdit.on('modifyend', this.changeCoordinates);
        this.modifyEdit.setActive(false);
      }
      this.selectInteraction.set('typeId', this.typeForLayer.id);
      this.selectInteraction.set('style', selectStyle);
      if ((this.infoCardOn.data || this.editCardOn.data) && this.selectInteraction.get('typeId') === this.getObjectForCard.name) {
        this.map.getAllLayers().filter(el => el.get('typeId') === this.getObjectForCard.name).forEach(el => {
          el.getSource().getFeatures().forEach(element => {
            if (element.getId() === this.getObjectForCard.id) {
              this.selectInteraction.getFeatures().push(element);
            }
          });
        });
      }
    },
    filteredLayer() {
      const allLayers = this.map.getAllLayers().filter(el => el.get('typeId') != undefined);
      allLayers.forEach(layer => {
        if (!this.filteredTypes.find(el => el.id === layer.get('typeId'))) {
          this.deletedLayers.push(layer);
          this.map.removeLayer(layer);
        }
      });
      this.filteredTypes.forEach(type => {
        if (!allLayers.find(el => el.get('typeId') === type.id)) {
          this.map.addLayer(this.deletedLayers.find(el => el.get('typeId') === type.id))
        }
      })
    },
    closeFilter() {
      this.isFilter = !this.isFilter;
      const allLayers = this.map.getAllLayers().filter(el => el.get('typeId') != undefined);
      allLayers.forEach(layer => {
        if (!this.filteredTypes.find(el => el.id === layer.get('typeId'))) {
          this.filteredTypes.push(this.allType.find(el => el.id === layer.get('typeId')))
        }
      });
    }
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
        zoom: 12,
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
    this.filteredTypes = this.allType;
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