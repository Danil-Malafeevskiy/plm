<template>
    <v-card class="card_of_object" v-show="cardVisable_.data === true">
        <div class="card__window">
            <p style="display: none">{{ objectForCard }}</p>
            <v-file-input v-if="!objectForCard.image" @change="fileToBase64" accept="image/*" :class="{
                'background_color_red': !('properties' in objectForCard && 'username' in objectForCard.properties),
                'background_color_gray': ('properties' in objectForCard && 'username' in objectForCard.properties)
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
            <v-img v-if="objectForCard.image" :src="objectForCard.image" :class="{
                'one_picture': infoCardOn_.data,
                'not_one_picture': !infoCardOn_.data,
            }" width="100%" height="37.53%"></v-img>
            <div style="overflow-y: scroll; overflow-x: hidden; height: 100%">
                <v-card-text class="pa-0">
                    <v-form>
                        <v-row justify="start" style="padding-bottom: 0 !important;">
                            <v-col cols="2" sm="6" md="5" lg="6" v-if="infoCardOn_.data">
                                <v-card-text v-if="objectForCard.properties.username != undefined" class="pa-0"
                                    style="font-size: 24px;">{{
                                            objectForCard.properties.username
                                    }}
                                </v-card-text>
                                <v-card-text v-else-if="'name' in objectForCard" class="pa-0" style="font-size: 24px;">
                                    {{
                                            typeForFeature.name
                                    }}
                                </v-card-text>
                                <v-card-text v-else class="pa-0" style="font-size: 24px;">{{
                                        objectForCard.properties.name
                                }}
                                </v-card-text>

                            </v-col>
                            <v-col class="pa-0" cols="2" sm="6" md="5" lg="6" v-if="infoCardOn_.data">
                                <v-card-text class="pa-0"
                                    style="font-size: 24px; display: flex; justify-content: flex-end;">
                                    <v-btn @click="editOn" depressed class="ma-0 btn" fab small elevation="0"
                                        style="background-color: white !important" color="white"
                                        :disabled="!editMode && actions === 'getFeatures'"
                                        :class="{ 'btn_disabled': !editMode && actions === 'getFeatures' }">
                                        <v-icon>
                                            mdi-pencil
                                        </v-icon>
                                    </v-btn>
                                    <v-btn @click="deleteObjectOnCard()" class="ma-0 btn" fab small elevation="0"
                                        :disabled="!editMode && actions === 'getFeatures'"
                                        style="background-color: white !important"
                                        :class="{ 'btn_disabled': !editMode && actions === 'getFeatures' }">
                                        <v-icon>
                                            mdi-delete-outline
                                        </v-icon>
                                    </v-btn>
                                </v-card-text>
                            </v-col>
                            <v-col cols="2" sm="6" md="5" lg="6" v-else-if="addCardOn_.data">
                                <v-card-text style="font-size: 24px; padding: 16px 0;">Создание объекта</v-card-text>
                            </v-col>
                            <v-col cols="2" sm="6" md="5" lg="6" v-else>
                                <v-card-text style="font-size: 24px; padding: 16px 0;">Редактирование</v-card-text>
                            </v-col>
                            <template v-if="!('name' in objectForCard)">
                                <v-col v-for="(f, index) in objectForCard.properties" :key="index" cols="2" sm="6"
                                    md="5" lg="6" v-show="typeof (f) != 'object' && index != 'group'">
                                    <v-text-field v-if="index != 'password'" v-model="objectForCard.properties[index]"
                                        hide-details :label="index" :placeholder="index" filled
                                        :readonly="infoCardOn_.data">
                                    </v-text-field>
                                    <v-text-field v-else v-model="objectForCard.properties[index]"
                                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.min]"
                                        hint="Минимум 8 символов" :type="showPassword ? 'text' : 'password'"
                                        @click:append="showPassword = !showPassword" hide-details :label="index"
                                        :placeholder="index" filled :readonly="infoCardOn_.data">
                                    </v-text-field>
                                </v-col>
                            </template>
                            <template v-else-if="('name' in objectForCard)">
                                <v-col v-for="el in typeForFeature.headers" :key="el.text" cols="2" sm="6" md="5" lg="6"
                                    v-show="el.text != 'id'">
                                    <v-text-field v-if="el.text != 'id' && checkEqualityOfFieads(el.text)"
                                        v-model="objectForCard.properties[el.text]" hide-details :label="el.text"
                                        :placeholder="el.text" filled :readonly="infoCardOn_.data">
                                    </v-text-field>
                                    <v-text-field v-else-if="el.text != 'id'"
                                        v-model="objectForCard.properties[el.text]" background-color="#C9C8ED"
                                        color="#0F0CA7" hide-details :label="el.text" :placeholder="el.text" filled
                                        :readonly="infoCardOn_.data" append-icon="mdi-progress-question"
                                        @click:append="changeConflictField(el.text)">
                                    </v-text-field>
                                </v-col>
                            </template>
                        </v-row>

                        <FormForDynamicField :objectForCard="objectForCard" :infoCardOn="infoCardOn"
                            :checkEqualityOfFieads="checkEqualityOfFieads" :changeConflictField="changeConflictField" />

                        <ExpansionPanelForCard :objectForCard="objectForCard" :infoCardOn="infoCardOn" />

                    </v-form>
                </v-card-text>
            </div>

            <div class="card__footer" v-if="addCardOn_.data">
                <v-btn text @click="notVisableCard(); addCardOn_.data = !addCardOn_.data">ОТМЕНА
                </v-btn>
                <v-btn text @click="addNewFeature()">Создать</v-btn>
            </div>
            <div class="card__footer" v-else-if="editCardOn_.data">
                <v-btn @click="changeItem(isOldItem = !isOldItem)"
                    v-if="newData.filter(el => el.id === objectForCard.id).length" color="#0F0CA7" text
                    style="margin-right: 15px !important">
                    оригинал
                </v-btn>

                <v-btn text @click="notVisableCard(); editCardOn_.data = !editCardOn_.data"
                    style="margin-right: 15px !important">
                    ОТМЕНА
                </v-btn>
                <v-btn text @click="editObject()">Редактирование</v-btn>

            </div>

        </div>
    </v-card>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import { mdiImagePlusOutline } from '@mdi/js'
