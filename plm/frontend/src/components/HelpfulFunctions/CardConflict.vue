<template>
    <v-scroll-x-reverse-transition>
        <v-card class="card_of_object_1" v-if="conflictCard === true">
            <div class="card__window">
                <p style="display: none">{{ objectForCard }}</p>
                <v-card
                    v-if="'properties' in objectForCard && 'type' in objectForCard.properties && objectForCard.properties.type === 'Point'"
                    class="one_picture pa-0 ma-0 background_color_gray" tile flat
                    style="width: 100% !important; height: 59.45% !important; overflow-y: scroll !important;">

                    <v-row no-gutters justify="start">
                        <v-col v-for="(el, index) in listMdiIcons" :key="index" md="3" lg="4"
                            style="max-width: 48px !important" class="ma-0">
                            <v-radio-group hide-details class="pa-0 ma-0" v-model="objectForCard.image">
                                <v-radio :value="el" readonly class="ma-2" color="#E93030"
                                    :on-icon="el" :off-icon="el" style="
                                    min-height: 2em !important; 
                                    min-width: 2em !important;
                                "></v-radio>
                            </v-radio-group>
                        </v-col>
                    </v-row>
                </v-card>
                <v-file-input v-else-if="'properties' in objectForCard && 'type' in objectForCard.properties"
                    accept="image/*" class="pa-0 ma-0 background_color_red" height="37.53%" :prepend-icon="icon"
                    disabled hide-input>
                </v-file-input>

                <v-file-input v-else-if="!objectForCard.image" accept="image/*" :class="{
                    'background_color_red': !('properties' in objectForCard && 'username' in objectForCard.properties),
                    'background_color_gray': ('properties' in objectForCard && 'username' in objectForCard.properties)
                }" class="pa-0 ma-0" height="37.53%" :prepend-icon="icon" disabled hide-input>
                </v-file-input>

                <template v-if="!('properties' in objectForCard && 'type' in objectForCard.properties)">
                    <v-img v-if="objectForCard.image" :src="objectForCard.image" class="one_picture" width="100%" height="37.53%"></v-img>
                </template>

                <div style="overflow-y: scroll; overflow-x: hidden; height: 100%">
                    <v-card-text class="pa-0">
                        <v-form>
                            <v-row justify="start" style="padding-bottom: 0 !important;">
                                <v-col cols="2" sm="6" md="5" lg="6">
                                    <v-card-text style="font-size: 24px; padding: 16px 0;">Оригинал
                                    </v-card-text>
                                </v-col>
                                <v-col v-for="el in typeForFeature.headers" :key="el.text" cols="2" sm="6" md="5" lg="6"
                                    v-show="el.text != 'id'">
                                    <v-text-field v-if="el.text != 'id' && checkEqualityOfFieads(el.text)"
                                        v-model="objectForCard.properties[el.text]" hide-details :label="el.text"
                                        :placeholder="el.text" filled readonly>
                                    </v-text-field>
                                    <v-text-field v-else-if="el.text != 'id'"
                                        v-model="objectForCard.properties[el.text]" background-color="#C9C8ED"
                                        color="#0F0CA7" hide-details :label="el.text" :placeholder="el.text" filled
                                        readonly append-icon="mdi-progress-question">
                                    </v-text-field>
                                </v-col>
                            </v-row>

                            <FormForDynamicField :objectForCard="objectForCard" :infoCardOn="{data: true}"
                                :checkEqualityOfFieads="checkEqualityOfFieads" />

                            <ExpansionPanelForCard :objectForCard="objectForCard" :infoCardOn="{data: true}" />
                            <v-snackbar v-model="snackbar" timeout="2000" color="red accent-2">
                                Не может быть атрибутов с одинаковыми именами
                            </v-snackbar>
                        </v-form>
                    </v-card-text>
                </div>
            </div>
        </v-card>
    </v-scroll-x-reverse-transition>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket } from '@mdi/js'
import ExpansionPanelForCard from './ExpansionPanelForCard.vue'
import FormForDynamicField from './FormForDynamicField.vue';

