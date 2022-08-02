<template>
  <div class="child" v-if="filterFeature.length != 0">
    <p class="object ma-0" v-if="items.length % 10 === 1">{{ items.length }} объект </p>
    <p class="object ma-0" v-else-if="items.length % 10 > 1 && items.length % 10 < 5">{{ items.length }} объекта </p>
    <p class="object ma-0" v-else>{{ items.length }} объектов </p>
    <v-data-table @click:row="test" :headers="headers" show-select item-key="Номер опоры" :items="items"
      :items-per-page="10" class="pa-0" style="
        height: 100% !important;
        width: 50% !important; 
        background-color: #E5E5E5; 
        box-shadow: none !important;
        margin-left: 2% !important;;
      "></v-data-table>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';


export default {
  name: 'TablePage',
  props: ['infoCardOn', 'visableCard', 'notVisableCard', 'addCardOn'],
  data() {
    return {
      features: {
        features: this.allFeatures
      },
      feature: this.getFeature,
      items: [],
      headers: [
        {
          text: 'Номер опоры',
          align: 'start',
          sortable: false,
          value: 'Номер опоры',
        },
        { text: 'ВЛ', value: 'ВЛ' },
        { text: 'Тип опоры', value: 'Тип опоры' },
        { text: 'Материал', value: 'Материал' },
      ],
      infoCardOn_: this.infoCardOn,
      addCardOn_: this.addCardOn,
    }
  },
  watch: {
    getFeature: function () {
      this.feature = this.getFeature;
    },
    allFeatures: function () {
      this.features = this.allFeatures;
    },
    filterFeature: {
      handler() {
        this.items = [];
        this.filterFeature.forEach(element => {
          let test = element.properties;
          test.id = element.id;
          this.items.push(test);
        });
      }
    }
  },
  computed: mapGetters(['allFeatures', 'getFeature', 'filterFeature']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature', 'getOneFeature']),
    ...mapMutations(['emptyFeature', 'updateFeature']),
    async test(obj) {
      if (!this.addCardOn.data) {
        if (this.getFeature.id != obj.id || !this.infoCardOn_.data) {
          await this.getOneFeature(obj.id);
          this.infoCardOn_.data = true;
          this.visableCard();
        }
        else {
          this.infoCardOn_.data = false;
          this.notVisableCard();
        }
      }
    }
  },
  async mounted(){
  },
}
</script>

<style>
.v-data-table__selected {
  background-color: #FBDADA !important;
}

.object {
  padding-left: 2% !important;
  padding-top: 1% !important;
  width: 50%;
  display: inline-block;
}

#title {
  font-size: 96px;
}

.v-window__container {
  position: relative;
  display: block !important;
}

.child {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
}

#subtitle {
  font-size: 32px;
  color: #EF5350;
}

#container {
  opacity: 0;
  animation: ani 1.5s forwards;

}

.v-data-table__wrapper {
  overflow-x: hidden !important;
}

@keyframes ani {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }

}
</style>