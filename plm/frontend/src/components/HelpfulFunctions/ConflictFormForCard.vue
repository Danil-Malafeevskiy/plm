<template>
    <div style="overflow-y: hidden; overflow-x: hidden; height: 100%">
        <v-card-text class="pa-0">
            <v-form v-if="objectForConflict_" class="conflict_form">
                <div style="display: flex">
                    <v-card-text style="font-size: 16px; color: #787878; font-weight: 500; padding: 16px 24px;">
                        Версия в системе
                    </v-card-text>
                    <v-card-text style="font-size: 16px; color: #787878; font-weight: 500; padding: 16px 30px;">
                        Новая версия
                    </v-card-text>
                </div>
                <v-row justify="space-between" style="padding-bottom: 0 !important;">
                    <template v-for="el in typeForFeature.headers">
                        <v-col :key="`origin-element-${el.text}`" cols="3" sm="6" md="5" lg="6" v-if="el.text != 'id'">
                            <v-text-field v-if="objectForConflict_"
                                :class="{ 'blue_field': !checkEqualityOfFieads(el.text) }"
                                :value="objectForConflict_.properties[el.text]" hide-details :label="el.text"
                                :placeholder="el.text" filled disabled>
                            </v-text-field>
                        </v-col>
                        <v-btn v-if="!checkEqualityOfFieads(el.text) && el.text != 'id'" small icon
                            :key="`change-field-button-${el.text}`" @click="changeItem(el.text)" style="
                                        max-height: 100% !important;
                                        margin: auto 0 !important;
                                    ">
                            <v-icon v-if="notConflictObject.properties[el.text] === objectForCard.properties[el.text]">
                                mdi-arrow-right</v-icon>
                            <v-icon v-else>mdi-arrow-left</v-icon>
                        </v-btn>
                        <v-col v-if="notConflictObject && el.text != 'id'" :key="`new-element-${el.text}`" cols="3" sm="6"
                            md="5" lg="6" v-show="el != 'id'">
                            <v-text-field :class="{ 'blue_field': !checkEqualityOfFieads(el.text) }"
                                :value="notConflictObject.properties[el.text]" hide-details :label="el.text"
                                :placeholder="el.text" filled readonly>
                            </v-text-field>
                        </v-col>
                    </template>
                </v-row>

                <FormForDynamicField :objectForCard="notConflictObject" :infoCardOn="{ data: true }"
                    :checkEqualityOfFieads="checkEqualityOfFieads" :conflictCard="conflictCard"
                    :objectForConflict="objectForConflict" :changeItem="changeItem"
                    :notConflictObject="objectForCard" />

                <v-row justify="space-between" style="padding: 0 24px !important;">
                    <v-col cols="3" sm="6" md="5" lg="6">
                        <v-card-text>Новая геометрия</v-card-text>
                    </v-col>
                    <v-btn v-if="(notConflictObject.geometry.coordinates !== objectForConflict.geometry.coordinates)" small icon @click="changeCoordinates()" style="
                                        max-height: 100% !important;
                                        margin: auto 0 !important;
                                    ">
                        <v-icon
                            v-if="'geometry' in objectForConflict && objectForCard.geometry.coordinates !== objectForConflict.geometry.coordinates">
                            mdi-arrow-right</v-icon>
                        <v-icon v-else>mdi-arrow-left</v-icon>
                    </v-btn>
                    <v-col cols="3" sm="6" md="5" lg="6">
                        <v-card-text>Текущая геометрия</v-card-text>
                    </v-col>
                </v-row>
            </v-form>
        </v-card-text>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import FormForDynamicField from './FormForDynamicField.vue';

