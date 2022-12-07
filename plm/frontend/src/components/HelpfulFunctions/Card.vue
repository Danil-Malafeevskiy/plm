<template>
    <v-scroll-x-reverse-transition>
        <v-card class="card_of_object" v-show="cardVisable_.data">
            <div class="card__window">
                <p style="display: none">{{ objectForCard }}</p>
                <v-card
                    v-if="'properties' in objectForCard && 'type' in objectForCard.properties && objectForCard.properties.type === 'Point'"
                    class="one_picture pa-0 ma-0 background_color_gray" tile flat
                    style="width: 100% !important; min-height: 37.53% !important; overflow-y: scroll !important;">

                    <v-row no-gutters justify="start">
                        <v-col v-for="(el, index) in listMdiIcons" :key="index" md="3" lg="4"
                            style="max-width: 48px !important" class="ma-0">
                            <v-radio-group hide-details class="pa-0 ma-0" v-model="objectForCard.image">
                                <v-radio :value="el" :readonly="infoCardOn.data" class="ma-2" color="#E93030"
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
                    :disabled="infoCardOn_.data" hide-input>
                </v-file-input>

                <v-file-input v-else-if="!objectForCard.image" @change="fileToBase64" accept="image/*" :class="{
                    'background_color_red': !('properties' in objectForCard && 'first_name' in objectForCard.properties),
                    'background_color_gray': ('properties' in objectForCard && 'first_name' in objectForCard.properties)
                }" class="pa-0 ma-0" height="37.53%" :prepend-icon="icon" :disabled="infoCardOn_.data" hide-input>
                </v-file-input>
                <template v-else-if="objectForCard.image && !infoCardOn_.data">
                    <div class="background_img"></div>
                    <v-btn class="btn_del_img ma-3 pa-0" elevation="0" icon @click="objectForCard.image = ''">
                        <v-icon color="white">
                            mdi-delete-outline
                        </v-icon>
                    </v-btn>
                </template>

                <template v-if="!('properties' in objectForCard && 'type' in objectForCard.properties)">
                    <v-img v-if="objectForCard.image" :src="objectForCard.image" :class="{
                        'one_picture': infoCardOn_.data,
                        'not_one_picture': !infoCardOn_.data,
                    }" width="100%" style="max-height: 37.53%"></v-img>
                </template>

                <StandartFormCard :objectForCard_="objectForCard" :infoCardOn="infoCardOn" :editCardOn="editCardOn" :editMode="editMode"
                                  :addCardOn="addCardOn_" @notVisableCard="notVisableCard" :cardVisable="cardVisable"/>

            </div>
        </v-card>
    </v-scroll-x-reverse-transition>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket } from '@mdi/js'
import StandartFormCard from './StandartFormCard.vue';

export default {
    name: 'CardInfo',
    components: {
        
        StandartFormCard,
    },
    props: ['cardVisable', 'addCardOn', 'infoCardOn', 'editCardOn', 'visableCard', 'notVisableCard', 'editMode'],
    data() {
        return {
            cardVisable_: this.cardVisable,
            addCardOn_: this.addCardOn,
            infoCardOn_: this.infoCardOn,
            editCardOn_: this.editCardOn,
            icon: mdiImagePlusOutline,
            objectForCard: {},
            showPassword: false,
            listMdiIcons: [mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket],
        }
    },
    watch: {
        cardVisable: {
            handler() {
                this.cardVisable_ = this.cardVisable;
            }, deep: true
        },
        addCardOn: {
            handler() {
                if (this.addCardOn.data) {
                    this.objectForCard = this.emptyObject;
                }
            },
            deep: true,
        },
        getObjectForCard: {
            handler() {
                this.objectForCard = this.getObjectForCard;
            },
            deep: true,
        },
        oneType: {
            handler() {
                let emptyObject = {
                    name: this.oneType.id,
                    type: 'Feature',
                    properties: {},
                    geometry: {
                        type: this.oneType.type,
                        coordinates: [],
                    }
                };
                for (const el in this.oneType.headers) {
                    emptyObject.properties[el.text] = '';
                }
                for (const el in this.oneType.properties) {
                    emptyObject.properties[el] = '';
                }
                this.upadateEmptyObject(emptyObject);
                if (this.addCardOn.data) {
                    this.objectForCard = this.emptyObject;
                    this.updateOneType({ type: this.oneType, forFeature: true });
                }
            }
        },
        objectForCard: {
            handler() {
                if ('name' in this.objectForCard && this.objectForCard.name != this.typeForFeature.id) {
                    this.getOneTypeObjectForFeature({ id: this.objectForCard.name, forFeature: true });
                }
                else if (this.typeForFeature.id != 0 && this.objectForCard.name != this.typeForFeature.id) {
                    const emptyType = {
                        id: 0,
                        headers: [],
                        properties: [],
                    };
                    this.updateOneType({ type: emptyType, forFeature: true });
                }

                if(this.objectForCard && this.objectForCard.geometry && this.objectForCard.geometry.type === 'Point'){
                    this.offPointsFlag_ = false
                    this.setOffPointsFlag(false)
                }
                
            },
        },
        
        
    },
    computed: {
        ...mapGetters(['offPointsFlag', 'arrayEditMode', 'getObjectForCard', 'emptyObject', 'oneType', 'typeForFeature', 'allListItem', 'arrayEdit', 'newData', 'actions', 'user', 'error']),
    },
    methods: {
        ...mapActions(['getTypeObject', 'deleteObject', 'putObject', 'setOffPointsFlag', 'postObject', 'getOneObject', 'getAllObject', 'filterForFeature', 'getOneTypeObjectForFeature', 'getAlltypeForTable', 'putUser']),
        ...mapMutations(['updateFunction', 'updateOffPointsFlag', 'upadateEmptyObject', 'updateOneType', 'updateArrayEditMode', 'updateObjectForCard']),

        fileToBase64(file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                this.objectForCard.image = e.target.result;
            };
            reader.readAsDataURL(file);
        },

    },

    mounted() {
        this.setOffPointsFlag(false)
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

.card_of_object {
    width: 38.05% !important;
    z-index: 5 !important;
    min-height: 92.08% !important;
    position: absolute !important;
    left: 60.28% !important;
    top: 4.19% !important;
    border-radius: 12px !important;
}

.card__info {
    align-items: center;
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
    /* justify-content: space-between; */
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