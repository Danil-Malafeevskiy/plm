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
            <v-btn depressed class="ma-0" color="#FFFFFF" v-bind="attrs" v-on="on">
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
        <v-btn color="#FFFFFF" depressed class="ma-0" @click="deleteObjects(oneType.group)">
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
    <v-data-table @click:row="showCard" :headers="headersForTale" v-model="selected" show-select item-key="id"
      :items="tableArrayItems" :items-per-page="heightTable" :footer-props="{ 'items-per-page-options': rowsPerPage }"
      class="pa-0" @toggle-select-all="showAll()" :item-class="classRow" style="
        height: 100% !important;
        width: 50% !important; 
        background-color: #FFFFFF; 
        box-shadow: none !important;
        margin-left: 2% !important;
      ">
    </v-data-table>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';
import Vue from "vue";

export default {
  name: 'TablePage',
  props: ['infoCardOn', 'visableCard', 'notVisableCard', 'addCardOn', 'editCardOn', 'editMode'],
  data() {
    return {
      infoCardOn_: this.infoCardOn,
      addCardOn_: this.addCardOn,
      editCardOn_: this.editCardOn,
      tableArrayItems: [],
      headersForTale: [],
      arrObjects: {},
      objectOnTable: null,
    }
  },
  watch: {
    oneType: {
      handler() {
        this.getSortType(this.oneType.type);
        this.headersForTale = this.oneType.headers;
        if (!(`${this.oneType?.name} ${this.oneType?.group}` in this.arrObjects)) {
          Vue.set(this.arrObjects, `${this.oneType?.name} ${this.oneType?.group}`, [])
        }
      }
    },
    headers: function () {
      this.headersForTale = this.headers;
    },
    allListItem: {
      handler() {
        this.addNewObjectInTable();
      }
    },
    arrayEditMode: {
      handler() {
        this.addNewObjectInTable();
      },
      deep: true,
    },
  },
  computed: {
    ...mapGetters(['allListItem', 'getObjectForCard', 'headers',
      'drawType', 'getToolbarTitle', 'arrayEditMode', 'newData', 'oneType',
      'selectedDrawType', 'actions', 'allGroups', 'user', 'arrayEdit']),
    selected: {
      get() {
        if (this.oneType && this.arrObjects[`${this.oneType.name} ${this.oneType.group}`]) {
          return this.arrObjects[`${this.oneType.name} ${this.oneType.group}`];
        }
        else {
          return [];
        }
      },
      set(items) { this.arrObjects[`${this.oneType.name} ${this.oneType.group}`] = items }
    },
    type() {
      if ('username' in this.selected[0]) {
        return this.allGroups.filter(el => el.name != this.getToolbarTitle)
      }
      else {
        return this.selectedDrawType.filter(el => el.name != this.getToolbarTitle && el.group === this.oneType.group);
      }
    },
    heightTable() {
      return Math.round((document.querySelector('.v-window__container').offsetHeight - 64 - 69 - 58 - 75) / 48) - 2 * (this.editMode ? 1 : 0);
    },
    rowsPerPage() {
      let rows = [];
      let countPage = 5;
      for (let i = 1; countPage * i < this.heightTable; i++) {
        rows.push(countPage * i);
      }
      rows.push(this.heightTable);
      return rows;
    },
    oldPutObject(){
      const putObject = this.arrayEdit.put.find(el => el.id === this.objectOnTable.id);
      return putObject ? { ...putObject.properties } : 1;
    },
    newPutObject(){
      const newObject = this.newData.find(el => el.id === this.objectOnTable.id);
      return newObject ? { ...newObject.properties } : 1;
    }
  },
  methods: {
    ...mapActions(['getAllObject', 'getOneObject', 'deleteObject', 'putObject', 'filterForFeature', 'getOneTypeObjectForFeature', 'getSortType']),
    ...mapMutations(['emptyFeature', 'updateFeature', 'addSelectedObject', 'updateSelectedObejcts', 'updateOneType', 'updateObjectForCard', 'updateArrayEditMode']),

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
      this.selected = [];
    },
    async deleteObjects(group) {
      let deleteArray;
      if (this.actions === 'getFeatures') {
        deleteArray = {};
        deleteArray.delete = this.selected;
        deleteArray.group = group;
        this.updateArrayEditMode({ item: deleteArray, type: 'delete' });
        this.$emit('openEditMode');
      }
      else {
        deleteArray = this.selected;
        this.deleteObject(deleteArray);
      }
      this.resetSelected();
    },
    async moveObject(type) {
      let arrPut = [];
      for (const element of this.selected) {
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
      this.objectOnTable = object;
      let checkObject = { ...object.properties };

      if ('first_name' in checkObject) {
        checkObject.full_name = checkObject.first_name + ' ' + checkObject.last_name;
      }

      let putObject = this.oldPutObject;
      let newObject = this.newPutObject;

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
      let classForItem = '';
      if (this.infoCardOn_.data || this.editCardOn.data) {
        if ('id_' in this.getObjectForCard) {
          if (item.id_ === this.getObjectForCard.id_) { //&& this.checkequalsItems(item, this.getObjectForCard)) {
            classForItem += 'v-data-table__selected';
          }
        }
        else {
          if (item.id === this.getObjectForCard.id) { //&& this.checkequalsItems(item, this.getObjectForCard)) {
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
    addNewObjectInTable(){
      this.tableArrayItems = [...this.allListItem];
        if (this.oneType && this.oneType.group && this.arrayEdit.post.length && this.actions === 'getFeatures') {
          for (let i in this.arrayEdit.post) {
            if (this.arrayEdit.post[i].name === this.oneType.id)
            this.tableArrayItems.push({ ...this.arrayEdit.post[i].properties, id_: this.arrayEdit.post[i].id_ });
          }
        }
    }
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