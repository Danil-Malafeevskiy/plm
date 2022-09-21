<template>
    <v-row justify="start">
        <template v-if="'properties' in objectForCard && 'type' in objectForCard.properties">
            <p class="attributes ma-0">Основные атрибуты</p>
                    <v-col v-for="(el, index) in objectForCard.properties.headers" :key="index" cols="2" sm="6" md="5"
                    lg="6" v-show="el.text != 'id'">
                    <v-text-field v-model="objectForCard_.properties.headers[index].text" :label="el.text"
                        :placeholder="el.text" filled :readonly="infoCardOn.data" :rules="[rules.required, rules.main]"
                        @input="textToValue(index)" append-icon="mdi-delete-outline"
                        @click:append="deleteMainAttribute(index)">
                    </v-text-field>
                </v-col>
            <v-col cols="2" sm="6" md="5" lg="6">
                <v-btn class="ma-0 pa-0 btn_on_card" :disabled="infoCardOn.data" width="100%" depressed color="#EE5E5E"
                    @click="addMainAttribute">
                    <v-icon color="white" dark>
                        mdi-plus
                    </v-icon>
                </v-btn>
            </v-col>
        </template>
        <template v-if="'properties' in objectForCard && 'type' in objectForCard.properties">
            <p class="attributes ma-0">Допольнительные атрибуты</p>
            <v-col v-for="(el, index) in objectForCard.properties.properties"
                :key="objectForCard.properties.headers.length + index" cols="2" sm="6" md="5" lg="6"
                v-show="el != 'id'">
                <v-text-field v-model="objectForCard_.properties.properties[index]" :label="el" :placeholder="el" filled
                    :readonly="infoCardOn.data" append-icon="mdi-delete-outline"
                    @click:append="deleteAdditionalAttribute(index)" :rules="[rules.required]">
                </v-text-field>
            </v-col>
            <v-col cols="2" sm="6" md="5" lg="6">
                <v-btn class="ma-0 pa-0 btn_on_card" :disabled="infoCardOn.data" width="100%" depressed color="#EE5E5E"
                    @click="addAdditionalAttribute">
                    <v-icon color="white" dark>
                        mdi-plus
                    </v-icon>
                </v-btn>
            </v-col>
        </template>
        <template v-if="'name' in objectForCard">
            <p v-if="typeForFeature.properties.length" class="attributes ma-0">Допольнительные атрибуты
            </p>
            <v-col v-for="el in typeForFeature.properties" :key="el" cols="2" sm="6" md="5" lg="6" v-show="el != 'id'">
                <v-text-field v-if="checkEqualityOfFieads(el)" v-model="objectForCard_.properties[el]" hide-details
                    :label="el" :placeholder="el" filled :readonly="infoCardOn.data">
                </v-text-field>
                <v-text-field v-else v-model="objectForCard_.properties[el]" background-color="#C9C8ED" color="#0F0CA7"
                    hide-details :label="el" :placeholder="el" filled :readonly="infoCardOn.data"
                    append-icon="mdi-progress-question" @click:append="changeConflictField(el)">
                </v-text-field>
            </v-col>
        </template>
    </v-row>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'FormForDynamicField',
    props: ['objectForCard', 'infoCardOn', 'checkEqualityOfFieads', 'changeConflictField'],
    data() {
        return {
            objectForCard_: this.objectForCard,
            rules: {
                required: el => this.checkDoubleFields(el) || 'Одинаковые имена атрибутов',
                main: el => !!el || 'Обяательный атрибут'
            },
        }
    },
    watch: {
        objectForCard: {
            handler() {
                this.objectForCard_ = this.objectForCard;
            }
        }
    },
    computed: mapGetters(['typeForFeature', 'allListItem']),
    methods: {
        addMainAttribute() {
            this.objectForCard_.properties.headers.push({ text: '', value: '' });
        },
        textToValue(index) {
            this.objectForCard_.properties.headers[index].value = this.objectForCard_.properties.headers[index].text;
        },
        addAdditionalAttribute() {
            this.objectForCard_.properties.properties.push('');
        },
        deleteMainAttribute(index_) {
            if (!this.infoCardOn.data) {
                this.objectForCard_.properties.headers = this.objectForCard_.properties.headers.filter((el, index) => index != index_);
            }
        },
        deleteAdditionalAttribute(index_) {
            if (!this.infoCardOn.data) {
                this.objectForCard_.properties.properties = this.objectForCard_.properties.properties.filter((el, index) => index != index_);
            }
        },
        checkDoubleFields(element) {
            if (element != undefined) {
                let arrayOfFields = [...this.objectForCard.properties.headers.filter(el => el.text.trim() === element.trim())];
                arrayOfFields = [...arrayOfFields, ...this.objectForCard.properties.properties.filter(el => el.trim() === element.trim())];
                return arrayOfFields.length === 1 || !arrayOfFields.length;
            }
        }
    }
}
</script>

<style>
.attributes {
    font-size: 16px;
    width: 100%;
    padding-left: 12px;
    color: #787878;
}

.btn_on_card {
    height: 50px !important;
    border-radius: 8px !important;
}
</style>