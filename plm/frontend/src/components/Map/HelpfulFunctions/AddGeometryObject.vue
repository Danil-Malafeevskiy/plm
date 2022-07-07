<template>
    <div class="add_window" style="display: none" >
        Добавление <br>
        
        <p>Выбери своего бойца
        <select v-model="draw" @change="updateValue($event.target.value)">
            <option value="Point">Point</option>
            <option value="LineString">LineString</option>
            <option value="Polygon">Polygon</option>
        </select></p>
        <p v-if="this.cord[0] === this.cord[0]"> Координата: {{this.cord[0]}}  {{this.cord[0]}} </p> 
        <ValidationObserver v-slot="{ invalid }">
            <form @submit.prevent="onSubmit">

                <ValidationProvider name="number_support" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.number_support" type="text" step="1" placeholder="number_support" >
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="VL" rules="required|alpha_dash|alpha_spaces" v-slot="{ errors }">
                    <input v-model="properties.VL" type="text" placeholder="VL" >
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

                <ValidationProvider name="type" rules="required|alpha_num" v-slot="{ errors }">
                    <input v-model="geometry.type" type="text" placeholder="type" >
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <button class="edit save" type="submit" :disabled="invalid">Submit</button>
            </form>
        </ValidationObserver>
        <button class="edit save" @click="close('.add_window')">Закрыть</button>
        <div style="font-size: 10px">
        <p>{{type}}</p>
        <p>{{properties}}</p>
        <p>{{geometry}}</p>
        <p>{{fuck}}</p>
        </div>
    </div>
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
    props: ['cord', 'drawType', 'close'],
    data: function() {
        return {
            fuck: this.cord,
            type: 'Feature',
            properties:{
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
            geometry:{
                type: '',
                coordinates: [ this.cord[1], this.cord[0]]
            },

            draw: this.drawType,
        };
    },
    watch: {
        cord: function () {
            this.properties.shirota = this.cord[0];
            this.properties.dolgota = this.cord[1];
            this.geometry.coordinates = [this.cord[1], this.cord[0]];
            this.fuck = this.cord;
        },
    },
    
    methods: {
        onSubmit() {
            axios.post('/tower', {
                type: this.type,               
                properties: this.properties,
                geometry: this.geometry,
            }).then((response) => console.log(response.data));
            
        },
        updateValue: function (drawType) {
            this.$emit('input', drawType);
    }
    },
    computed: {
        propModel: {
            get () { return this.prop },
            set (value) { this.$emit('update:prop', value) },
  },

},

};
</script>

<style>

.add_window{
    width: 20em;
}

input {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #aaa;
    transition: .3s border-color;
}

select{
    border: 1px solid black;
}

input:hover {
    border: 1px solid #111;
}
</style>
