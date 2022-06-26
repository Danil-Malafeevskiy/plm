<template>
  <v-content>
    <div id="map">
     <MapArea />
    </div>
  </v-content>
</template>

<script>
import MapArea from "@/components/Map/MapArea.vue";

  export default {
    name: 'MapView',

    components: {
      MapArea,
  },
  }
</script>
