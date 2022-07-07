<template>
    <vl-interaction-select :features.sync="selectedFeatures">
        <template slot-scope="select">
        <vl-overlay v-for="feature in select.features" :key="feature.id" :id="feature.id"
            :position="feature.geometry.coordinates" :auto-pan="true">
            <div id="card">
            Точка № {{ feature.properties.id }}<br>
            Номер опоры: {{ feature.properties.number_support }} <br>
            ВЛ: {{ feature.properties.VL }} <br>
            Тип опоры: {{ feature.properties.type_support }} <br>
            Шифр опоры: {{ feature.properties.code_support }} <br>
            Материал: {{ feature.properties.material }} <br>
            Угол: {{ feature.properties.corner }} <br>
            Высота: {{ feature.properties.height }}<br>
            <button class="edit btn" @click="edit(feature, '.edit_window')"><img src="/static/edit.png"></button>
            <button class="edit btn" @click="delet(feature.id)"><img src="/static/delete.png"></button>
            </div>
        </vl-overlay>
        </template>
    </vl-interaction-select>
</template>

<script>
import axios from 'axios';

export default {
  name: 'OverlayInfo',
  props: ['dialog', 'edit'],
  methods:{
    delet(id){
      axios.delete(`/tower/${id}`).then((response) => console.log(response.data));
      window.parent.location = window.parent.location.href;
    }
  }
  
  }
  
</script>

<style>
.v-main__wrap {
  display: flex;
}

#card {
  background: white;
  border: 1px solid grey;
  color: black;
  padding: 0.5em;
  border-radius: 8%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 0 10px rgba(128, 128, 128, 0.5);
}

.edit {
  border: 1px solid white;
  padding: 2px;
  margin-right: 5px;
}

.add{
  min-width: 5em;
  max-height: 2.5em;

}

.btn > img{
  display: block;
  max-width: 40px;
  max-height: 40px;
}

.edit_window {
  border-left: 1px solid black;
  min-width: 20em;
}

.save {
  margin-left: 1em;
}
</style>