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
            <button class="edit" @click="edit(feature, '.edit_window')">Редактировать</button>
            </div>
        </vl-overlay>
        </template>
    </vl-interaction-select>
</template>

<script>

export default {
  name: 'OverlayInfo',
  props: ['edit'],
  components: {

  },
  data() {
    return {
      
    }
  },
  }
  
</script>

<style>
#content {
  margin-top: 40em;
}

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
  border: 1px solid grey;
  padding: 2px;
}

.add{
  min-width: 5em;
  max-height: 2.5em;

}

.edit_window {
  border-left: 1px solid black;
  min-width: 20em;
}

.save {
  margin-left: 1em;
}
</style>