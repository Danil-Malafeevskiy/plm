<template>
  <v-app>

    <NavigationDrawer :addCardOn="addCardOn" />

    <v-main>

      <v-toolbar color="#E5E5E5" style="border-bottom: 1px solid #E0E0E0; box-shadow: none;">
        <v-toolbar-title>{{  getToolbarTitle  }}</v-toolbar-title>
        <template v-slot:extension>

          <v-tabs v-model="tab" align-with-title color="#E93030">
            <v-tab v-for="item in items" :key="item" class="ma-0">
              <span>{{  item  }}</span>
            </v-tab>
          </v-tabs>
          <v-btn @click="editMode = !editMode" class="pa-0" style="margin: 0 10px 0 0 !important" fab small
            elevation="0" color="#E5E5E5">
            <v-icon>
              mdi-pencil
            </v-icon>
          </v-btn>
          <v-btn :disabled="cardVisable.data" class="show__card" height="28px" width="80px" depressed
            color="#EE5E5E" @click="addCardOn.data = !addCardOn.data; visableCard();">
            <v-icon color="white !default" dark>
              mdi-plus
            </v-icon>
          </v-btn>

        </template>
      </v-toolbar>

      <v-tabs-items v-model="tab" style="height: 89.7%">

        <CardInfo :cardVisable="cardVisable" :addCardOn="addCardOn" :infoCardOn="infoCardOn" :editCardOn="editCardOn"
          :visableCard="visableCard" :notVisableCard="notVisableCard" :editMode="editMode" />

        <v-tab-item>
          <div v-if="editMode" class="edit_line">
            <div>
              <a @click="editMode = !editMode" style="margin: 5px 20px">
                <v-icon small>mdi-close</v-icon>
              </a>
              <span style="color: #454545;">Редактирование</span>
            </div>
            <div>
              <span style="color: #454545; margin-right: 20px">{{ arrayEditMode.put.length + arrayEditMode.post.length + arrayEditMode.delete.length }} объектов</span>
              <v-btn @click="editObjects" plain class="pa-0" style="margin: 0 10px 0 0">
                <span style="color: #454545;">применить</span>
              </v-btn>
            </div>
          </div>
          <div flat>
            <Auth v-if="getAuth === false" />
            <!-- <ConflicWindow /> -->

            <TablePage :visableCard="visableCard" :infoCardOn="infoCardOn" :notVisableCard="notVisableCard"
              :addCardOn="addCardOn" :editCardOn="editCardOn" />
          </div>
        </v-tab-item>
        <v-tab-item>
          <div flat>
            <MapArea :allFeatures="allFeatures" :visableCard="visableCard" :notVisableCard="notVisableCard"
              :addCardOn="addCardOn" :infoCardOn="infoCardOn" :editCardOn="editCardOn" :getFeature="emptyObject" />
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
import { mapActions, mapGetters, mapMutations } from 'vuex';
import ConflicWindow from './components/HelpfulFunctions/ConflicWindow.vue';


export default {
  components: {
    TablePage,
    MapArea,
    CardInfo,
    NavigationDrawer,
    Auth,
},
  data() {
    return {
      tab: null,
      filteredFeatures: [],
      items: [
        'список', 'карта'
      ],
      cardVisable: { data: false },
      addCardOn: { data: false },
      infoCardOn: { data: false },
      editCardOn: { data: false },
      editMode: false,
      test: null,
      feature: this.getFeature,
    }
  },
  watch: {
    editMode: {
      handler(){
        if(!this.editMode){
          this.resetArrayEditMode();
          this.filterForFeature(this.oneType.id);
        }
      }
    },
    // emptyObject: {
    //   handler(){
    //     //console.log(this.emptyObject)
    //   }
    // }
  },
  computed: mapGetters(['allFeatures', 'getFeature', 'getToolbarTitle', 'getAuth', 'getObjectForCard', 'emptyObject', 'oneType', 'arrayEditMode']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature', 'putFeature', 'getUser', 'filterForFeature', 'deleteFeature', 'getOneTypeObject']),
    ...mapMutations(['updateFeature', 'updateList', 'resetArrayEditMode']),
    visableCard() {
      this.cardVisable.data = true;
    },
    notVisableCard() {
      this.cardVisable.data = false;
    },
    disabledAddButton() {
      return !this.cardVisable.data && JSON.stringify(this.emptyObject) === '{}';
    },
    onmessage(e) {
      const data = JSON.parse(e.data);
      this.getFeatures();
      if (data.data.name === this.oneType.id) {
        this.filterForFeature(this.oneType.id);
      }
      switch (data.action) {
        case "update":
          console.log(data.data)
          console.log("Success update!")
          break;
        case "create":
          console.log(data.data)
          console.log("Success create!")
          break;
        case 'delete':
          console.log(data.data);
          break;
        default:
          break;
      }
    },
    editObjects(){
      let arrPut = this.arrayEditMode.put;
      let arrDel = { id: [] };
      for(let key in this.arrayEditMode.delete){
        arrDel.id.push(this.arrayEditMode.delete[key].id)
      }
      console.log(arrDel)
      arrPut.forEach(element => {
        this.putFeature(element);
      });
      this.deleteFeature(arrDel);
      this.resetArrayEditMode();
      this.editMode = !this.editMode;
    }
  },
  mounted() {
    const chatSocket = new WebSocket("ws://localhost:8000/test");
    const webSocket = new WebSocket("ws://127.0.0.1:8000/test")

    webSocket.onmessage = this.onmessage;
    chatSocket.onmessage = this.onmessage;

    this.getUser();
    this.getFeatures();
    this.getOneTypeObject({ id: 2, test: true })
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
  background-color: #E5E5E5 !important;
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
  min-height: 10.3% !important;
  max-height: 10.3% !important;
}

.v-input__prepend-outer {
  min-width: 100% !important;
  min-height: 100% !important;
  height: 100% !important;
  margin: 0 !important;
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
}

.v-toolbar__content {
  min-height: 50% !important;
  max-height: 50% !important;
}

.v-toolbar__extension {
  min-height: 50% !important;
  max-height: 50% !important;
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
  background-color: #FBDADA;
  position: relative;
  height: 45px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>


