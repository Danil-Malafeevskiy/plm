<template>
    <v-scroll-x-reverse-transition>
        <v-card class="card_of_object" v-show="cardVisable.data === true">
            <div class="card__window">
                <p style="display: none">{{ objectForCard }}</p>
                <template
                    v-if="objectForConflict_ && objectForCard && objectForConflict_.image === objectForCard.image">
                    <v-img v-if="objectForCard.image" :src="objectForCard.image" class="one_picture">
                    </v-img>

                    <v-file-input v-else class="pa-0 ma-0 background_color_red" :prepend-icon="icon" disabled
                        hide-input>
                    </v-file-input>
                </template>
                <div v-else-if="objectForConflict_ && objectForCard" class="conflict_pictures">
                    <v-img v-if="objectForConflict_.image" :src="objectForConflict_.image" class="two_pictures">
                    </v-img>
                    <v-file-input v-else class="pa-0 ma-0 two_background_color_red" :prepend-icon="icon" disabled
                        hide-input>
                    </v-file-input>
                    <v-btn small icon @click="changeImage" style="
                                        max-height: 100% !important;
                                        margin: auto 0 !important;
                                    ">
                        <v-icon v-if="notConflictObject.image === objectForCard.image">
                            mdi-arrow-right</v-icon>
                        <v-icon v-else>mdi-arrow-left</v-icon>
                    </v-btn>
                    <v-img v-if="objectForCard.image" :src="objectForCard.image" class="two_pictures">
                    </v-img>
                    <v-file-input v-else class="pa-0 ma-0 two_background_color_red" :prepend-icon="icon" disabled
                        hide-input>
                    </v-file-input>
                </div>

                <v-tabs v-model="tab" align-with-title color="#E93030">
                    <v-tab v-for="item in items" :key="item" class="ma-0">
                        <span>{{ item }}</span>
                    </v-tab>
                </v-tabs>
                <v-divider></v-divider>
                <v-tabs-items v-model="tab">
                    <v-tab-item v-if="items.find(el => el === 'Конфликт версий')">

                        <div style="overflow-y: hidden; overflow-x: hidden; height: 100%">
                            <v-card-text class="pa-0">
                                <div style="display: flex">
                                    <v-card-text
                                        style="font-size: 16px; color: #787878; font-weight: 500; padding: 16px 24px;">
                                        Версия в системе
                                    </v-card-text>
                                    <v-card-text
                                        style="font-size: 16px; color: #787878; font-weight: 500; padding: 16px 30px;">
                                        Новая версия
                                    </v-card-text>
                                </div>
                                <v-form v-if="objectForConflict_ !== undefined">
                                    <v-row justify="space-between" style="padding-bottom: 0 !important;">
                                        <template v-for="el in typeForFeature.headers">
                                            <v-col :key="`origin-element-${el.text}`" cols="3" sm="6" md="5" lg="6"
                                                v-if="el.text != 'id'">
                                                <v-text-field v-if="objectForConflict_"
                                                    :class="{ 'blue_field': !checkEqualityOfFieads(el.text) }"
                                                    v-model="objectForConflict_.properties[el.text]" hide-details
                                                    :label="el.text" :placeholder="el.text" filled disabled>
                                                </v-text-field>
                                            </v-col>
                                            <v-btn v-if="!checkEqualityOfFieads(el.text) && el.text != 'id'" small icon
                                                :key="`change-field-button-${el.text}`" @click="changeItem(el.text)"
                                                style="
                                        max-height: 100% !important;
                                        margin: auto 0 !important;
                                    ">
                                                <v-icon
                                                    v-if="notConflictObject.properties[el.text] === objectForCard.properties[el.text]">
                                                    mdi-arrow-right</v-icon>
                                                <v-icon v-else>mdi-arrow-left</v-icon>
                                            </v-btn>
                                            <v-col v-if="objectForCard && el.text != 'id'"
                                                :key="`new-element-${el.text}`" cols="3" sm="6" md="5" lg="6"
                                                v-show="el != 'id'">
                                                <v-text-field :class="{ 'blue_field': !checkEqualityOfFieads(el.text) }"
                                                    v-model="objectForCard.properties[el.text]" hide-details
                                                    :label="el.text" :placeholder="el.text" filled>
                                                </v-text-field>
                                            </v-col>
                                        </template>
                                    </v-row>

                                    <FormForDynamicField :objectForCard="objectForCard" :infoCardOn="{ data: true }"
                                        :checkEqualityOfFieads="checkEqualityOfFieads" :conflictCard="conflictCard"
                                        :objectForConflict="objectForConflict" :changeItem="changeItem"
                                        :notConflictObject="notConflictObject" />

                                    <v-row justify="space-between" style="padding-bottom: 0 !important;">
                                        <v-col cols="3" sm="6" md="5" lg="6">
                                            <v-card-text>Новая геометрия</v-card-text>
                                        </v-col>
                                        <v-btn small icon @click="changeCoordinates()" style="
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

                    </v-tab-item>
                    <v-tab-item>
                        <v-card-text style="font-size: 16px; color: #454545; font-weight: 400; padding: 16px 30px;">
                            Конфликтующие объекты
                        </v-card-text>
                        <v-data-table :headers="headers" item-key="id" :items="itemsForTable" hide-default-footer
                            style="background-color: #FFFFFF; padding: 16px 30px;">
                        </v-data-table>
                    </v-tab-item>
                </v-tabs-items>

                <div class="card__footer">
                    <v-btn text color="#787878" @click="notVisableCard()" style="margin-right: 15px !important">
                        ОТМЕНА
                    </v-btn>
                    <v-btn text @click="editObject()" color="#787878">применить</v-btn>

                </div>
            </div>
        </v-card>
    </v-scroll-x-reverse-transition>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiImagePlusOutline } from '@mdi/js';
