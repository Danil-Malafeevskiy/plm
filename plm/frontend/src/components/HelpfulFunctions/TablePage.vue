<template>
  <div class="child" v-if="allListItem.length != 0">
    <div class="sub_tittle">
      <p>{{ selected.length }}</p>
      <span class="object" v-if="allListItem.length % 10 === 1">{{ allListItem.length }} объект </span>
      <span class="object" v-else-if="allListItem.length % 10 > 1 && allListItem.length % 10 < 5">
        {{ allListItem.length }} объекта </span>
      <span class="object" v-else>{{ allListItem.length }} объектов </span>
      
      <v-icon v-if="selected.length != 0" small>mdi-close</v-icon>
      <div style="margin: 20px;" v-if="selected.length != 0">
        <a @click="deleteObjects">
          <span style="color: #787878;"></span>Удалить
        </a>
      </div>
    </div>
    <v-data-table @click:row="showCard"
      :headers="headers" v-model="selected" show-select :item-key="headers[0].text" :items="allListItem" :items-per-page="10" class="pa-0"
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
  name: 'TablePage',
  props: ['infoCardOn', 'visableCard', 'notVisableCard', 'addCardOn'],
  data() {
    return {
      features: {
        features: this.allFeatures
      },
      feature: this.getFeature,
      infoCardOn_: this.infoCardOn,
      addCardOn_: this.addCardOn,
      test: [],
    }
  },
  watch: {
    getFeature: function () {
      this.feature = this.getFeature;
    },
    allFeatures: function () {
      this.features = this.allFeatures;
    },
    arrObjects: {
      handler(){
        console.log(this.arrObjects);
      },
      deep: true,
    }
    // allListItem:{
    //   handler(){
    //     for(let i in this.allListItem){
    //       if(typeof (this.allListItem[i]) === 'object'){
    //         delete this.allFeatures[i];
    //       }
    //     }
    //   },
    //   deep: true
    // }
  },
  computed: {
    ...mapGetters(['allFeatures', 'getFeature', 'allListItem', 'getObjectForCard', 'headers', 'arrObjects', 'getToolbarTitle']),
    selected: {
      get() { return this.arrObjects[`${this.getToolbarTitle}`]; },
      set(value) { this.updateSelectedObejcts({objects: value, name: this.getToolbarTitle}); }
    },
    selectedLength(){
      return this.arrObjects[`${this.getToolbarTitle}`].length;
    }
  },
  methods: {
    ...mapActions(['getFeatures', 'postFeature', 'getOneFeature', 'getOneObject', 'deleteObject']),
    ...mapMutations(['emptyFeature', 'updateFeature', 'addSelectedObject', 'updateSelectedObejcts']),

    async showCard(obj) {
      if (!this.addCardOn.data) {
        if (this.getObjectForCard === null || this.getObjectForCard.id != obj.id || !this.infoCardOn_.data) {
          await this.getOneObject(obj.id);
          this.visableCard();
          this.infoCardOn_.data = true;
        }
        else {
          this.infoCardOn_.data = false;
          this.notVisableCard();
        }
      }
    },
    // selectAllobject({ items, value }) {
    //   if (value) {
    //     this.updateSelectedObejcts(items);
    //   }
    //   else {
    //     this.updateSelectedObejcts([]);
    //   }
    //   console.log(this.arrObjects);

    // },
    // selectOneObject({ item, value }) {
    //   console.log(this.selected);
    //   if (value) {
    //     this.addSelectedObject(item);
    //   }
    //   else {
    //     let newArr = this.arrObjects.filter(element => element != item)
    //     this.updateSelectedObejcts(newArr);
    //   }
    //   console.log(this.arrObjects)
    // },
    deleteObjects() {
      this.arrObjects.forEach(element => {
        this.deleteObject(element.id);
      });
    }
  },
  async mounted() {
  },
}
</script>

<style>
.v-data-table__selected {
  background-color: #FBDADA !important;
}

.sub_tittle {
  display: flex;
  /* min-width: 100%; */
  /* width: 50%; */
}

.object {
  /* padding-left: 2% !important;
  padding-top: 1% !important;
  width: 50%;
  display: inline-block; */
  margin: 20px;
  color: #787878;
  font-weight: 500;
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