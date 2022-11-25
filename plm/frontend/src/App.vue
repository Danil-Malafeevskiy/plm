<template>
  <v-app>
    <NavigationDrawer :addCardOn="addCardOn" :notVisableVersions="notVisableVersions" :visableCard="visableCard"
      :editCardOn="editCardOn" :visableVersions="visableVersions" :versionsPage="versionsPage"
      :infoCardOn="infoCardOn" />
    <FIleInputWindow v-if="isFileInput" @offFileInput="offFileInput" />
    <v-main>
      <router-view></router-view>
      <div style="display: none">
        <canvas id="png_icon_of_type">
        </canvas>
        <v-icon id="svg_icon_of_type" color="#E93030" v-if="typeForLayer">{{ typeForLayer.image }}</v-icon>
        <canvas id="png_icon_of_one_type">
        </canvas>
        <v-icon id="svg_icon_of_one_type" color="#E93030" v-if="oneType">{{ oneType.image }}</v-icon>
      </div>

      <v-toolbar color="#F5F5F4" style="border-bottom: 1px solid #E0E0E0; box-shadow: none;" :class="{
        'features': actions === 'getFeatures'
      }">
        <v-toolbar-title><span style="font-size: 24px">{{ getToolbarTitle }}</span></v-toolbar-title>
        <template v-slot:extension>

          <v-tabs v-model="tab" align-with-title color="#E93030">
            <v-tab v-for="item in items" :key="item" class="ma-0">
              <span>{{ item }}</span>
            </v-tab>
          </v-tabs>
          <template v-if="actions === 'getFeatures'">
            <v-btn @click="editMode = true" class="pa-0" style="margin: 0 10px 0 0 !important" fab small elevation="0"
              color="#F5F5F4">
              <v-icon color="#A5A5A6">
                mdi-pencil
              </v-icon>
            </v-btn>

            <v-btn :disabled="cardVisable.data || (!editMode && actions === 'getFeatures')"
              style="border-radius: 4px; margin-right: 10px !important" class="show__card" height="28px" width="80px"
              color="#EE5E5E" @click="addCardOn.data = !addCardOn.data; visableCard();">
              <v-icon color="white !default" dark>
                mdi-plus
              </v-icon>
            </v-btn>
            <v-btn depressed class="pa-0 mr-0" small fab elevation="0" color="#F5F5F4"
              @click="isFileInput = !isFileInput">
              <v-icon color="#A5A5A6">
                mdi-file-upload
              </v-icon>
            </v-btn>
          </template>
        </template>
        <v-btn v-if="actions !== '' && actions !== 'getFeatures'"
          :disabled="cardVisable.data || (!editMode && actions === 'getFeatures')"
          style="border-radius: 4px; margin-right: 10px !important; margin-bottom: 10px;" class="show__card"
          height="28px" width="80px" color="#EE5E5E" @click="addCardOn.data = !addCardOn.data; visableCard();">
          <v-icon color="white !default" dark>
            mdi-plus
          </v-icon>
        </v-btn>
      </v-toolbar>

      <v-tabs-items v-model="tab" :style="{ height: heightVItem }">

        <CardConflict v-show="conflictCard" :cardVisable="cardVisable" :conflictCard="conflictCard" :editMode="editMode"
          :objectForConflict="objectForConflict" :notVisableCard="notVisableCard" />

        <CardInfo v-if="!conflictCard" :cardVisable="cardVisable" :addCardOn="addCardOn" :infoCardOn="infoCardOn"
          :editCardOn="editCardOn" :visableCard="visableCard" :notVisableCard="notVisableCard" :editMode="editMode" />

        <v-tab-item>

          <v-slide-y-transition>
            <div v-if="editMode && actions === 'getFeatures'" style="background-color: #FBDADA;">
              <div class="edit_line">
                <div>
                  <a @click="closeEditMode" style="margin: 5px 20px">
                    <v-icon small>mdi-close</v-icon>
                  </a>
                  <span style="color: #454545;">Редактирование</span>
                  <span style="color: #454545; margin-left: 20px; font-weight: 500;">{{ arrayEdit.put.length +
                      arrayEdit.post.length
                      +
                      arrayEdit.delete.length
                  }} объектов</span>
                </div>
                <div>
                  <v-btn @click="arrayEditMode.messege = ''" text class="pa-0" style="margin: 0 10px 0 0">
                    <span style="color: #787878;">Удалить Комментарий</span>
                  </v-btn>
                  <v-btn @click="editObjects" text class="pa-0" style="margin: 0 10px 0 0">
                    <span style="color: #787878;">применить</span>
                  </v-btn>
                </div>
              </div>
              <v-text-field v-model="arrayEditMode.messege" class="pa-2" background-color="#F1F1F1" hide-details
                label="Комментарий" append-icon="mdi-close" @click:append="arrayEditMode.messege = ''"
                placeholder="Комментарий" filled>
              </v-text-field>
            </div>
          </v-slide-y-transition>
          <div flat>

            <Auth v-if="getAuth === false && authbool" />
            <ConflicWindow v-if="isConflict" @offConflictWindow="offConflictWindow" />
            <TablePage :visableCard="visableCard" :infoCardOn="infoCardOn" :notVisableCard="notVisableCard"
              :addCardOn="addCardOn" :editCardOn="editCardOn" v-if="!versionsPage.data" />
            <VersionControl v-if="versionsPage.data" :versionsPage="versionsPage" />
          </div>
        </v-tab-item>
        <v-tab-item>
          <div flat>
            <MapArea :allFeatures="allFeatures" :cardVisable="cardVisable" :visableCard="visableCard"
              :notVisableCard="notVisableCard" :addCardOn="addCardOn" :infoCardOn="infoCardOn" :editCardOn="editCardOn"
              :getFeature="emptyObject" :changeElements="changeElements" />
          </div>
        </v-tab-item>
      </v-tabs-items>
    </v-main>
  </v-app>
