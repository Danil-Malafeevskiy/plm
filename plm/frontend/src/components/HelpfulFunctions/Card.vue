<template>
    <v-scroll-x-reverse-transition>
        <v-card class="card_of_object" v-show="cardVisable_.data">
            <div class="card__window">
                <p style="display: none">{{ objectForCard }}</p>
                <PictureForCard v-show="!conflictCard" :objectForCard_="objectForCard" :infoCardOn_="infoCardOn"
                    :conflictCard="conflictCard" />

                <PictureForConflict v-show="conflictCard" :objectForCard_="objectForCard"
                    :objectForConflict="objectForConflict" />

                <StandartFormCard v-if="!conflictCard" :objectForCard_="objectForCard" :infoCardOn="infoCardOn"
                    :editCardOn="editCardOn" :editMode="editMode" :addCardOn="addCardOn_"
                    @notVisableCard="notVisableCard" :cardVisable="cardVisable" :errorMessage="errorMessage"
                    :snackbar="snackbar" @showSnacker="showSnacker" />
                <template v-else>
                    <v-tabs v-model="tab" align-with-title style="z-index: 1" color="#E93030">
                        <v-tab v-for="item in sliderForConflict" :key="item" class="ma-0">
                            <span>{{ item }}</span>
                        </v-tab>
                    </v-tabs>
                    <v-divider></v-divider>
                    <v-tabs-items v-model="tab" style="position: absolute; top: 0; bottom: 0; left: 0; right: 0;">
                        <v-tab-item>
                            <StandartFormCard :objectForCard_="objectForCard" :infoCardOn="infoCardOn"
                                :editCardOn="editCardOn" :editMode="editMode" :addCardOn="addCardOn_"
                                @notVisableCard="notVisableCard" :cardVisable="cardVisable" :errorMessage="errorMessage"
                                :snackbar="snackbar" @showSnacker="showSnacker" :conflictCard="conflictCard" />
                        </v-tab-item>
                        <v-tab-item>
                            <ConflictFormForCard :objectForCard_="objectForCard" :conflictCard="conflictCard"
                                :objectForConflict="objectForConflict" />
                        </v-tab-item>
                        <v-tab-item>
                            <TableForConflict :objectForCard="objectForCard" :cardVisable="cardVisable" />
                        </v-tab-item>
                    </v-tabs-items>
                </template>
            </div>
            <CardFooter v-if="!infoCardOn.data" :objectForCard_="objectForCard" :infoCardOn="infoCardOn"
                :editCardOn="editCardOn" :editMode="editMode" :addCardOn="addCardOn_" @notVisableCard="notVisableCard"
                :cardVisable="cardVisable" @showSnacker="showSnacker" />
        </v-card>
    </v-scroll-x-reverse-transition>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket } from '@mdi/js'
import StandartFormCard from './StandartFormCard.vue';
import CardFooter from './CardFooter.vue';
import ConflictFormForCard from './ConflictFormForCard.vue';
import Vue from 'vue';
import TableForConflict from './TableForConflict.vue';
import PictureForCard from './PictureForCard.vue';
import PictureForConflict from './PictureForConflict.vue';

export default {
    name: 'CardInfo',
    components: {
        StandartFormCard,
        CardFooter,
        ConflictFormForCard,
        TableForConflict,
        PictureForCard,
        PictureForConflict
    },
    props: ['cardVisable', 'addCardOn', 'infoCardOn', 'editCardOn', 'visableCard', 'notVisableCard', 'editMode', 'conflictCard', 'objectForConflict'],
    data() {
        return {
            cardVisable_: this.cardVisable,
            addCardOn_: this.addCardOn,
            infoCardOn_: this.infoCardOn,
            editCardOn_: this.editCardOn,
            objectForCard: {},
            listMdiIcons: [mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket],
            errorMessage: '',
            snackbar: false,
            sliderForConflict: ['Объект', 'Конфликт версий', 'Конфликт положений'],
            tab: null,
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
                if ('name' in this.objectForCard && typeof this.objectForCard.name === 'string') {
                    Vue.set(this.objectForCard, 'ruls', []);
                }
            },
        }
    },
    computed: {
        ...mapGetters(['offPointsFlag', 'arrayEditMode', 'getObjectForCard', 'emptyObject', 'oneType', 'typeForFeature', 'allListItem', 'arrayEdit', 'newData', 'actions', 'user', 'error']),
        heightPicture() {
            if (this.conflictCard)
                return '24.48%'
            else
                return '37.5%'
        }
    },
    methods: {

        ...mapActions(['getTypeObject', 'deleteObject', 'putObject', 'setOffPointsFlag', 'postObject', 'getOneObject', 'getAllObject', 'filterForFeature', 'getOneTypeObjectForFeature', 'getAlltypeForTable', 'putUser']),
        ...mapMutations(['updateFunction', 'updateOffPointsFlag', 'upadateEmptyObject', 'updateOneType', 'updateArrayEditMode', 'updateObjectForCard']),

        showSnacker(errorText) {
            this.errorMessage = errorText;
            this.snackbar = true;
        },
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

.v-window {
    border-radius: 12px !important;
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

.card__info {
    align-items: center;
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


.v-icon--link::after {
    background-color: rgba(255, 255, 255, 0) !important;
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
.card_of_object {
    width: 38.05% !important;
    z-index: 5 !important;
    min-height: 92.08% !important;
    position: absolute !important;
    left: 60.28% !important;
    top: 4.19% !important;
    border-radius: 12px !important;
}
</style>