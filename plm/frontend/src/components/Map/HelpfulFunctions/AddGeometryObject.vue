<!-- eslint-disable vue/no-mutating-props -->
<template>
    <div class="add_window" style="display: none" >
        Добавление <br>
        <p v-if="this.cord[0] === this.cord[0]"> Координата: {{this.cord[0]}}  {{this.cord[0]}} </p> 
            <ValidationObserver v-slot="{ invalid }">
                <form @submit.prevent="onSubmit">
                    <ValidationProvider name="VL" rules="required|alpha_dash|alpha_spaces" v-slot="{ errors }">
                        <input v-model="VL" type="text" placeholder="MAX_OOP" value="cockowin.danil@gmail.com">
                        <span>{{ errors[0] }}</span>
                    </ValidationProvider>

                    <ValidationProvider name="type_support" rules="required|alpha" v-slot="{ errors }">
                        <input v-model="type_support" type="text" placeholder="First Mom">
                        <span>{{ errors[0] }}</span>
                    </ValidationProvider>

                    <ValidationProvider name="code_support" rules="required|alpha_dash" v-slot="{ errors }">
                        <input v-model="code_support" type="text">
                        <span>{{ errors[0] }}</span>
                    </ValidationProvider>
                    <ValidationProvider name="material" rules="required|alpha" v-slot="{ errors }">
                        <input v-model="material" type="text">
                        <span>{{ errors[0] }}</span>
                    </ValidationProvider>
                    <ValidationProvider name="corner" rules="required|decimal" v-slot="{ errors }">
                        <input v-model="corner" type="number" step="any">
                        <span>{{ errors[0] }}</span>
                    </ValidationProvider>
                    <ValidationProvider name="height" rules="required|decimal" v-slot="{ errors }">
                        <input v-model="height" type="number" step="any">
                        <span>{{ errors[0] }}</span>
                    </ValidationProvider>

                    <button class="edit save" type="submit" :disabled="invalid">Submit</button>
                </form>
            </ValidationObserver>
        <button class="edit save" @click="close('.add_window')">Закрыть</button>

        <select v-model="drawType">
            <option value="Point">Point</option>
            <option value="LineString">LineString</option>
            <option value="Polygon">Polygon</option>
        </select>

    </div>
</template>

<script>
import { ValidationProvider, ValidationObserver } from 'vee-validate';

export default {
    components: {
        ValidationProvider,
        ValidationObserver
    },
    name: 'AddGeometryObject',
    props: ['close', 'cord', 'drawType'],
    data: function() {
        return {
            id: null,
            number_support: null,
            VL: null,
            type_support: null,
            code_support: null,
            material: null,
            corner: null,
            height: null,
        };
    },

    methods: {
        onSubmit() {
            console.log(JSON.stringify({
                id: this.id,
                number_support: this.number_support,
                VL: this.VL,
                type_support: this.type_support,
                code_support: this.code_support,
                material: this.material,
                corner: this.corner,
                height: this.height,
            }));
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

input:hover {
    border: 1px solid #111;
}
</style>
