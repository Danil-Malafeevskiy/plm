<template>
    <transition name="animation">
        <div class="edit_window" v-if="showEdit">
            Редактирование
            <form @submit.prevent="onSubmit">
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
                </ul>
                <div style="display: flex;">
                    <button class="edit save" type="submit">Применить</button>
                    <a class="edit save" @click="close('.edit_window')">Закрыть</a>
                </div>
            </form>
        </div>
    </transition>
</template>

<script>
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
