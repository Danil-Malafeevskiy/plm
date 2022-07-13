<template>
    <transition name="animation">
        <div class="add_window" v-if="showAdd">
            <p style="font-size: 32px;">Добавление объекта</p>
            <p>Выбор объекта для выделения
                <select v-model="draw.data" @change="interaction">
                    <option selected value="-">-</option>
                    <option value="Point">Point</option>
                    <option value="LineString">LineString</option>
                    <option value="Polygon">Polygon</option>
                </select>
            </p>
            <button class="edit save" @click="interaction">Удалить объект</button>
            <!-- <form @submit.prevent="onSubmit">
                <ul>
                    <li v-for="(f, index) in feature_.properties" :key="f.number_support">

                        <p v-if="typeof (f) === 'boolean'">
                            <span>{{ index }}</span>
                            <input v-model="feature_.properties[index]" type="checkbox"
                                placeholder="MAX_OOP" value="cockowin.danil@gmail.com" step="any">
                        </p>
                        <p v-else>
                            <span>{{ index }}</span>
                            <input v-model="feature_.properties[index]" :type="typeof (f) === 'string' ? 'text' : 'number'"
                                placeholder="MAX_OOP" value="cockowin.danil@gmail.com" step="any">
                        </p>
                    </li>
                </ul> -->
                <div style="display: flex;">
                    <button class="edit save" type="submit">Создать</button>
                    <a class="edit save" @click="close('add')">Закрыть</a>
                </div>
            <!-- </form> -->
        </div>
    </transition>
</template>

<script>
//import { mapActions } from 'vuex'

export default {
    components: {
    },
    name: 'AddGeometryObject',
    props: ['drawType', 'showAdd', 'close', 'interaction', 'clearDrawLayer'],
    data () {
        return {
            draw: this.drawType,
        };
    },
};
</script>

<style>
input {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #aaa;
    transition: .3s border-color;
    outline: none;
}

select {
    border: 1px solid black;
    padding: 2px 3px;
}

input:active {
    border: 1px solid #EF5350;
}

input:focus {
    border: 1px solid #EF5350;
    box-shadow: 0 0 10px rgba(239, 83, 80, 0.5);
}
</style>