</template>

<script>
import TablePage from './components/HelpfulFunctions/TablePage.vue';
import MapArea from './components/Map/MapArea.vue';
import CardInfo from './components/HelpfulFunctions/Card.vue';
import NavigationDrawer from './components/HelpfulFunctions/NavigationDrawer.vue';
import Auth from './components/Auth/Auth.vue';
import ConflicWindow from './components/HelpfulFunctions/ConflicWindow.vue';
import VersionControl from './components/HelpfulFunctions/VersionControl.vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiAlignHorizontalCenter } from '@mdi/js';
import { Canvg } from 'canvg';
import FIleInputWindow from './components/HelpfulFunctions/FIleInputWindow.vue';
import CardConflict from './components/HelpfulFunctions/CardConflict.vue';

export default {
  components: {
    TablePage,
    MapArea,
    CardInfo,
    NavigationDrawer,
    Auth,
    ConflicWindow,
    VersionControl,
    FIleInputWindow,
    CardConflict
  },

  data() {
    return {
      tab: null,
      filteredFeatures: [],
      items: [
        'список', 'карта'
      ],
      objectForConflict: {},
      conflictCard: false,
      cardVisable: { data: false },
      addCardOn: { data: false },
      infoCardOn: { data: false },
      editCardOn: { data: false },
      versionsPage: { data: false },
      editMode: false,
      test: mdiAlignHorizontalCenter,
      isConflict: false,
      isFileInput: false,
      arrPut: [],
      file: null,
      changeElements: [],
      componentKey: 0,
      authbool: null,
    }
  },
  watch: {
    oneType: {
      handler() {
        if (this.oneType.image) {
          setTimeout(async () => {
            let canvas = document.getElementById('png_icon_of_one_type');
            let svg = document.querySelector('#svg_icon_of_one_type svg');
            canvas.height = 24;
            canvas.width = 24;
            let v = await Canvg.from(canvas.getContext('2d'), svg.parentNode.innerHTML.trim());
            v.start();
            v.stop();
          });
        }
      },
      deep: true,
    },
    getObjectForCard: {
      handler() {
        this.visableConflictCard();
      }
    },
    emptyObject: {
      handler() {
        if (this.actions === 'getFeatures')
          this.emptyObject.group = this.oneType.group;
      }
    },
    actions: {
      handler() {
        this.notVisableCard();
        if (this.actions === 'getFeatures') {
          this.items = ['список', 'карта'];
        }
        else {
          this.items = ['список'];
        }
        setTimeout(() => {
          this.infoCardOn.data = false;
          this.addCardOn.data = false;
          this.editCardOn.data = false;
        }, 280);
      }
    },
  },
  computed: {...mapGetters(['allFeatures', 'getToolbarTitle', 'getAuth', 'getObjectForCard', 'emptyObject', 'oneType', 'arrayEditMode',
    'newData', 'actions', 'typeForLayer', 'arrayEdit', 'allListItem', 'user', 'conflictArrays']),
    
    heightVItem(){
      if(this.actions === 'getFeatures'){
        return '89.7%';
      }
      else{
        return '94%';
      }
    }
  },
  methods: {

    ...mapActions(['getFeatures', 'postFeature', 'putFeature', 'getUser', 'filterForFeature', 'deleteFeature', 'getTypeObject']),
    ...mapMutations(['updateFeature', 'updateList', 'resetArrayEditMode', 'updateNewData', 'resetNewData', 'deleteObjectFromArrayEditMode']),

    visableVersions() {
      this.versionsPage.data = true
    },
    notVisableVersions() {
      this.versionsPage.data = false
    },

    visableCard() {
      this.cardVisable.data = true;
    },
    notVisableCard() {
      this.cardVisable.data = false;
    },
    disabledAddButton() {
      return !this.cardVisable.data && JSON.stringify(this.emptyObject) === '{}';
    },
    async onmessage(e) {
      const data = JSON.parse(e.data);
      console.log(data);
      switch (data.action) {
        case "update": {
          if (this.editMode) {
            let editObject = this.arrayEditMode[data.data.group].put.filter(el => el.id === data.data.id);

            if (editObject.length && this.searchConflict(editObject[0], data.data)) {
              await this.updateNewData(data.data);
              this.visableConflictCard();
              if (this.newData.length === 1) {
                this.isConflict = true;
              }
            }
          }
          break;
        }
        case 'delete':
          if (this.editMode) {
            this.deleteObjectFromArrayEditMode(data.data);
          }
          if (this.getObjectForCard && this.getObjectForCard.id === data.data.id) {
            this.infoCardOn.data = false;
            this.editCardOn.data = false;
            this.notVisableCard();
          }
          break;
        default:
          if ('content' in data && (data.content === 'Все объекты добавлены и обновлены!' || data.content === 'Все объекты добавлены!')) {
            this.getFeatures();
          }
          break;
      }
    },
    async editObjects() {
      for (let key in this.arrayEditMode) {
        if (key != 'messege') {
          await this.putFeature({ ...this.arrayEditMode[key], messege: this.arrayEditMode.messege + `(${key})`, group: key });
        }
      }

      if (this.conflictArrays.length || this.newData.length){
        this.isConflict = true;
        return;
      }

      this.resetArrayEditMode();
      this.editMode = !this.editMode;
      this.getTypeObject();

    },
    offConflictWindow() {
      this.isConflict = !this.isConflict;
    },
    offFileInput() {
      this.isFileInput = !this.isFileInput;
    },
    searchConflict(itemFirst, itemSecond) {
      let result = false;
      for (let key in itemFirst) {
        if (typeof itemFirst[key] === 'object') {
          result = result || this.searchConflict(itemFirst[key], itemSecond[key])
        }
        else if (itemFirst[key] != itemSecond[key]) {
          return true;
        }
      }
      return result;
    },
    closeEditMode() {
      this.editMode = !this.editMode;
      if (this.editCardOn.data) {
        this.editCardOn.data = !this.editCardOn.data;
        this.infoCardOn = !this.editCardOn.data;
      }
      this.resetNewData();
      this.resetArrayEditMode();
      this.getFeatures();
      this.filterForFeature(this.oneType.id);
    },
    visableConflictCard() {
      let object = this.newData.find(el => el.id === this.getObjectForCard.id);
      if (object) {
        this.objectForConflict = object
        this.conflictCard = true;
      }
      else if (this.conflictArrays.find(el => el.find(element => element.id_ === undefined ? element.id === this.getObjectForCard.id : element.id_ === this.getObjectForCard.id_ ))) {
        this.conflictCard = true;
      }
      else{
        this.conflictCard = false;
      }
    },
    checkPath() {
      if (location.pathname === '/') {
        this.authbool = true
      } else {
        this.authbool = false
      }
    },
  },
  mounted() {
    this.checkPath()
    this.getUser();
    this.getFeatures();

    const chatSocket = new WebSocket("ws://localhost:8000/test");
    chatSocket.onmessage = this.onmessage;
  }
}
</script>