import FormForDynamicField from './FormForDynamicField.vue';

export default {
    name: 'CardConflict',
    components: {
        FormForDynamicField,
    },
    props: ['cardVisable', 'conflictCard', 'editMode', 'notVisableCard', 'objectForConflict'],
    data() {
        return {
            cardVisable_: this.cardVisable,
            showPassword: false,
            icon: mdiImagePlusOutline,
            listSelectedIcons: [],
            isOldItem: false,
            objectForConflict_: { properties: {} },
            objectForCard: this.getObjectForCard,
            notConflictObject: { properties: {} },
            tab: null,
            items: ['Конфликт версий', 'Конфликт положений'],
            headers: [
                {
                    text: 'Имя объекта',
                    value: 'id'
                },
                {
                    text: 'Тип объекта',
                    value: 'type'
                },
            ],
            itemsForTable: [],
        }
    },
    watch: {
        getObjectForCard: function () {
            this.objectForCard = this.getObjectForCard;
            //this.objectForConflict_ = this.getObjectForCard;
            this.notConflictObject = JSON.parse(JSON.stringify(this.objectForCard));
            if (this.newData.find(el => el.id === this.getObjectForCard.id)) {
                this.items[0] = 'Конфликт версий';
            }
            else {
                this.items.filter(el => el != 'Конфликт версий')
            }
            if (this.conflictArrays.find(el => el.find(element => element.id_ === undefined ? element.id === this.getObjectForCard.id : element.id_ === this.getObjectForCard.id_))) {
                this.itemsForTable = [];
                this.items[this.items.length] = 'Конфликт положений';
                let array = this.conflictArrays.find(el => el.find(element => element.id_ === undefined ? element.id === this.getObjectForCard.id : element.id_ === this.getObjectForCard.id_))
                array.forEach(element => {
                    this.itemsForTable.push({ id: element.id, type: this.allType.find(el => el.id === element.name).name })
                })
            }
            else {
                this.items.filter(el => el != 'Конфликт положений')
            }
            this.items = [...new Set(this.items)];
        },
        cardVisable: {
            handler() {
                this.cardVisable_ = this.cardVisable;
            }, deep: true
        },
        objectForConflict: function () {
            this.objectForConflict_ = this.objectForConflict;
            this.notConflictObject = JSON.parse(JSON.stringify(this.objectForCard));
        },
    },
    computed: {
        ...mapGetters(['getObjectForCard', 'emptyObject', 'oneType', 'typeForFeature', 'arrayEdit', 'newData', 'actions', 'allListItem', 'conflictArrays', 'allType']),
    },
    methods: {
        ...mapActions(['getOneTypeObjectForFeature']),
        ...mapMutations(['updateOneType', 'updateObjectForCard', 'updateArrayEditMode', 'deleteItemFromNewData']),
        async editObject() {
            this.notConflictObject.geometry.coordinates = this.objectForCard.geometry.coordinates;
            this.updateArrayEditMode({ item: this.notConflictObject, type: 'put' });
            this.deleteItemFromNewData(this.notConflictObject);
            this.allListItem.forEach(element => {

                if (element.id === this.notConflictObject.id) {
                    for (let el in element) {
                        if (el != 'id') {
                            element[el] = this.notConflictObject.properties[el];
                        }
                    }
                }
            });
            await this.updateObjectForCard(JSON.parse(JSON.stringify(this.notConflictObject)));
            this.objectForConflict_ = { properties: {} };
            this.notVisableCard();
        },
        changeItem(field) {
            if (this.notConflictObject.properties[field] == this.objectForCard.properties[field]) {
                this.notConflictObject.properties[field] = this.objectForConflict_.properties[field];
            }
            else {
                this.notConflictObject.properties[field] = this.objectForCard.properties[field];
            }
        },
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
        },
        changeImage() {
            this.notConflictObject.image = this.notConflictObject.image === this.objectForCard.image ? this.objectForConflict.image : this.objectForCard.image;
        },
        changeCoordinates() {
            if (this.objectForCard.geometry !== this.objectForConflict_.geometry) {
                this.objectForCard.geometry = this.objectForConflict_.geometry;
            }
            else {
                this.objectForCard.geometry = this.notConflictObject.geometry;
            }
        }
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

.card__footer {
    display: flex;
    bottom: 0px;
    justify-content: flex-end;
    border-top: 1px solid #E0E0E0;
    border-radius: 0 0 12px 12px !important;
    background-color: white;
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

.card__footer {
    display: flex;
    bottom: 0px;
    justify-content: flex-end;
    border-top: 1px solid #E0E0E0;
    border-radius: 0 0 12px 12px !important;
    background-color: white;
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