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
            :value="el"
            :label="user.is_superuser || user.groups.length > 1 ? el.name + ' (' + el.group + ')' : el.name">
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
import { Icon, Style, Fill, Stroke } from 'ol/style';
//import Circle from 'ol/geom/Circle';
import Select from 'ol/interaction/Select';
import { Canvg } from 'canvg';
import { toStringXY } from 'ol/coordinate';
import Feature from 'ol/Feature';

export default {
  components: {
  },
  props: ['allFeatures', 'visableCard', 'addCardOn', 'infoCardOn', 'notVisableCard', 'editCardOn', 'getFeature', 'changeElements', 'cardVisable'],
  data() {
    return {
      coord: [],
      features: {
        type: 'FeatureCollection',
        features: this.allFeatures,
      },
      feature: this.getFeature,
      map: null,
      drawLayer: new VectorLayer({
        source: new VectorSource()
      }),
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
      pointCoordInLine: null,
      pointCoordInLineIndex: null,
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
          await this.addNewLayers();
          this.map.removeInteraction(this.selectInteraction);

          this.selectInteraction = new Select({
            style: this.getStyleFromSelect,
            layers: this.map.getAllLayers(),
          });

          this.map.addInteraction(this.selectInteraction);
          this.addChangedObjectOnMap();
        }
      }
    },
    arrayEdit: {
      handler() {
        this.addChangedObjectOnMap();
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
        if (this.newData.find(el => el.id === this.objectForCard.id) || this.conflictArrays.find(el => el.find(element => element.id_ === undefined ? element.id === this.objectForCard.id : element.id_ === this.objectForCard.id_))) {
          this.map.getInteractions().getArray().forEach(element => {

            if (element instanceof Modify) {
              element.setActive(true);
            }
          });
        }
        else {
          this.map.getInteractions().getArray().forEach(element => {

            if (element instanceof Modify) {
              element.setActive(this.editCardOn_.data);
            }
          });
        }
      }
    },
    'getObjectForCard.geometry': {
      handler() {
        const layer = this.map.getAllLayers().find(layer => layer.get('typeId') === this.getObjectForCard.name);
        let features = layer.getSource().getFeatures();

        for (let i in features) {
          if (features[i].getId() === this.oldFeature.id) {
            features[i].getGeometry().setCoordinates(this.coordinatesFromLonLat(this.oldFeature.geometry.coordinates));
          }
        }
      },
    },
    changeElements: {
      handler() {
        const arrayIdLayer = [...new Set(this.changeElements.map(el => el.name))];
        arrayIdLayer.forEach(async el => {
          await this.filterForFeatureForMap(el);
          const layer = this.map.getAllLayers().find(element => {
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
        this.selectInteraction.setActive(!this.addCardOn.data);
        if (!this.addCardOn_.data) {
          const checkFeature = this.map.getFeaturesAtPixel(this.map.getPixelFromCoordinate(fromLonLat(this.emptyObject.geometry.coordinates)))
          if (checkFeature.length && checkFeature[0].getGeometry().getType() === 'LineString') {
            let havePostPoint = this.arrayEdit.post.some((el) => {
              return this.checkEqualCoordinates(el.geometry.coordinates, this.emptyObject.geometry.coordinates)
            })

            if (!havePostPoint) {
              this.arrayEdit.put.forEach(async element => {
                if (element.geometry.type === 'LineString') {
                  this.comparePointLine(this.emptyObject.geometry.coordinates, element.geometry.coordinates)
                  element.geometry.coordinates.splice(this.pointCoordInLineIndex, 1)
                  this.updateArrayEditMode({ item: element, type: 'put' });
                  let newCoord = element.geometry.coordinates
                  newCoord.forEach((el, i) => {
                    newCoord[i] = fromLonLat(el)
                  });
                  checkFeature[0].getGeometry().setCoordinates(newCoord)
                  newCoord.forEach((el, i) => {
                    newCoord[i] = toLonLat(el)
                  });

                  await this.getOneFeatureId(element.id)

                  if (JSON.stringify(this.oneFeature) === JSON.stringify(element)) {
                    let checkLine = this.oneFeature.geometry.coordinates.every((el, index) => {
                      return this.checkEqualCoordinates(el, element.geometry.coordinates[index])
                    })
                    if (checkLine) {
                      this.deleteObjectFromArrayEditMode(this.oneFeature)
                    }
                  }

                }
              });
            }
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
        this.editCardOn_ = this.editCardOn;
        this.map.getInteractions().getArray().forEach(element => {
          if (element instanceof Modify) {
            element.setActive(this.editCardOn_.data)
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
          this.selectInteraction.getFeatures().clear();
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
  },
  computed:{ 
    ...mapGetters(['drawType', 'oneFeature', 'offPointsFlag', 'allType', 'typeForLayer', 'getObjectForCard', 'arrayEdit', 'oneType', 'allTypeForMap', 'featureForMap', 'featureInMap', 'newData', 'emptyObject', 'user', 'conflictArrays']),
},
  methods: {
    ...mapMutations(['updateOneFeature', 'upadateEmptyObject', 'updateObjectForCard', 'updateArrayEditMode', 'deleteObjectFromArrayEditMode']),
    ...mapActions(['getOneFeature', 'getOneFeatureId', 'setOffPointsFlag', 'getOneTypeObject', 'getAllType', 'getOneObject', 'filterForFeatureForMap', 'getFeatureForMap']),
    addChangedObjectOnMap() {
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
    checkEqualCoordinates(coord1, coord2) {
      if (coord1[0] === coord2[0] && coord1[1] === coord2[1]) {
        return true
      } else {
        return false
      }
    },

    comparePointLine(coordPoint, coordLine) {
      coordLine.forEach((element, index) => {
        if (this.checkEqualCoordinates(coordPoint, element)) {
          if (index != coordLine.length && index != 0) {
            this.pointCoordInLine = coordPoint
            this.pointCoordInLineIndex = index
          }
        }
      });
    },
    returnCoordinateForPoint(id, typeId, coordinates) {
      const layer = this.map.getAllLayers().find(el => el.get('typeId') === typeId);
      const features = layer.getSource().getFeatures();
      let feature = features.find(el => { return el.getId() === id });

      const oldCoordinates = feature.getGeometry().getCoordinates();
      const newCoordinates = this.coordinatesFromLonLat(coordinates);
      feature.getGeometry().setCoordinates(newCoordinates);
      if (layer.get('type') === 'Point') {
        this.returnCoordinateForLineString(oldCoordinates, newCoordinates);
      }

    },
    returnCoordinateForLineString(oldCoordinates, newCoordinates) {
      if (!this.offPointsFlag) {
        const geom = this.map.getFeaturesAtPixel(this.map.getPixelFromCoordinate(oldCoordinates), {
          filterLayer: el => el.get('type') === 'LineString',
        });
        geom.forEach((element) => {
          if (element.getGeometry().getType() === 'LineString') {
            element.getGeometry().getCoordinates().forEach(async (coord, index) => {
              if (toStringXY(coord, 7) === toStringXY(oldCoordinates, 7)) {
                let lineStingCooradinates = element.getGeometry().getCoordinates();
                lineStingCooradinates[index] = newCoordinates;
                element.getGeometry().setCoordinates(lineStingCooradinates);

                if (Number.isInteger(element.getId())) {
                  await this.getOneFeatureId(element.getId())
                  this.arrayEdit.put.forEach(putElement => {
                    if (putElement.id === element.getId()) {
                      lineStingCooradinates.forEach((element, index) => {
                        lineStingCooradinates[index] = toLonLat(element)
                      });
                      putElement.geometry.coordinates = lineStingCooradinates
                    }
                  });

                }

                if (typeof element.getId() === 'string') {
                  this.changeNewLineString(element.getId(), element.getGeometry().getCoordinates());
                }
              }
            });
          }
        })
      }

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
    coordinatesToLonLat(coordinates) {
      if (typeof coordinates[0] === 'object') {
        for (let i in coordinates) {
          if (typeof coordinates[i][0] === 'object') {
            for (let j in coordinates[i]) {
              coordinates[i][j] = toLonLat(coordinates[i][j]);
            }
          }
          else {
            coordinates[i] = toLonLat(coordinates[i]);
          }
        }
      }
      else {
        coordinates = toLonLat(coordinates);
      }
      return coordinates;
    },
    coordinatesFromLonLat(coordinates) {
      if (typeof coordinates[0] === 'object') {
        for (let i in coordinates) {
          if (typeof coordinates[i][0] === 'object') {
            for (let j in coordinates[i]) {
              coordinates[i][j] = fromLonLat(coordinates[i][j]);
            }
          }
          else {
            coordinates[i] = fromLonLat(coordinates[i]);
          }
        }
      }
      else {
        coordinates = fromLonLat(coordinates);
      }
      return coordinates;
    },
    updateCoordinates() {
      if (this.drawLayer.getSource().getFeatures().length === 1 || (this.arrFeatureForDraw.length && this.drawLayer.getSource().getFeatures().length === this.arrFeatureForDraw.length + 1)) {
        this.map.removeInteraction(this.draw);
        let coordinates;

        if (this.drawLayer.getSource().getFeatures().length === 1) {
          coordinates = this.drawLayer.getSource().getFeatures()[0].getGeometry().getCoordinates();
        }
        else {
          coordinates = this.drawLayer.getSource().getFeatures().find(el => el.getGeometry().getType() === 'LineString').getGeometry().getCoordinates();
        }

        this.feature.geometry.coordinates = this.coordinatesToLonLat(coordinates);
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
      this.updateCoordinates();
      const feature_ = this.map.getFeaturesAtPixel(event.pixel)[0];

      if (feature_ && !this.addCardOn_.data && (feature_.getId() != this.objectForCard.id || !this.cardVisable.data)) {
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
      else if (!feature_ && !this.addCardOn_.data) {
        this.notVisableCard();
        setTimeout(() => {
          this.infoCardOn_.data = false;
          this.editCardOn_.data = false;
        }, 500)
      }
    },
    changeCoordinates(event) {
      const coordinates = event.features.getArray()[0].getGeometry().getCoordinates();
      if (this.addCardOn_.data) {
        this.feature.geometry.coordinates = this.coordinatesToLonLat(coordinates);
      }
      else {
        this.returnCoordinateForLineString(this.editedPointCoordinates, coordinates)
        this.objectForCard.geometry.coordinates = this.coordinatesToLonLat(coordinates);
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

        const layer = this.map.getAllLayers().find(el => el.get('typeId') === this.oneType.id);
        this.drawLayer.set('standartIcon', layer.get('standartIcon'));
        this.drawLayer.setStyle(this.getStyleFromLayer);

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
        const snap = new Snap({ source: source });
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
          type: this.drawType,
          style: this.drawLayer.getStyle(),
          source: this.drawLayer.getSource()
        });
      }
      this.map.addLayer(this.drawLayer);
      this.map.addInteraction(this.draw);
      this.map.addInteraction(this.modify);
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
    async addNewLayers() {
      for (let i in this.allTypeForMap) {
        let element = this.allTypeForMap[i];
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

        await this.getOneTypeObject({ id: element.id, forFeature: true });
        layer.set('typeId', this.typeForLayer.id);
        layer.set('type', this.typeForLayer.type);
        layer.set('group', this.typeForLayer.group);

        if (this.typeForLayer.type === 'Point') {
          layer.setZIndex(Infinity)
        } else if (layer.getSource().getFeatures().length && layer.getSource().getFeatures()[0].getGeometry().getType() === 'LineString') {
          layer.setZIndex(2)
        } else if (layer.getSource().getFeatures().length && layer.getSource().getFeatures()[0].getGeometry().getType() === 'Polygon') {
          layer.setZIndex(0)
        }

        this.map.addLayer(layer);
        this.canvas.height = 25;
        this.canvas.width = 25;
        this.addModify(layer);
      }
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
    getStyleFromLayer(feature) {
      const type = feature.getGeometry().getType();
      if (type === 'Point') {
        let layer = feature.getLayer(this.map);
        layer = layer ? layer : this.map.getAllLayers().find(el => el.get('typeId') === this.oneType.id);
        const conflictObject = this.conflictArrays.find(el => el.find(element => element.id === feature.getId())) || this.newData.find(el => el.id === feature.getId());
        return new Style({
          image: new Icon({
            anchor: [0.5, 0, 5],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: conflictObject ? layer.get('conflictIcon') : layer.get('standartIcon'),
          }),
          zIndex: Infinity,
        });
      }
      else if (type === 'LineString') {
        return new Style({
          stroke: new Stroke({ color: "blue", width: 2 }),
          zIndex: 2,
        });
      }
      else {
        return new Style({
          stroke: new Stroke({
            color: 'blue',
            width: 3,
          }),
          fill: new Fill({
            color: 'rgba(0, 0, 255, 0.1)',
          }),
          zIndex: 0,
        });
      }
    },
    getStyleFromSelect(feature) {
      const type = feature.getGeometry().getType();
      if (type === 'Point') {
        const layer = feature.getLayer(this.map);
        return new Style({
          image: new Icon({
            anchor: [0.5, 0, 5],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: layer.get('selectIcon'),
          }),
          zIndex: Infinity,
        });
      }
      else if (type === 'LineString') {
        return new Style({
          stroke: new Stroke({ color: "red", width: 2 }),
        });
      }
      else {
        return new Style({
          stroke: new Stroke({
            color: 'red',
            width: 3,
          }),
          fill: new Fill({
            color: 'rgba(255, 0, 0, 0.1)',
          }),
        });
      }
    },
    async addModify(layer) {
      if (this.typeForLayer.type === 'Point' && !(this.typeForLayer.image === '')) {
        this.updataDomElements();

        await this.svgToSpan();
        const blackIcon = this.canvas.toDataURL('image/png');

        this.canvas.getContext("2d").fillStyle = window.getComputedStyle(this.svg, null).getPropertyValue('color');
        await this.svgToSpan();
        const redIcon = this.canvas.toDataURL('image/png');

        this.canvas.getContext("2d").fillStyle = '#27258B';
        await this.svgToSpan();
        const blueIcon = this.canvas.toDataURL('image/png');

        layer.set('standartIcon', blackIcon);
        layer.set('selectIcon', redIcon);
        layer.set('conflictIcon', blueIcon);
      }
      layer.setStyle(this.getStyleFromLayer);
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
    
    Feature.prototype.getLayer = function (map) {
      var this_ = this, layer_, layersToLookFor = [];

      var check = function (layer) {
        var source = layer.getSource();
        if (source instanceof VectorSource) {
          var features = source.getFeatures();
          if (features.length > 0) {
            layersToLookFor.push({
              layer: layer,
              features: features
            });
          }
        }
      };
      map.getLayers().forEach(function (layer) {
        check(layer);
      });
      layersToLookFor.forEach(function (obj) {
        var found = obj.features.some(function (feature) {
          return this_ === feature;
        });
        if (found) {
          layer_ = obj.layer;
        }
      });
      return layer_;
    };

    this.selectInteraction = new Select();

    await this.addNewLayers();

    this.map.on('click', this.getFeature_);
    if (this.addCardOn_.data) {
      this.addInteraction();
    }

    this.selectInteraction = new Select({
      style: this.getStyleFromSelect,
      layers: this.map.getAllLayers(),
    });
    this.modifyEdit = new Modify({
      //style: this.getStyleFromSelect,
      features: this.selectInteraction.getFeatures(),
    })
    this.modifyEdit.on('modifystart', this.takeCoordinates);
    this.modifyEdit.on('modifyend', this.changeCoordinates);
    this.modifyEdit.setActive(false);
    
    this.map.addInteraction(this.modifyEdit);
    this.map.addInteraction(this.selectInteraction);

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