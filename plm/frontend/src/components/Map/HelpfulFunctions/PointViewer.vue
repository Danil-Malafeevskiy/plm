<template>
    <vl-feature>
        <vl-geom-multi-point :coordinates="[]"></vl-geom-multi-point>
    </vl-feature>
</template>

<script>

  export default {
    data () {
      return { 
        zoom: 2,
        center: [0, 0],
        rotation: 0,
      }
    }
  }
</script>

<style>

</style>