export default {
    name: 'CardConflict',
    components: {
        ExpansionPanelForCard,
        FormForDynamicField,
    },
    props: ['cardVisable', 'conflictCard', 'editMode', 'objectForCard_'],
    data() {
        return {
            cardVisable_: this.cardVisable,
            icon: mdiImagePlusOutline,
            showPassword: false,
            listMdiIcons: [mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket],
            listSelectedIcons: [],
            isOldItem: false,
            snackbar: false,
            objectForCard: this.objectForCard_
        }
    },
    watch: {
        cardVisable: {
            handler() {
                this.cardVisable_ = this.cardVisable;
                if (this.cardVisable_.data) {
                    setTimeout(() => {
                        let card = document.querySelector('.card_of_object_1');
                        if (card != undefined) {
                            card.style.cssText = 'width: 38.05% !important;';
                        }
                    });
                }
            }, deep: true
        },
        objectForCard_: function(){
            this.objectForCard = this.objectForCard_;
        }
    },
    computed: {
        ...mapGetters(['getObjectForCard', 'emptyObject', 'oneType', 'typeForFeature', 'arrayEditMode', 'newData', 'actions', 'user']),
    },
    methods: {
        ...mapActions(['getOneTypeObjectForFeature']),
        ...mapMutations(['updateOneType', 'updateObjectForCard']),
        changeItem(isOldItem) {
            let newPutobject;
            if (isOldItem) {
                newPutobject = this.newData.filter(el => el.id === this.objectForCard.id);
            }
            else {
                newPutobject = this.arrayEditMode.put.filter(el => el.id === this.objectForCard.id);
            }

            this.updateObjectForCard(JSON.parse(JSON.stringify(newPutobject[0])));
        },
        checkEqualityOfFieads(field) {
            if (this.newData.length) {
                try {
                    let newPutObject = this.newData.filter(el => el.id === this.objectForCard.id)[0];
                    if (newPutObject != undefined) {
                        let oldPutObject = this.arrayEditMode.put.filter(el => el.id === this.objectForCard.id)[0];
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
        checkDoubleFields(type) {
            let arrayOfFeilds = [];
            for (let i in type.headers) {
                arrayOfFeilds.push(type.headers[i].text.trim());
            }
            for (let i in type.properties) {
                arrayOfFeilds.push(type.properties[i].trim());
            }
            arrayOfFeilds = [...new Set(arrayOfFeilds)];
            if (arrayOfFeilds.length != type.headers.length + type.properties.length) {
                return true;
            }
            return false;
        }

    },
    mounted() {

    }
}
</script>

<style scoped>
#permission {
    margin-top: 0 !important;
    margin-left: 1em !important;
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

.card_of_object_1 {
    z-index: 1 !important;
    width: 38.05% !important;
    min-height: 92.08% !important;
    position: absolute !important;
    left: 21.28% !important;
    top: 4.19% !important;
    border-radius: 12px !important;
}

.card__info {
    align-items: center;
}

.card__footer {
    display: flex;
    bottom: 0px;
    justify-content: flex-end;
    border-top: 1px solid #E0E0E0;
    border-radius: 0 0 12px 12px !important;
    background-color: white;
}

.v-icon--link .v-icon__svg {
    min-width: 133.33px !important;
    min-height: 133.33px !important;
    fill: #FFFFFF !important;
}

.card__window {
    position: absolute;
    top: 0;
    bottom: 0;
    min-width: 100%;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 12px;
}

.card__img {
    align-items: flex-start;
}

.v-icon--link::after {
    background-color: rgba(255, 255, 255, 0) !important;
}

.v-file-input {
    min-height: 37.53%;
    max-height: 37.53%;
    border-radius: 12px 12px 0 0;
}

.background_color_red {
    background-color: #EE5E5E !important;
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
    border-radius: 12px 12px 0 0 !important;
}

.not_one_picture {
    position: absolute !important;
    border-radius: 12px 12px 0 0 !important;
}

.background_img {
    z-index: 1;
    background-color: #000;
    opacity: 0.3;
    min-height: 37.53%;
    max-height: 37.53%;
    border-radius: 12px 12px 0 0;
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
</style>