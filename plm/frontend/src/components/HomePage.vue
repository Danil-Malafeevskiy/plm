<template>
    <div class="child">
      <p class="object ma-0">{{ items.length }} объекта </p>
      <v-data-table :headers="headers" show-select :items="items" :items-per-page="14" class=" pa-0"
        style="
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
  name: 'HomePage',
  data() {
    return {
      features: {
        features: this.allFeatures
      },
      feature: this.getFeature,
      items: [],
      headers: [
        {
          text: 'MAMA',
          align: 'start',
          sortable: false,
          value: 'number_support',
        },
        { text: 'VL', value: 'VL' },
        { text: 'type_support', value: 'type_support' },
        { text: 'material', value: 'material' },
      ],
    }
  },
  watch: {
    getFeature: function () {
      this.feature = this.getFeature;
    },
    allFeatures: function () {
      this.features = this.allFeatures;
      this.addItem();
    },

  },
  computed: mapGetters(['allFeatures', 'getFeature']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature']),
    ...mapMutations(['emptyFeature', 'updateFeature']),

    addItem(){
      this.features.forEach(element => {
        this.items.push(element.properties);
      });
    }
  },

  async mounted() {
    await this.getFeatures();
    await this.emptyFeature();
  }

}
</script>

<style>

.v-data-table__selected{
  background-color: #FBDADA !important;
}

.object{
  padding-left: 2% !important;
  padding-top: 1% !important;
  width: 50%;
  display: inline-block;
}

#title{
  font-size: 96px;
}

.v-window__container {
  position: relative;
  display: block !important;
}

.child{
  position: absolute; 
  left:0;
  right:0;
  top:0;
  bottom:0;
}

#subtitle{
  font-size: 32px;
  color: #EF5350;
}

#container{
  opacity: 0;
  animation: ani 1.5s forwards;
  
}
.v-data-table__wrapper{
  overflow-x: hidden !important;
}
@keyframes ani {
0% {opacity: 0;}
100% {opacity: 1;}

}

</style>