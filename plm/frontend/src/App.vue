<template>
  <v-app style="display: flex">
    
    <NavigationDrawer />
    <v-main>
      <v-toolbar color="#E5E5E5" style="border-bottom: 1px solid #E0E0E0;">
        <v-toolbar-title>{{featureName}}</v-toolbar-title>

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
         :visableCard="visableCard" :notVisableCard="notVisableCard" />
        <v-tab-item>
          <div flat>
            <Auth />
            <TablePage :visableCard="visableCard" :infoCardOn="infoCardOn" :notVisableCard="notVisableCard" :addCardOn="addCardOn"/>
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
import Auth from './components/Auth/Auth.vue';
import { mapActions, mapGetters, mapMutations } from 'vuex';

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
  computed: mapGetters(['allFeatures', 'getFeature', 'featureName']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature', 'putFeature']),
    ...mapMutations(['emptyFeature', 'updateFeature']),
    visableCard() {
      this.cardVisable.data = true;
      let btn = document.querySelector('.show__card');
      btn.setAttribute('disabled', true);
      btn.classList.add('v-btn--disabled');
    },
    notVisableCard() {
      this.cardVisable.data = false;
      let btn = document.querySelector('.show__card');
      btn.removeAttribute('disabled', false);
      btn.classList.remove('v-btn--disabled');
    },
  },
  async mounted() {
    await this.getFeatures();
    this.emptyFeature();
    this.auth = document.getElementById('auth').innerText;
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



</style>


