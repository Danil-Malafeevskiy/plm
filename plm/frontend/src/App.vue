<template>
  <v-app style="display: flex">
    
    <NavigationDrawer />
    <v-main>
      <v-toolbar color="#E5E5E5" style="border-bottom: 1px solid #E0E0E0;">
        <v-toolbar-title>Your Dashboard</v-toolbar-title>

        <template v-slot:extension>

          <v-tabs v-model="tab" align-with-title color="#E93030">
            <v-tab v-for="item in items" :key="item" class="ma-0">
              <span>{{ item }}</span>
            </v-tab>
          </v-tabs>
          <v-btn class="show__card" height="28px" width="80px" depressed color="#EE5E5E"
            @click="visableCard(); addCardOn.data = !addCardOn.data; emptyFeature()">
            <v-icon color="white !default" dark>
              mdi-plus
            </v-icon>
          </v-btn>

        </template>
      </v-toolbar>
      <v-tabs-items v-model="tab" style="height: 89.7%">
        <CardInfo :cardVisable="cardVisable" :addCardOn="addCardOn" :infoCardOn="infoCardOn" :editCardOn="editCardOn"
          :getFeature="getFeature" :visableCard="visableCard" :notVisableCard="notVisableCard" />
        <v-tab-item>
          <div flat>
            <TablePage />
          </div>
        </v-tab-item>
        <v-tab-item>
          <div flat>
            <MapArea :allFeatures="allFeatures" :cord="cord" :visableCard="visableCard" :notVisableCard="notVisableCard"
              :addCardOn="addCardOn" :infoCardOn="infoCardOn" :editCardOn="editCardOn" :getFeature="getFeature" />
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
import { mapActions, mapGetters, mapMutations } from 'vuex';

export default {
  components: {
    TablePage,
    MapArea,
    CardInfo,
    NavigationDrawer,
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
      test: null,
      feature: this.getFeature,
      cord: { data: [NaN, NaN] },
    }
  },
  watch: {
    getFeature: function () {
      this.feature = this.getFeature;
    },
    selectedItem: {
      handler() {
        const domItem = document.querySelector('.v-item-group').childNodes[this.selectedItem];
        if (domItem != undefined) {
          this.filteredFeatures = this.allFeatures.filter(r => (` ${r.name}` === domItem.childNodes[0].innerText))
        }
      },
    }
  },
  computed: mapGetters(['allFeatures', 'getFeature']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature', 'putFeature']),
    ...mapMutations(['emptyFeature', 'updateFeature']),
    visableCard() {
      this.cardVisable.data = true;
      let btn = document.querySelector('.v-btn');
      btn.setAttribute('disabled', true);
      btn.classList.add('v-btn--disabled');
    },
    notVisableCard() {
      this.cardVisable.data = false;
      let btn = document.querySelector('.v-btn');
      btn.removeAttribute('disabled', false);
      btn.classList.remove('v-btn--disabled');
    },
  },
  mounted() {
    this.getFeatures();
    this.emptyFeature();
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

/* .v-list-item__content{
  margin: 31.25% 20px;
} */

/* .v-item--active{
  background-color: #FDEDED;
} */

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

.card__window {
  position: absolute;
  top: 0;
  bottom: 0;
  min-width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 12px;
}

.card__img {
  align-items: flex-start;
}

.v-input__icon,
.v-icon--link {
  min-width: 100% !important;
  height: 100% !important;
  min-height: 100% !important;
  justify-content: center !important;
  align-items: center !important;
}

.v-icon--link::after {
  background-color: rgba(255, 255, 255, 0) !important;
}

.v-file-input {
  min-height: 37.53%;
  background-color: #EE5E5E;
  border-radius: 12px 12px 0 0;
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

.card__info {
  align-items: center;
}

.card__footer {
  align-items: flex-end;
  display: flex;
  bottom: 0px;
  justify-content: flex-end;
  border-top: 1px solid #E0E0E0;
  border-radius: 0 0 12px 12px !important;
  background-color: white;
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

.show__card {
  margin-right: 8px;
  border-radius: 8px !important;
}

.v-window__container {
  min-height: 100%;
}

.v-card {
  z-index: 1 !important;
  min-height: 92.08% !important;
  position: absolute !important;
  left: 60.28% !important;
  top: 4.19% !important;
  border-radius: 12px !important;
}

.v-tabs {
  max-height: 128%;
}

.v-tabs>*,
.v-tabs>*:after,
.v-tabs>*:before {
  max-height: 100% !important;
}

.row {
  padding: 24px 24px 12px 24px !important;
}
</style>


