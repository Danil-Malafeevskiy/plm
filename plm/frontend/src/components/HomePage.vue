<template>
    <div id="container">
      <div id="title">
        Карта ЛЭП
      </div>
      <br>
      <div id="subtitle">
        Автоматизированное приложение для решения поставленных задач
      </div>
    </div>
</template>

<script>

  export default {
    name: 'HomePage',
  }
</script>

<style>

  #title{
    font-size: 96px;
  }

  #subtitle{
    font-size: 32px;
    color: #EF5350;
  }

  #container{
    margin-top: 25em;
    margin-left: 0em;
    opacity: 0;
    animation: ani 1.5s forwards;
    
  }

  @keyframes ani {
  0% {opacity: 0;}
  100% {opacity: 1;}

}


</style>