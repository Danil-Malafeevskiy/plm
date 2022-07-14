<template>
  <v-app>
    <v-navigation-drawer app color="#DDDDDD" permanent :mini-variant-width=55 width="18.96%">
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            <v-icon left>{{ icon.mdiMenu }}</v-icon>
            База объектов
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon>{{ item }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>


    <v-main>
      <v-toolbar color="#E5E5E5" style="border-bottom: 1px solid #E0E0E0;">
        <v-toolbar-title>Your Dashboard</v-toolbar-title>

        <template v-slot:extension>

          <v-tabs v-model="tab" align-with-title color="#E93030">
            <v-tab v-for="item in items" :key="item">
              <span>{{ item }}</span>
            </v-tab>
          </v-tabs>
          <v-btn class="show__card" height="28px" width="80px" depressed color="#EE5E5E" @click="toggleBtn()">
            <v-icon color="white !default" dark>
              {{ icon.mdiPlus }}
            </v-icon>
          </v-btn>
        </template>
      </v-toolbar>
      <v-tabs-items v-model="tab" style="height: 89.7%">

        <v-card v-if="mini" width="38.05%">

          <div class="card__window">
            <div style="overflow-y: scroll; overflow-x: hidden;">
              <v-card-text class="pa-0">
                <v-form @submit.prevent="onSubmit">
                  <v-row justify="start" class="pa-2">
                    <v-col cols="2" sm="6" md="5" lg="6">
                      <v-card-text style="font-size: 24px;">Создание объекта</v-card-text>
                    </v-col>
                    <v-col v-for="(f, index) in feature_.properties" :key="f.number_support" cols="2" sm="6" md="5"
                      lg="6">
                      <v-text-field v-model="feature_.properties[index]" :value="feature_.properties[index]" hide-details :label="index" :placeholder="index" filled></v-text-field>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </div>

            <div class="card__footer">
              <v-btn color="white" depressed @click="toggleBtn()">ОТМЕНА</v-btn>
              <v-btn color="white" depressed @click="onSubmit()">Применить</v-btn>
            </div>

          </div>
        </v-card>

        <v-tab-item>
          <div flat>
            <HomePage />
          </div>
        </v-tab-item>
        <v-tab-item>
          <div flat>
            <MapArea :allFeatures="allFeatures" :cord="cord" />
          </div>
        </v-tab-item>
      </v-tabs-items>
    </v-main>
  </v-app>
</template>

<script>
import HomePage from './components/HomePage.vue'
import MapArea from './components/Map/MapArea.vue'
import * as icon from '@mdi/js'
import { mapActions, mapGetters } from 'vuex';
import { toLonLat } from 'ol/proj';
//import { toLonLat } from 'ol/proj';

export default {
  components: {
    HomePage,
    MapArea
  },
  data() {
    return {
      tab: null,
      items: [
        'СПИСОК', 'КАРТА'
      ],
      mini: false,
      icon: icon,
      test: null,
      feature_: {
        type: 'Feature',
        properties: {},
        geometry: {},
      },
      cord: {data: [NaN, NaN]}
    }
  },
  computed: mapGetters(['allFeatures']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature']),
    toggleBtn() {
      this.mini = !this.mini;
      let btn = document.querySelector('.v-btn')
      if (!btn.hasAttribute('disabled')) {
        btn.setAttribute('disabled', true);
        btn.classList.add('v-btn--disabled');
        document.querySelector('.v-icon');
      }
      else {
        btn.removeAttribute('disabled', false);
        btn.classList.remove('v-btn--disabled');
      }
    },
    async onSubmit() {
      this.feature_.geometry = {
        type: 'Point',
        coordinates: toLonLat(this.cord.data),
      }
      this.feature_.properties.shirota = this.feature_.geometry.coordinates[1];
      this.feature_.properties.dolgota = this.feature_.geometry.coordinates[0];
      console.log(JSON.stringify([this.feature_]));
      await this.postFeature(JSON.stringify([this.feature_]));
    },
  },
  async mounted() {
    await this.getFeatures();

    for (let key in this.allFeatures[0]) {
      if (key === 'properties') {
        for (let key1 in this.allFeatures[0][key]) {
          if (key1 != 'id') {
            if (typeof (this.allFeatures[0][key][key1]) === 'string')
              this.feature_[key][key1] = "";
            else if (typeof (this.allFeatures[0][key][key1]) === 'number')
              this.feature_[key][key1] = 1;
            else if (typeof (this.allFeatures[0][key][key1]) === 'boolean')
              this.feature_[key][key1] = false;
          }
        }
      }
    }
  }
}
</script>
<style>
.v-tabs-items {
  background-color: #E5E5E5 !important;
}

.v-main {
  /* min-width: 81.04% !important; */
  padding-left: 18.96% !important;
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
  padding: 0 12px !important;

}
</style>


