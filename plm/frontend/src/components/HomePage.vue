<template>
  <div id="object">
    <p>{{ items.length }} объекта </p>
    <v-data-table :headers="headers" show-select :items="items"  :items-per-page="14" 
      class="ma-0 pa-0 elevation-1" 
      
      style="
        height: 91.28%;
        width: 50% !important; 
        background-color: #E5E5E5; 
        box-shadow: none !important;
      "
    ></v-data-table>
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
    },

  },
  computed: mapGetters(['allFeatures', 'getFeature']),
  methods: {
    ...mapActions(['getFeatures', 'postFeature']),
    ...mapMutations(['emptyFeature', 'updateFeature']),

    addItem(){
      console.log(1)
      this.features.forEach(element => {
        this.items.push(element.properties);
      });
      console.log(this.items)
    }
  },

  async mounted() {
    await this.getFeatures();
    await this.emptyFeature();
    this.addItem();
  }

}
</script>

<style>

.v-data-table__selected{
  background-color: #FBDADA !important;
}

#object{
  padding-left: 2% !important;
  padding-top: 1% !important;
}

#title{
  font-size: 96px;
}

#subtitle{
  font-size: 32px;
  color: #EF5350;
}

#container{
  opacity: 0;
  animation: ani 1.5s forwards;
  
}

@keyframes ani {
0% {opacity: 0;}
100% {opacity: 1;}

}

</style>