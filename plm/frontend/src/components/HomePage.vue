<template>
    <div id="container">
      <div id="title">
        Карта ЛЭП
      </div>
      <br>
      <div id="subtitle">
        Автоматизированное приложение для решения поставленных задач<br>

        Здесь должна быть таблица
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
    opacity: 0;
    animation: ani 1.5s forwards;
    
  }

  @keyframes ani {
  0% {opacity: 0;}
  100% {opacity: 1;}

}


</style>