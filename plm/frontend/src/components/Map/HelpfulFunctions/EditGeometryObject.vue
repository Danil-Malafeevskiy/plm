<template>
<transition name="animation">
    <div class="edit_window" v-if="showEdit">
        Редактирование
        <ValidationObserver v-slot="{ invalid }">
            <form @submit.prevent="onSubmit">
                <ValidationProvider name="VL" rules="required|alpha_dash|alpha_spaces" v-slot="{ errors }">
                    <input v-model="properties.VL" type="text" placeholder="MAX_OOP" value="cockowin.danil@gmail.com">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="type_support" rules="required|alpha" v-slot="{ errors }">
                    <input v-model="properties.type_support" type="text" placeholder="First Mom">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>

                <ValidationProvider name="code_support" rules="required|alpha_dash" v-slot="{ errors }">
                    <input v-model="properties.code_support" type="text">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>
                <ValidationProvider name="material" rules="required|alpha" v-slot="{ errors }">
                    <input v-model="properties.material" type="text">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>
                <ValidationProvider name="corner" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.corner" type="number" step="any">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>
                <ValidationProvider name="height" rules="required|decimal" v-slot="{ errors }">
                    <input v-model="properties.height" type="number" step="any">
                    <span>{{ errors[0] }}</span>
                </ValidationProvider>
                <div style="display: flex;">
                    <button class="edit save" type="submit" :disabled="invalid">Применить</button>
                    <a class="edit save" @click="close('.edit_window')">Закрыть</a>
                </div>
            </form>
        </ValidationObserver>
        
    </div>
    </transition>
</template>

<script>
import { ValidationProvider, ValidationObserver } from 'vee-validate';
import { mapActions } from 'vuex'

export default {
    components: {
        ValidationProvider,
        ValidationObserver
    },
    name: 'AddGeometryObject',
    props: ['feature', 'close', 'showEdit'],
    data: function () {
        return {
            id: null,
            type: null,
            properties: {
                id: null,
                name_tap: null,
                number_support: null,
                VL: null,
                type_support: null,
                code_support: null,
                material: null,
                corner: null,
                X: null,
                Y: null,
                Z: null,
                shirota: null,
                dolgota: null,
                height: null,
                TPV_photo: null,
                UF_photo: null,
                v_defects: null,
                u_defects: null,
                code_support_in_1C: null,
                guid: null,
                flag_defects: null,
                comment_in_TOiR: null
            },
            geometry: {
                id: null,
                type: null,
                coordinates: []
            }
        };
    },

    watch: {
        feature: function () {
            this.id = this.feature.id;
            this.type = this.feature.type;
            this.properties = this.feature.properties;
            this.geometry = this.feature.geometry;
        }
    },

    methods: {
        ...mapActions(['putFeature']),
        onSubmit() {
            // axios.put('/tower', {
            //     id: this.id,
            //     type: this.type,
            //     properties: this.properties,
            //     geometry: this.geometry
            // }).then((response) => {
            //     console.log(response.data);
            // });
            // window.parent.location = window.parent.location.href;
            this.putFeature({id: this.id,
                 type: this.type,
                 properties: this.properties,
                 geometry: this.geometry});
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

}

input {
    border-radius: 10px;
    border: 1px solid #aaa;
    ;
    transition: .3s border-color;
}

input:hover {
    border: 1px solid #111;
}
</style>