export default {
    name: 'ConflictFormForCard',
    components: {
        FormForDynamicField,
    },
    props: ['objectForCard_', 'conflictCard', 'objectForConflict'],
    data() {
        return {
            objectForCard: this.objectForCard_,
            objectForConflict_: this.objectForConflict,
            notConflictObject: JSON.parse(JSON.stringify(this.objectForCard_)),
        }
    },
    watch: {
        objectForCard_() {
            this.objectForCard = this.objectForCard_;
            this.notConflictObject = JSON.parse(JSON.stringify(this.objectForCard_))
        },
        objectForConflict() {
            this.objectForConflict_ = this.objectForConflict;
        }
    },
    computed: {
        ...mapGetters(['typeForFeature', 'newData', 'arrayEdit']),
    },
    methods: {
        // ...mapMutations(['updateObjectForCard']),
        checkEqualityOfFieads(field) {
            if (this.newData.length) {
                try {
                    let newPutObject = this.newData.filter(el => el.id === this.objectForCard.id)[0];
                    if (newPutObject != undefined) {
                        let oldPutObject = this.arrayEdit.put.filter(el => el.id === this.objectForCard.id)[0];
                        return newPutObject.properties[field] === oldPutObject.properties[field];
                    }
                    return true;
                }
                catch (error) {
                    console.log(error, field);
                }
            }
            return true;
        },
        changeCoordinates() {
            if (this.objectForCard.geometry !== this.objectForConflict_.geometry) {
                this.objectForCard.geometry = this.objectForConflict_.geometry;
            }
            else {
                this.objectForCard.geometry = this.notConflictObject.geometry;
            }
        },
        changeItem(field) {
            if (this.notConflictObject.properties[field] === this.objectForCard.properties[field]) {
                this.objectForCard.properties[field] = this.objectForConflict_.properties[field];
            }
            else {
                this.objectForCard.properties[field] = this.notConflictObject.properties[field];
            }
        },
    },
}
</script>

<style scoped>
#permission {
    margin-top: 0 !important;
    margin-left: 1em !important;
}

.conflict_form {
    position: absolute !important;
    top: 30% !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 70px !important;
    z-index: 2;
    overflow: hidden scroll;
}

.v-expansion-panel-content__wrap {
    padding: 0 !important;
}

.v-application--is-ltr .v-expansion-panel-header__icon {
    margin-left: 0 !important;
}

.show__card {
    margin-right: 8px;
    border-radius: 8px !important;
}

.v-window__container {
    min-height: 100%;
}

.btn {
    background-color: white !important;
}

.btn_disabled {
    opacity: 0.5;
}

.card__info {
    align-items: center;
}

.card__window {
    display: flex !important;
    flex-direction: column !important;
    position: absolute;
    top: 0;
    bottom: 0;
    min-width: 100%;
    max-width: 100%;
    border-radius: 12px;
}

.card__img {
    align-items: flex-start;
}

.v-icon--link::after {
    background-color: rgba(255, 255, 255, 0) !important;
}

.background_color_red {
    background-color: #EE5E5E !important;
    max-height: 22.48% !important;
    min-height: 22.48% !important;
    border-radius: 12px 12px 0 0;
}

.background_color_gray {
    background-color: #DDDDDD !important;
}

.btn_del_img {
    position: absolute;
    z-index: 2;
    right: 0;
}

.one_picture {
    position: relative !important;
    max-height: 22.48% !important;
    border-radius: 12px 12px 0 0 !important;
}

.conflict_pictures {
    display: flex;
    justify-content: space-between;
    background-color: #C9C8ED;
    padding: 34px 50px;
    border-radius: 12px 12px 0 0;
    max-height: 22.48%;
}

.two_pictures {
    max-width: 42% !important;
    border-radius: 4px;
}

.two_background_color_red {
    background-color: #EE5E5E !important;
    max-width: 42% !important;
    border-radius: 4px;
}

.row {
    padding: 24px 24px 12px 24px !important;
}

.card_from_block {
    height: 100%;
}

.v-icon::after {
    background-color: none !important;
}

.col-sm-6 {
    width: 46%;
    max-width: 46%;
    flex-basis: 46%;
}

.v-window {
    height: 100% !important;
}

@media (min-width: 1025px) and (max-width: 1919px) {
    .col-sm-6 {
        width: 45%;
        max-width: 45%;
        flex-basis: 45%;
    }
}
</style>

<style>
.v-input__icon,
.v-icon--link {
    min-width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    justify-content: center !important;
    align-items: center !important;
}

.blue_field {
    background-color: #C9C8ED !important;
    color: #0F0CA7 !important;
}
</style>