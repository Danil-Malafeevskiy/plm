<template>
    <transition name="animation">
        <div class="edit_window" v-if="showEdit">
            Редактирование
            <!-- <ValidationObserver v-slot="{ invalid }"> -->
            <form @submit.prevent="onSubmit">
                <ul>
                    <li v-for="(f, index) in feature_.properties" :key="f.number_support">

                        <p v-if="typeof (f) === 'boolean'">
                            <span>{{ index }}</span>
                            <input v-model="feature_.properties[index]" type="checkbox"
                                placeholder="MAX_OOP" value="cockowin.danil@gmail.com" step="any">
                        </p>
                        <p v-else-if="index != 'geometry'">
                            <span>{{ index }}</span>
                            <input v-model="feature_.properties[index]" :type="typeof (f) === 'string' ? 'text' : 'number'"
                                placeholder="MAX_OOP" value="cockowin.danil@gmail.com" step="any">
                        </p>
                    </li>
                </ul>

                <!-- <ValidationProvider name="VL" rules="required|alpha_dash|alpha_spaces" v-slot="{ errors }">
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
                </ValidationProvider> -->
                <div style="display: flex;">
                    <button class="edit save" type="submit">Применить</button>
                    <a class="edit save" @click="close('.edit_window')">Закрыть</a>
                </div>
            </form>
            <!--</ValidationObserver>-->

        </div>
    </transition>
</template>

<script>
//import { ValidationProvider, ValidationObserver } from 'vee-validate';
import { mapActions } from 'vuex'

export default {
    components: {
        //ValidationProvider,
        //ValidationObserver
    },
    name: 'AddGeometryObject',
    props: ['feature', 'close', 'showEdit'],
    data() {
        return {
            feature_: this.feature,
        }
    },
    watch: {
        feature: function () {
            this.feature_ = this.feature;
        }
    },
    methods: {
        ...mapActions(['putFeature']),
        onSubmit() {
            this.putFeature(this.feature_);
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