<style>
* {
  scrollbar-width: thin;
  scrollbar-color: #A9A9A9;
}

*::-webkit-scrollbar {
  width: 8px;
}

*::-webkit-scrollbar-thumb {
  background-color: #A9A9A9;
  border-radius: 16px;
}

.v-application--wrap {
  flex-direction: unset !important;
}

.v-navigation-drawer--fixed {
  position: unset !important;
  z-index: none;
}

.v-autocomplete {
  max-width: 65.93% !important;
  height: 3.57% !important;
  max-height: 3.57% !important;
  align-items: center !important;
  background: #FAFAFA !important;
  border-radius: 8px !important;
}

.v-list-item--link {
  background-color: #FAFAFA;
}

.v-list-item__title {
  font-size: 20px !important;
}

.v-label {
  font-size: 14px !important;
}

.v-main {
  padding-left: 0 !important;
}

.v-tabs-items {
  background-color: #FFFFFF !important;
}

.v-tabs-slider-wrapper {
  padding: 0 16px !important;
}

.v-divider {
  border-color: #E0E0E0 !important;
}

.v-navigation-drawer__border {
  background-color: #E5E5E5 !important;
}

.v-toolbar {
  /* min-height: 10.3% !important; */
  max-height: 6.74% !important;
}

.features {
  max-height: 10% !important;
}

