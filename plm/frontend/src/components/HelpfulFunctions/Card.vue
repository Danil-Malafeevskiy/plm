<template>
    <v-card class="card_of_object" v-show="cardVisable_.data === true">
        <div class="card__window">
            <p style="display: none;">{{ emptyObject }}</p>
            <v-file-input class="pa-0 ma-0" height="37.53%" color="#EE5E5E" :prepend-icon="icon" hide-input>
            </v-file-input>
            <div style="overflow-y: scroll; overflow-x: hidden; height: 100%">
                <v-card-text class="pa-0">
                    <v-form>
                        <v-row justify="start" v-if="addCardOn_.data">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text style="font-size: 24px; padding: 16px 0;">Создание объекта</v-card-text>
                            </v-col>
                            <v-col v-for="(f, index) in emptyObject.properties" :key="f.number_support" cols="2" sm="6"
                                md="5" lg="6">

                                <v-text-field v-if="typeof (f) === 'number'" type="number"
                                    v-model.number="emptyObject.properties[index]"
                                    :value="emptyObject.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                                <v-text-field v-else-if="typeof (f) === 'string'" type="text"
                                    v-model="emptyObject.properties[index]" :value="emptyObject.properties[index]"
                                    hide-details :label="index" :placeholder="index" filled>
                                </v-text-field>
                                <!-- <v-text-field v-else type="checkbox" v-model="emptyObject.properties[index]"
                                    :value="emptyObject.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field> -->

                            </v-col>
                        </v-row>
                        <v-row justify="start" v-else-if="infoCardOn_.data">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text class="pa-0" style="font-size: 24px;">{{ getObjectForCard.name }}
                                </v-card-text>
                            </v-col>

                            <v-col class="pa-0" cols="2" sm="6" md="5" lg="6">
                                <v-card-text class="pa-0"
                                    style="font-size: 24px; display: flex; justify-content: flex-end;">
                                    <v-btn
                                        @click="editCardOn_.data = !editCardOn_.data; infoCardOn_.data = !infoCardOn_.data;"
                                        class="ma-0" fab small elevation="0" color="white">
                                        <v-icon>
                                            mdi-pencil
                                        </v-icon>
                                    </v-btn>
                                    <v-btn
                                        @click="deleteObject(getObjectForCard.id); infoCardOn_.data = !infoCardOn_.data; notVisableCard()"
                                        class="ma-0" fab small elevation="0" color="white">
                                        <v-icon>
                                            mdi-delete-outline
                                        </v-icon>
                                    </v-btn>
                                </v-card-text>
                            </v-col>
                            <v-col v-for="(f, index) in getObjectForCard.properties" :key="f.number_support"
                                v-show="index != 'name_tap' && index != 'id'" cols="2" sm="6" md="5" lg="6">

                                <v-text-field v-if="typeof (f) === 'number'" type="number" readonly
                                    v-model="getObjectForCard.properties[index]"
                                    :value="getObjectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                                <v-text-field v-else-if="typeof (f) === 'string'" type="text" readonly
                                    v-model="getObjectForCard.properties[index]"
                                    :value="getObjectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                                <!-- <v-text-field v-else type="checkbox" v-model="getObjectForCard.properties[index]"
                                    :value="getObjectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled readonly>
                                </v-text-field> -->

                            </v-col>
                        </v-row>
                        <v-row justify="start" v-else-if="editCardOn.data">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text style="font-size: 24px; padding: 16px 0;">Редактирование</v-card-text>
                            </v-col>
                            <v-col v-for="(f, index) in getObjectForCard.properties" :key="f.number_support"
                                v-show="index != 'id'" cols="2" sm="6" md="5" lg="6">

                                <v-text-field v-if="typeof (f) === 'number'" type="number"
                                    v-model.number="getObjectForCard.properties[index]"
                                    :value="getObjectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                                <v-text-field v-else-if="typeof (f) === 'string'" type="text"
                                    v-model="getObjectForCard.properties[index]"
                                    :value="getObjectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                                <!-- <v-text-field v-else type="checkbox" v-model="getObjectForCard.properties[index]"
                                    :value="getObjectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field> -->

                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
            </div>

            <div class="card__footer" v-if="addCardOn_.data">
                <v-btn color="white" depressed @click="notVisableCard(); addCardOn_.data = !addCardOn_.data">ОТМЕНА
                </v-btn>
                <v-btn color="white" depressed @click="addNewFeature()">Создать</v-btn>
            </div>
            <div class="card__footer" v-else-if="editCardOn_.data">
                <v-btn color="white" depressed @click="notVisableCard(); editCardOn_.data = !editCardOn_.data">ОТМЕНА
                </v-btn>
                <v-btn color="white" depressed @click="editObject()">Редактирование</v-btn>
            </div>

        </div>
    </v-card>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiImagePlusOutline } from '@mdi/js'

