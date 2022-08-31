<template>
    <v-row justify="start">
        <template v-if="'properties' in objectForCard && 'type' in objectForCard.properties">
            <p class="attributes ma-0">Основные атрибуты</p>
            <v-col v-for="(el, index) in objectForCard.properties.headers" :key="index" cols="2" sm="6" md="5" lg="6"
                v-show="el.text != 'id'">
                <v-text-field v-model="objectForCard_.properties.headers[index].text" hide-details
                    :label="objectForCard.properties.headers[index].text"
                    :placeholder="objectForCard.properties.headers[index].text" filled :readonly="infoCardOn.data"
                    @input="textToValue(index)" append-icon="mdi-delete-outline"
                    @click:append="deleteMainAttribute(el.text)">
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

            <v-col v-for="(el, index) in objectForCard.properties.properties" :key="index" cols="2" sm="6" md="5" lg="6"
                v-show="el.text != 'id'">
                <v-text-field v-model="objectForCard_.properties.properties[index]" hide-details
                    :label="objectForCard.properties.properties[index]"
                    :placeholder="objectForCard.properties.properties[index]" filled :readonly="infoCardOn.data"
                    append-icon="mdi-delete-outline" @click:append="deleteAdditionalAttribute(el)">
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
            <v-col v-for="(el, index) in typeForFeature.properties" :key="index" cols="2" sm="6" md="5" lg="6"
                v-show="el.text != 'id'">
                <v-text-field v-model="objectForCard_.properties[el]" hide-details :label="el" :placeholder="el" filled
                    :readonly="infoCardOn.data">
                </v-text-field>
            </v-col>
        </template>
    </v-row>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'FormForDynamicField',
    props: ['objectForCard', 'infoCardOn'],
    data() {
        return {
            objectForCard_: this.objectForCard,
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
            this.objectForCard_.properties.headers.push({});
        },
        textToValue(index) {
            this.objectForCard_.properties.headers[index].value = this.objectForCard_.properties.headers[index].text;
        },
        addAdditionalAttribute() {
            this.objectForCard_.properties.properties.push('');
        },
        deleteMainAttribute(text) {
            if (!this.infoCardOn.data) {
                this.objectForCard_.properties.headers = this.objectForCard_.properties.headers.filter(el => el.text != text);
            }
        },
        deleteAdditionalAttribute(text) {
            if (!this.infoCardOn.data) {
                this.objectForCard_.properties.properties = this.objectForCard_.properties.properties.filter(el => el != text);
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