import ExpansionPanelForCard from './ExpansionPanelForCard.vue'
import FormForDynamicField from './FormForDynamicField.vue';

export default {
    name: 'CardInfo',
    components: {
        ExpansionPanelForCard,
        FormForDynamicField
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
            rules: {
                min: v => v.length >= 8 || 'Минимум 8 символов',
            },
            isOldItem: false,
        }
    },
    watch: {
        cardVisable: {
            handler() {
                this.cardVisable_ = this.cardVisable;
                if (this.cardVisable_.data) {
                    document.querySelector('.card_of_object').style.cssText = 'width: 38.05% !important; left: 60.28% !important;';
                }
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
            }
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
            },
        }
    },
    computed: {
        ...mapGetters(['getTypeId', 'getObjectForCard', 'emptyObject', 'oneType', 'typeForFeature', 'allListItem', 'arrayEditMode', 'newData', 'actions']),
    },
    methods: {
        ...mapActions(['deleteObject', 'putObject', 'postObject', 'getOneObject', 'getAllObject', 'filterForFeature', 'getOneTypeObjectForFeature']),
        ...mapMutations(['updateFunction', 'upadateEmptyObject', 'updateOneType', 'updateArrayEditMode', 'updateObjectForCard', 'deleteItemFromNewData']),
        async addNewFeature() {
            if (this.objectForCard.name != null) {
                this.objectForCard.name = this.getTypeId;
                await this.postObject([this.objectForCard]);

                this.filterForFeature();
                this.getAllObject();
            }
            else {
                if ('groups' in this.objectForCard) {
                    this.objectForCard.properties = { ...this.objectForCard, ...this.objectForCard.properties }
                    delete this.objectForCard.properties.properties;
                }

                await this.postObject(this.objectForCard.properties);
            }
            this.addCardOn_.data = !this.addCardOn_.data;
            this.notVisableCard();
        },
        async editObject() {
            if (this.actions === 'getFeatures') {
                this.updateArrayEditMode({ item: this.objectForCard, type: 'put' });
                this.deleteItemFromNewData(this.objectForCard);
                this.allListItem.forEach(element => {

                    if (element.id === this.objectForCard.id) {
                        for (let el in element) {
                            if (el != 'id') {
                                element[el] = this.objectForCard.properties[el];
                            }
                        }
                    }
                });
                this.updateObjectForCard(JSON.parse(JSON.stringify(this.objectForCard)))
            }
            else {
                //console.log(this.objectForCard.properties)
                this.putObject(this.objectForCard);
            }
            this.editCardOn_.data = !this.editCardOn_.data;
            this.infoCardOn_.data = !this.infoCardOn_.data;
        },
        async deleteObjectOnCard() {
            if (this.actions === 'getFeatures') {
                this.updateArrayEditMode({ item: this.objectForCard, type: 'delete' })
            }
            else{
                this.deleteObject(this.objectForCard.id)
            }
            this.infoCardOn_.data = !this.infoCardOn_.data;
            this.notVisableCard();
        },
        fileToBase64(file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                this.objectForCard.image = e.target.result;
            };
            reader.readAsDataURL(file);
        },
        editOn() {
            this.editCardOn_.data = !this.editCardOn_.data;
            this.infoCardOn_.data = !this.infoCardOn_.data;
        },
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
        changeConflictField(field) {
            if (!this.infoCardOn.data) {
                let newPutObject = this.newData.filter(el => el.id === this.objectForCard.id)
                if (newPutObject[0].properties[field] === this.objectForCard.properties[field]) {
                    newPutObject = this.arrayEditMode.put.filter(el => el.id === this.objectForCard.id);
                }
                this.objectForCard.properties[field] = newPutObject[0].properties[field];
            }
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
    /* align-items: flex-end; */
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