export default {
    name: 'CardInfo',
    props: ['cardVisable', 'addCardOn', 'infoCardOn', 'editCardOn', 'visableCard', 'notVisableCard'],
    data() {
        return {
            cardVisable_: this.cardVisable,
            addCardOn_: this.addCardOn,
            infoCardOn_: this.infoCardOn,
            editCardOn_: this.editCardOn,
            feature: this.getFeature,
            icon: mdiImagePlusOutline,
        }
    },
    watch: {
        cardVisable: {
            handler() {
                this.cardVisable_ = this.cardVisable;
                if (this.cardVisable_.data) {
                    if (document.querySelector('.v-navigation-drawer').clientWidth * 100 / 1920 < 18) {
                        document.querySelector('.card_of_object').style.cssText = 'width: 38.05% !important; left: 60.28% !important;';
                    }
                    else {
                        document.querySelector('.card_of_object').style.cssText = 'width: 31.91% !important; left: 67.22% !important;';
                    }
                }
            }, deep: true
        },
        getFeature: function () {
            this.feature = this.getFeature;
        },
    },
    computed: {
        ...mapGetters(['featureName', 'filterFeature', 'getFeature', 'getObjectForCard', 'emptyObject']),
    },
    methods: {
        ...mapActions(['deleteObject', 'putObject', 'postObject']),
        ...mapMutations(['updateFunction']),
        async addNewFeature() {
            this.emptyObject.name = this.featureName;
            if (this.emptyObject.name != null) {
                await this.postObject(JSON.stringify([this.emptyObject]));
            }
            else {
                await this.postObject(JSON.stringify([this.emptyObject.properties]));
            }
            this.addCardOn_.data = !this.addCardOn_.data;
            this.notVisableCard();
        },
        async editObject() {
            this.getObjectForCard.geometry.coordinates = [this.getObjectForCard.properties['Широта'], this.getObjectForCard.properties['Долгота']];
            await this.putObject(JSON.stringify(this.getObjectForCard));
            this.editCardOn_.data = !this.editCardOn_.data;
            this.infoCardOn_.data = !this.infoCardOn_.data;
        }
    },
}
</script>

<style>
.show__card {
    margin-right: 8px;
    border-radius: 8px !important;
}

.v-window__container {
    min-height: 100%;
}

.card_of_object {
    z-index: 1 !important;
    min-height: 92.08% !important;
    position: absolute !important;
    left: 60.28% !important;
    top: 4.19% !important;
    border-radius: 12px !important;
}

.card__info {
    align-items: center;
}

.card__footer {
    align-items: flex-end;
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
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 12px;
}

.card__img {
    align-items: flex-start;
}

.v-input__icon,
.v-icon--link {
    min-width: 100% !important;
    height: 100% !important;
    min-height: 100% !important;
    justify-content: center !important;
    align-items: center !important;
}

.v-icon--link::after {
    background-color: rgba(255, 255, 255, 0) !important;
}

.v-file-input {
    min-height: 37.53%;
    max-height: 37.53%;
    background-color: #EE5E5E;
    border-radius: 12px 12px 0 0;
}

.row {
    padding: 24px 24px 12px 24px !important;
}

.card_from_block {
    height: 100%;
}
</style>