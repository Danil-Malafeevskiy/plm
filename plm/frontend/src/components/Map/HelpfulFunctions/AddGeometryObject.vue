<template>
<transition name="animation">
    <div class="add_window" v-if="showAdd">
        <p style="font-size: 32px;">Добавление объекта</p>
        <p>Выбор объекта для выделения
            <select v-model="draw" @change="updateValue($event.target.value)">
                <option selected value="Point">Point</option>
                <option value="LineString">LineString</option>
                <option value="Polygon">Polygon</option>
            </select>
        </p>
        <p v-if="this.cord[0] === this.cord[0]"> Координата: {{ this.cord[1] }} {{ this.cord[0] }} </p>
        <ValidationObserver v-slot="{ invalid }" class="slow">
            <form @submit.prevent="onSubmit">

                <ValidationProvider name="number_support" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.number_support" type="text" step="1" placeholder="number_support">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="VL" rules="required|alpha_dash|alpha_spaces" v-slot="{ errors }">
                    <input v-model="properties.VL" type="text" placeholder="VL">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="type_support" rules="required|alpha" v-slot="{ errors }">
                    <input v-model="properties.type_support" type="text" placeholder="type_support">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="code_support" rules="required|alpha_dash" v-slot="{ errors }">
                    <input v-model="properties.code_support" type="text" placeholder="code_support">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="material" rules="required|alpha" v-slot="{ errors }">
                    <input v-model="properties.material" type="text" placeholder="material">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="corner" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.corner" type="number" step="any" placeholder="corner">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="X" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.X" type="number" step="any" placeholder="X">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="Y" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.Y" type="number" step="any" placeholder="Y">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="Z" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.Z" type="number" step="any" placeholder="Z">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="height" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.height" type="number" step="any" placeholder="height">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="flag_defects" rules="required|alpha_num" v-slot="{ errors }">
                    <input v-model="properties.flag_defects" type="number" placeholder="flag_defects">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>
                <div>
                    <button class="edit save" type="submit" :disabled="invalid">Создать</button>
                    <a type="button" class="edit save" @click="close('add')">Закрыть</a>
                </div>
            </form>
        </ValidationObserver>
    </div>
   </transition>
</template>

<script>
import { ValidationProvider, ValidationObserver } from 'vee-validate';
import axios from 'axios';


export default {
    components: {
        ValidationProvider,
        ValidationObserver
    },
    name: 'AddGeometryObject',
    props: ['drawType', 'showAdd', 'cord', 'close'],
    data: function () {
        return {
            draw: "Point",
            type: 'Feature',
            properties: {
                name_tap: '',
                number_support: 1,
                VL: '',
                type_support: '',
                code_support: '',
                material: '',
                corner: '',
                X: 1,
                Y: 1,
                Z: 1,
                shirota: this.cord[0],
                dolgota: this.cord[1],
                height: 1,
                TPV_photo: '',
                UF_photo: '',
                v_defects: '',
                u_defects: '',
                code_support_in_1C: '',
                guid: '',
                flag_defects: 1,
                comment_in_TOiR: '',
            },
            geometry: {
                type: "Point",
                coordinates: [this.cord[1], this.cord[0]]
            },
        };
    },
    watch: {
        cord: function () {
            this.properties.shirota = this.cord[0];
            this.properties.dolgota = this.cord[1];
            this.geometry.coordinates = [this.cord[0], this.cord[1]]
        },
        draw: function () {
            this.geometry.type = this.draw;
        }
    },

    methods: {
        onSubmit() {
            axios.post('/tower', {
                type: this.type,
                properties: this.properties,
                geometry: this.geometry,
            }).then((response) => console.log(response.data));
            window.parent.location = window.parent.location.href;
        },
        updateValue: function (drawType) {
            this.$emit('input', drawType);
        },
    },
    computed: {
        propModel: {
            get() { return this.prop },
            set(value) { this.$emit('update:prop', value) },
        },

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
}

input:active {
    border: 1px solid #EF5350;
}

input:focus {
    border: 1px solid #EF5350;
    box-shadow: 0 0 10px rgba(239, 83, 80, 0.5);
}
</style>