.v-input__prepend-outer {
  min-width: 100% !important;
  min-height: 100% !important;
  height: 100% !important;
  margin: 0 !important;
}

.two_background_color_red .v-icon--link .v-icon__svg {
  min-width: 70px !important;
  min-height: 70px !important;
  fill: #FFFFFF !important;
}

.v-icon--link .v-icon__svg {
  min-width: 133.33px !important;
  min-height: 133.33px !important;
  fill: #FFFFFF !important;
}

.v-btn {
  padding: 4px 20px !important;
  margin: 16px 24px 16px 0 !important;
  font-size: 14px;
  border-radius: 8px;
}

.features .v-toolbar__content {
  min-height: 50% !important;
  max-height: 50% !important;
}

.v-toolbar__content {
  /* min-height: 100% !important; */
  justify-content: space-between;
  max-height: 100% !important;
}

.v-toolbar__extension {
  min-height: 50% !important;
  max-height: 50% !important;
  padding-bottom: 0 !important;
}

.v-toolbar__extension .v-tabs {
  height: 100% !important;
}

html {
  overflow: hidden !important;
}

.v-application code.code--custom {
  all: unset;
  background-color: #E5E5E5;
}

.v-window__container {
  min-height: 100%;
}

.v-tabs {
  max-height: 128%;
}

.v-tabs>*,
.v-tabs>*:after,
.v-tabs>*:before {
  max-height: 100% !important;
}

.edit_line {
  position: relative;
  height: 45px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.blur {
  filter: blur(3px) !important;
}

@media (min-width: 1025px) and (max-width: 1919px) {
  .v-toolbar {
    /* min-height: 10.3% !important; */
    max-height: 6.74% !important;
  }

  .features {
    max-height: 12% !important;
  }

  .features .v-toolbar__content {
    min-height: 50% !important;
    max-height: 50% !important;
  }

  .v-toolbar__content {
    /* min-height: 100% !important; */
    justify-content: space-between;
    max-height: 100% !important;
  }
}
</style>



