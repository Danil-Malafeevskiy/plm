<template>
    <transition name="animation">
        <div class="add_window" v-if="showAdd">
            <v-alert class="error_window" style="display: none; color: white;" type="error" :icon="icon">Ошибка!</v-alert>
            <v-alert class="success_window" style="display: none; color: white;" type="success">Объект успешно создан!</v-alert>
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
            <form @submit.prevent="onSubmit">
                <div class="add_form" v-for="(f, index) in feature_.properties" :key="f.number_support">
                    <p v-if="typeof (f) === 'boolean'">
                        <span>{{ index }}</span>
                        <input v-model="feature_.properties[index]" type="checkbox" placeholder="MAX_OOP"
                            value="cockowin.danil@gmail.com" step="any">
                    </p>
                    <p v-else-if="index != 'id' && index != 'dolgota' && index != 'shirota'">
                        <span>{{ index }}</span>
                        <input v-model="feature_.properties[index]" :type="typeof (f) === 'string' ? 'text' : 'number'"
                            placeholder="MAX_OOP" value="cockowin.danil@gmail.com" step="any">
                    </p>
                </div>
                <div style="display: flex;">
                    <button class="edit save" type="submit">Создать</button>
                    <a class="edit save" @click="close('add')">Закрыть</a>
                </div>
            </form>
        </div>
    </transition>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { toLonLat } from 'ol/proj';
import { mdiAlertCircleOutline } from '@mdi/js';

export default {
    components: {
    },
    name: 'AddGeometryObject',
    props: ['drawType', 'showAdd', 'close', 'interaction', 'clearDrawLayer', 'feature', 'coord'],
    data() {
        return {
            draw: this.drawType,
            test: null,
            cord: this.coord,
            feature_: {
                type: 'Feature',
                properties: {},
                geometry: {},
            },
            icon: mdiAlertCircleOutline 
        };
    },
    watch: {
        feature: function () {
            for (let key in this.feature) {
                if (key === 'properties') {
                    for (let key1 in this.feature[key]) {
                        if (key1 != 'id') {
                            if (typeof (this.feature[key][key1]) === 'string')
                                this.feature_[key][key1] = "";
                            else if (typeof (this.feature[key][key1]) === 'number')
                                this.feature_[key][key1] = 1;
                            else if (typeof (this.feature[key][key1]) === 'boolean')
                                this.feature_[key][key1] = false;
                        }
                    }
                }
            }
            this.test = this.feature;
        },
    },
    computed: mapGetters(['getResultPost']),
    methods: {
        ...mapActions(['postFeature']),
        async onSubmit() {
            this.feature_.geometry = {
                type: this.draw.data,
                coordinates: toLonLat(this.cord.data)
            }
            this.feature_.properties.shirota = this.feature_.geometry.coordinates[1];
            this.feature_.properties.dolgota = this.feature_.geometry.coordinates[0];
            console.log(this.feature_);
            await this.postFeature(JSON.stringify([this.feature_]));
            if(this.getResultPost){
                document.querySelector('.error_window').style.display = "none";
                document.querySelector('.success_window').style.display = "block";
            }
            else{
                document.querySelector('.error_window').style.display = "block";
                document.querySelector('.success_window').style.display = "none";
            }
        },
    }
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
