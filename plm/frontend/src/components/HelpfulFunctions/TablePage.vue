<template>
  <div v-if="allListItem[0] !== user">
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
      <span class="object" v-if="tableArrayItems.length % 10 === 1">{{ tableArrayItems.length }} объект </span>
      <span class="object" v-else-if="tableArrayItems.length % 10 > 1 && tableArrayItems.length % 10 < 5">
        {{ tableArrayItems.length }} объекта </span>
      <span class="object" v-else>{{ tableArrayItems.length }} объектов </span>
    </div>
    <v-data-table @click:row="showCard" :headers="headers" v-model="arrObjects[`${nameArray}`]" show-select
      :item-key="headers[0].text" :items="tableArrayItems" :items-per-page="5" class="pa-0"
      @toggle-select-all="showAll()" :item-class="classRow" style="
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
      infoCardOn_: this.infoCardOn,
      addCardOn_: this.addCardOn,
      editCardOn_: this.editCardOn,
      tableArrayItems: [],
    }
  },
  watch: {
    oneType: {
      handler() {
        this.getSortType(this.oneType.type);
      }
    },
    allListItem: {
      handler() {
        this.tableArrayItems = [...this.allListItem];
        if (this.oneType.group in this.arrayEditMode && this.arrayEdit.post.length) {
          for (let i in this.arrayEdit.post) {
            this.tableArrayItems.push({ ...this.arrayEdit.post[i].properties, id_: this.arrayEdit.post[i].id_ });
          }
        }
      }
    },
    arrayEditMode: {
      handler() {
        this.tableArrayItems = [...this.allListItem];
        if (this.oneType.group in this.arrayEditMode && this.arrayEdit.post.length) {
          for (let i in this.arrayEdit.post) {
            this.tableArrayItems.push({ ...this.arrayEdit.post[i].properties, id_: this.arrayEdit.post[i].id_ });
          }
        }
      },
      deep: true,
    }
  },
  computed: {
    ...mapGetters(['allListItem', 'getObjectForCard', 'headers', 'arrObjects', 'nameArray',
      'drawType', 'getToolbarTitle', 'arrayEditMode', 'newData', 'oneType',
      'selectedDrawType', 'actions', 'allGroups', 'user', 'arrayEdit']),
    selected: {
      get() {
        if (this.arrObjects[`${this.nameArray}`] != undefined) {
          return this.arrObjects[`${this.nameArray}`];
        }
        else {
          return [];
        }
      },
      set(value) { this.updateSelectedObejcts({ objects: value, name: this.nameArray }); }
    },
    type() {
      if ('username' in this.arrObjects[`${this.nameArray}`][0]) {
        return this.allGroups.filter(el => el.name != this.getToolbarTitle)
      }
      else {
        console.log(this.oneType.group);
        return this.selectedDrawType.filter(el => el.name != this.getToolbarTitle && el.group === this.oneType.group);
      }
    }
  },
  methods: {
    ...mapActions(['getAllObject', 'getOneObject', 'deleteObject', 'putObject', 'filterForFeature', 'getOneTypeObjectForFeature', 'getSortType']),
    ...mapMutations(['emptyFeature', 'updateFeature', 'addSelectedObject', 'updateSelectedObejcts', 'updateOneType', 'updateObjectForCard']),

    async showCard(obj) {
      if (!this.addCardOn.data) {
        if (this.getObjectForCard === null || this.getObjectForCard.id != obj.id ||
          (this.getObjectForCard.id == obj.id && !this.checkequalsItems(obj, this.getObjectForCard)) || !this.infoCardOn_.data) {
          if ('id_' in obj) {
            this.updateObjectForCard(JSON.parse(JSON.stringify(this.arrayEdit.post.find(el => el.id_ === obj.id_))));
          }
          else {
            const object = this.arrayEdit.put.filter(el => el.id === obj.id);
            if (object.length) {
              this.updateObjectForCard(JSON.parse(JSON.stringify(object[0])));
            }
            else {
              await this.getOneObject(obj.id);
            }
          }
          this.visableCard();
          this.infoCardOn_.data = true;
          this.editCardOn_.data = false;
        }
        else {
          await this.notVisableCard();
          setTimeout(() => this.infoCardOn_.data = false, 500);
        }
      }
    },
    showAll() {
      if (JSON.stringify(this.selected) === JSON.stringify(this.allListItem)) {
        this.selected = [];
      } else {
        this.selected = this.allListItem;
      }
    },
    resetSelected() {
      this.arrObjects[`${this.nameArray}`] = [];
    },
    async deleteObjects() {
      this.deleteObject(this.arrObjects[`${this.nameArray}`]);
      this.resetSelected();
    },
    async moveObject(type) {
      let arrPut = [];
      for (const element of this.arrObjects[`${this.nameArray}`]) {
        await this.getOneObject(element.id);
        if (this.actions === 'getFeatures') {
          this.getObjectForCard.name = type.id;
        }
        else {
          this.getObjectForCard.groups = [`${type.name}`];
        }
        arrPut.push(this.getObjectForCard);
      }
      this.putObject(arrPut);

      if (type.type != undefined) {
        await this.filterForFeature();
      }
      this.getAllObject();
      this.resetSelected();
    },
    changeItemFromTable(item, object) {
      for (let key in object) {
        if (key != 'id') {
          item[key] = object[key];
        }
      }
    },
    checkequalsItems(item, object) {
      let checkObject = { ...object.properties };
      let putObject = this.arrayEdit.put.find(el => el.id === object.id);
      putObject = putObject ? { ...putObject.properties } : 1;
      let newObject = this.newData.find(el => el.id === object.id);
      newObject = newObject ? { ...newObject.properties } : 1;
      for (let i in this.headers) {
        if (this.headers[i].text != 'id_' && this.headers[i].text != 'id' && checkObject[this.headers[i].text] !== item[this.headers[i].text]) {
          if (!(putObject && newObject && putObject[this.headers[i].text] === item[this.headers[i].text])) {
            return false;
          }
        }
      }
      return true;
    },
    classRow(item) {
      let classForItem = ''
      if (this.infoCardOn_.data || this.editCardOn.data) {
        if ('id_' in this.getObjectForCard) {
          if (item.id_ === this.getObjectForCard.id_ && this.checkequalsItems(item, this.getObjectForCard)) {
            classForItem += 'v-data-table__selected';
          }
        }
        else {
          if (item.id === this.getObjectForCard.id && this.checkequalsItems(item, this.getObjectForCard)) {
            classForItem += 'v-data-table__selected';
          }
        }
      }

      if (item.id_) {
        classForItem += ' text_color_purple';
      }

      const putObject = this.arrayEdit.put.filter(el => el.id === item.id);
      const deleteObject = this.arrayEdit.delete.filter(el => el.id === item.id);
      const newPutObject = this.newData.filter(el => el.id === item.id);

      if (newPutObject.length) {
        classForItem += ' text_color_blue';
        this.changeItemFromTable(item, putObject[0].properties);
      }
      else if (putObject.length) {
        classForItem += ' text_color_red';
        this.changeItemFromTable(item, putObject[0].properties);
      }

      if (deleteObject.length) {
        classForItem += ' text_color_gray';
        this.changeItemFromTable(item, deleteObject[0].properties);
      }

      return classForItem;
    },
  },
  mounted() {
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
}

.object {
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

.text_color_red {
  color: #D7153A;
}

.text_color_gray {
  color: gray;
}

.text_color_blue {
  color: #0F0CA7;
}

.text_color_purple {
  color: #cc1dcf;
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