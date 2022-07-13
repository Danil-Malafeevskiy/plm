<template>
  <div id="card">
    <div v-if="feature != null">
      <div v-for="(f, index) in feature.properties" :key="f.number_support">
         <p v-if='(index != "geometry") && f && (index != "v_defects")'>{{ index }}: {{ f }}</p>
      </div>
      <button class="edit btn" @click="edit(feature, '.edit_window')"><img src="/static/edit.png"></button>
      <button class="edit btn" @click="deleteFeature(feature.id); overlay.setPosition(undefined);"><img src="/static/delete.png"></button>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'OverlayInfo',
  props: ['dialog', 'edit', 'feature', 'overlay'],
  methods: mapActions(['deleteFeature']),
}

</script>

<style>
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

.add {
  min-width: 5em;
  max-height: 2.5em;

}

.btn>img {
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