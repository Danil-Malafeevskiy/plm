  <template>
  <div class="child" v-if="allListItem.length != 0">
    <div class="sub_tittle" v-if="selected.length != 0">
      <div style="margin: 20px 0;">
        <span class="object" v-if="selected.length % 10 === 1">{{ selected.length }} объект </span>
        <span class="object" v-else-if="selected.length % 10 > 1 && selected.length % 10 < 5">
          {{ selected.length }} объекта </span>

        <span class="object" v-else>{{ selected.length }} объектов </span>

        <a style="margin: 20px 0" @click="resetSelected()">
          <v-icon v-if="selected.length != 0" small>mdi-close</v-icon>
        </a>
      </div>
      <div style="margin-top: 20px;" v-if="selected.length != 0">
        <v-btn color="#E5E5E5" depressed class="ma-0" @click="deleteObjects">
          <span style="color: #787878; justify-content: end;">Удалить</span>
        </v-btn>
      </div>
    </div>
    <div class="sub_tittle" v-else>
      <span class="object" v-if="allListItem.length % 10 === 1">{{ allListItem.length }} объект </span>
      <span class="object" v-else-if="allListItem.length % 10 > 1 && allListItem.length % 10 < 5">
        {{ allListItem.length }} объекта </span>
      <span class="object" v-else>{{ allListItem.length }} объектов </span>
    </div>
    <v-data-table @click:row="showCard" :headers="headers" v-model="selected" show-select :item-key="headers[0].text"
      :items="allListItem" :items-per-page="10" class="pa-0" style="
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
      handler() {
        console.log(this.arrObjects[this.nameArray])
      },
      deep: true
    }
  },
  computed: {
    ...mapGetters(['allFeatures', 'getFeature', 'allListItem', 'getObjectForCard', 'headers', 'arrObjects', 'nameArray']),
    selected: {
      get() { return this.arrObjects[`${this.nameArray}`]; },
      set(value) { this.updateSelectedObejcts({ objects: value, name: this.nameArray }); }
    },
    selectedLength() {
      return this.arrObjects[`${this.nameArray}`].length;
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
    resetSelected() {
      this.arrObjects[`${this.nameArray}`] = [];
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
      for (const element of this.arrObjects[`${this.nameArray}`]) {
        this.deleteObject(element.id);
      }
      this.resetSelected();
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
  justify-content: space-between;
  width: 50%;
  /* min-width: 100%; */
  /* width: 50%; */
}

.object {
  /* padding-left: 2% !important;
  padding-top: 1% !important;
  width: 50%;
  display: inline-block; */
  margin: 20px 5px 20px 20px;
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