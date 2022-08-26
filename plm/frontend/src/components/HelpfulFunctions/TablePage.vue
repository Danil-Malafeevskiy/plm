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
        <v-menu offset-y v-if="type.length != 0">
          <template v-slot:activator="{ on, attrs }">
            <v-btn depressed class="ma-0" color="#E5E5E5" v-bind="attrs" v-on="on">
              <span style="color: #787878">Переместить в </span>
              <v-icon color="#787878">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in type" :key="index" link @click="moveObject(item)">
              <v-list-item-title>{{ item.name }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-btn color="#E5E5E5" depressed class="ma-0" @click="deleteObjects">
          <span style="color: #787878">Удалить</span>
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
      :items="allListItem" :items-per-page="10" class="pa-0"
        @toggle-select-all="showAll()"
        :item-class="classRow"
        style="
        height: 100% !important;
        width: 50% !important; 
        background-color: #E5E5E5; 
        box-shadow: none !important;
        margin-left: 2% !important;
      ">
      </v-data-table>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';

export default {
  name: 'TablePage',
  props: ['infoCardOn', 'visableCard', 'notVisableCard', 'addCardOn', 'editCardOn'],
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
    // arrObjects: {
    //   handler() {
    //     console.log(this.arrObjects[this.nameArray])
    //   },
    //   deep: true
    // }
  },
  computed: {
    ...mapGetters(['allFeatures', 'getFeature', 'allListItem', 'getObjectForCard', 'headers', 'arrObjects', 'nameArray', 'allType', 'drawType', 'getToolbarTitle']),
    selected: {
      get() { return this.arrObjects[`${this.nameArray}`]; },
      set(value) { this.updateSelectedObejcts({ objects: value, name: this.nameArray }); }
    },
    type() {
      return this.allType.filter(el => el.type != undefined ? el.type === this.drawType && el.name != this.getToolbarTitle : el.name != this.getToolbarTitle);
    }
  },
  methods: {
    ...mapActions(['getAllObject', 'getOneObject', 'deleteObject', 'putObject', 'filterForFeature']),
    ...mapMutations(['emptyFeature', 'updateFeature', 'addSelectedObject', 'updateSelectedObejcts']),

    async showCard(obj) {
      //console.log(obj);
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
    showAll(){
      if (JSON.stringify(this.selected) === JSON.stringify(this.allListItem)) {
        this.selected = [] ;
      } else {
        this.selected = this.allListItem;
      }
    },
    resetSelected() {
      this.arrObjects[`${this.nameArray}`] = [];
    },
    async deleteObjects() {
      for (const element of this.arrObjects[`${this.nameArray}`]) {
        this.deleteObject(element.id);
      }
      await this.filterForFeature();
      this.getAllObject();
      this.resetSelected();
    },
    async moveObject(type) {
      for (const element of this.arrObjects[`${this.nameArray}`]) {
        await this.getOneObject(element.id);
        console.log(this.getObjectForCard);
        if (type.type != undefined) {
          this.getObjectForCard.name = type.id;
        }
        else {
          this.getObjectForCard.groups = [`${type.name}`];
        }
        this.putObject(this.getObjectForCard);
      }

      if (type.type != undefined) {
        await this.filterForFeature();
      }
      this.getAllObject();
      this.resetSelected();
    },
    classRow(item){
      if(this.getObjectForCard != null && item.id === this.getObjectForCard.id && (this.infoCardOn_.data || this.editCardOn.data)){
        return 'v-data-table__selected';
      }
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