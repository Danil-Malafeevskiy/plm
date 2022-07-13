<template>
    <transition name="animation">
        <div class="edit_window" v-if="showEdit">
        <v-alert class="error_window" style="display: none; color: white;" type="error" :icon="icon">Ошибка!</v-alert>
            <v-alert class="success_window" style="display: none; color: white;" type="success">Изменения сохранены</v-alert>
            <p style="font-size: 32px;">Редактирование</p>
            <form @submit.prevent="onSubmit">
                <div class="edit_from" v-for="(f, index) in feature_.properties" :key="f.number_support">
                    <p v-if="typeof (f) === 'boolean'">
                        <span>{{ index }}</span>
                        <input v-model="feature_.properties[index]" type="checkbox" step="any">
                    </p>
                    <p v-else-if="index != 'id'">
                        <span>{{ index }}</span>
                        <input v-model="feature_.properties[index]" :type="typeof (f) === 'string' ? 'text' : 'number'"
                            step="any">
                    </p>
                </div>
                <div style="display: flex;">
                    <button class="edit save" type="submit">Применить</button>
                    <a class="edit save" @click="close('.edit_window')">Закрыть</a>
                </div>
            </form>
        </div>
    </transition>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { mdiAlertCircleOutline } from '@mdi/js';

export default {
    components: {
    },
    name: 'AddGeometryObject',
    props: ['feature', 'close', 'showEdit'],
    data() {
        return {
            feature_: this.feature,
            icon: mdiAlertCircleOutline 
        }
    },
    watch: {
        feature: function () {
            this.feature_ = this.feature;
        }
    },
    computed: mapGetters(['getResultPut']),
    methods: {
        ...mapActions(['putFeature']),
        async onSubmit() {
            await this.putFeature(this.feature_);
            if(this.putFeature){
                document.querySelector('.error_window').style.display = "none";
                document.querySelector('.success_window').style.display = "block";
            }
            else{
                document.querySelector('.error_window').style.display = "block";
                document.querySelector('.success_window').style.display = "none";
            }
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
