<template>
    <v-scroll-x-reverse-transition>
        <v-card class="card_of_object" v-show="cardVisable_.data === true">
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
                    }" width="100%" height="37.53%"></v-img>
                </template>

                <div style="overflow-y: scroll; overflow-x: hidden; height: 100%">
                    <v-card-text class="pa-0">
                        <v-form>
                            <v-row justify="start" style="padding-bottom: 0 !important;">
                                <v-col cols="2" sm="6" md="5" lg="6" v-if="infoCardOn_.data">
                                    <v-card-text v-if="objectForCard.properties.first_name != undefined" class="pa-0"
                                        style="font-size: 24px;">{{
                                                objectForCard.properties.first_name
                                        }}
                                    </v-card-text>
                                    <v-card-text v-else-if="'name' in objectForCard" class="pa-0"
                                        style="font-size: 24px;">
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
                                            :disabled="(!editMode && 'type' in this.objectForCard) || (user.permissions.filter(el => el.includes(objectForCard.group)).length != 2 && (!user.is_staff || !user.is_superuser))"
                                            :class="{ 'btn_disabled': !editMode && actions === 'getFeatures' }">
                                            <v-icon>
                                                mdi-pencil
                                            </v-icon>
                                        </v-btn>
                                        <v-btn @click="deleteObjectOnCard()" class="ma-0 btn" fab small elevation="0"
                                        :disabled="(!editMode && 'type' in this.objectForCard) || (user.permissions.filter(el => el.includes(objectForCard.group)).length != 2 && (!user.is_staff || !user.is_superuser))"
                                            style="background-color: white !important"
                                            :class="{ 'btn_disabled': !editMode && actions === 'getFeatures' }">
                                            <v-icon>
                                                mdi-delete-outline
                                            </v-icon>
                                        </v-btn>
                                    </v-card-text>
                                </v-col>
                                <v-col cols="2" sm="6" md="5" lg="6" v-else-if="addCardOn_.data">
                                    <v-card-text style="font-size: 24px; padding: 16px 0;">Создание объекта
                                    </v-card-text>
                                </v-col>
                                <v-col cols="2" sm="6" md="5" lg="6" v-else>
                                    <v-card-text style="font-size: 24px; padding: 16px 0;">Редактирование</v-card-text>
                                </v-col>
                                <template v-if="!('name' in objectForCard)">
                                    <v-col v-for="(f, index) in objectForCard.properties" :key="index" cols="2" sm="6"
                                        md="5" lg="6" v-show="typeof (f) != 'object' && index != 'group'">
                                        <v-text-field
                                            v-if="index != 'password' && index != 'first_name' && index != 'last_name' && index != 'type' && index != 'all_obj'"
                                            v-model="objectForCard.properties[index]" hide-details :label="index"
                                            :placeholder="index" filled :readonly="infoCardOn_.data">
                                        </v-text-field>
                                        <v-text-field v-else-if="index === 'password'"
                                            v-model="objectForCard.properties[index]"
                                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.min]"
                                            hint="Минимум 8 символов" :type="showPassword ? 'text' : 'password'"
                                            @click:append="showPassword = !showPassword" :label="index"
                                            :placeholder="index" filled :readonly="infoCardOn_.data">
                                        </v-text-field>
                                        <v-select v-else-if="index === 'type'" v-model="objectForCard.properties.type"
                                            filled lable="type" :items="types" :readonly="infoCardOn_.data">
                                        </v-select>
                                        <v-text-field v-else-if="index != 'all_obj'"
                                            v-model="objectForCard.properties[index]" :label="index"
                                            :placeholder="index" :hide-details="infoCardOn.data" filled
                                            :readonly="infoCardOn_.data" :rules="[rules.required]">
                                        </v-text-field>
                                    </v-col>
                                </template>
                                <template v-else-if="('name' in objectForCard)">
                                    <v-col v-for="el in typeForFeature.headers" :key="el.text" cols="2" sm="6" md="5"
                                        lg="6" v-show="el.text != 'id'">
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

                            <FormForDynamicField v-if="allListItem[0] !== user" :objectForCard="objectForCard"
                                :infoCardOn="infoCardOn" :checkEqualityOfFieads="checkEqualityOfFieads"
                                :changeConflictField="changeConflictField" />

                            <ExpansionPanelForCard v-if="allListItem[0] !== user" :objectForCard="objectForCard"
                                :cardVisable="cardVisable" :infoCardOn="infoCardOn" />
                            <v-snackbar v-model="snackbar" timeout="5000" color="red accent-2">
                                {{ errorMessege }}
                            </v-snackbar>
                        </v-form>
                        <v-form v-if="allListItem[0] === user">
                            <v-row justify="start" style="padding-bottom: 0 !important;">
                                <p class="attributes ma-0">Изменение пароля</p>
                                <v-col cols="2" sm="6" md="5" lg="6">
                                    <v-text-field v-model="password" label="Новый пароль"
                                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                        hint="Минимум 8 символов" placeholder="Новый пароль"
                                        :type="showPassword ? 'text' : 'password'" filled :readonly="infoCardOn_.data"
                                        @click:append="showPassword = !showPassword" :rules="[rules.min]">
                                    </v-text-field>
                                </v-col>
                                <v-col cols="2" sm="6" md="5" lg="6">
                                    <v-text-field v-model="password_again" label="Повторите пароль"
                                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                        hint="Минимум 8 символов" placeholder="Повторите пароль"
                                        :type="showPassword ? 'text' : 'password'" filled :readonly="infoCardOn_.data"
                                        @click:append="showPassword = !showPassword" :rules="[rules.min]">
                                    </v-text-field>
                                </v-col>
                                <v-col cols="2" sm="6" md="5" lg="6"></v-col>
                                <v-col cols="2" sm="6" md="5" lg="6" style="display: flex; justify-content: flex-end">
                                    <v-btn :disabled="password.length < 8 && password_again.length < 8"
                                        @click="changePassword" class="ma-0" text v-if="editCardOn.data">
                                        Изменить пароль
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>
                </div>
                <div class="card__footer" v-if="addCardOn_.data">
                    <v-btn text @click="notVisableCard(); addCardOn_.data = !addCardOn_.data">ОТМЕНА
                    </v-btn>
                    <v-btn text @click="addNewFeature()">Создать</v-btn>
                </div>
                <div class="card__footer" v-else-if="editCardOn.data">
                    <v-btn @click="changeItem(isOldItem = !isOldItem)"
                        v-if="newData.filter(el => el.id === objectForCard.id).length" color="#0F0CA7" text
                        style="margin-right: 15px !important">
                        оригинал
                    </v-btn>

                    <v-btn v-if="allListItem[0] != user" text
                        @click="notVisableCard(); editCardOn_.data = !editCardOn_.data"
                        style="margin-right: 15px !important">
                        ОТМЕНА
                    </v-btn>
                    <v-btn text @click="editObject()">применить</v-btn>

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
import { v4 as uuidv4 } from 'uuid';

export default {
    name: 'CardInfo',
    components: {
        ExpansionPanelForCard,
        FormForDynamicField,
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
            listSelectedIcons: [],
            isOldItem: false,
            snackbar: false,
            rules: {
                required: value => !!value || 'Обязательное поле',
                min: v => v !== undefined ? v.length >= 8 : !!v || 'Минимум 8 символов',
            },
            errorMessege: '',
            password: '',
            password_again: '',
            types: ['Point', 'LineString', 'Polygon']
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
        },
        allListItem: {
            handler() {
                if (this.allListItem[0] === this.user) {
                    let userForCard = { properties: {} };
                    for (let i in this.user) {
                        if (i === 'email' || i === 'first_name' || i === 'last_name' || i === 'email') {
                            userForCard.properties[i] = this.user[i];
                        }
                        else {
                            userForCard[i] = this.user[i];
                        }
                    }
                    this.updateObjectForCard(userForCard);
                }
            }
        },
        snackbar: {
            handler() {
                if (!this.snackbar) {
                    this.updateError(null);
                }
            }
        }
    },
    computed: {
        ...mapGetters(['getTypeId', 'getObjectForCard', 'emptyObject', 'oneType', 'typeForFeature', 'allListItem', 'arrayEdit', 'newData', 'actions', 'user', 'error']),
    },
    methods: {
        ...mapActions(['getTypeObject', 'deleteObject', 'putObject', 'postObject', 'getOneObject', 'getAllObject', 'filterForFeature', 'getOneTypeObjectForFeature', 'getAlltypeForTable', 'putUser']),
        ...mapMutations(['updateFunction', 'upadateEmptyObject', 'updateOneType', 'updateArrayEditMode', 'updateObjectForCard', 'deleteItemFromNewData', 'updateError']),
        async addNewFeature() {
            if (this.objectForCard.name && typeof this.objectForCard.name === 'number') {
                if (!this.objectForCard.geometry.coordinates.length) {
                    this.showSnacker('Создайте объект на карте!');
                    return;
                }
                this.objectForCard.id_ = uuidv4();
                this.updateArrayEditMode({ item: JSON.parse(JSON.stringify(this.objectForCard)), type: 'post' });
            }
            else {
                this.checkCorrectFields();

                let object = JSON.parse(JSON.stringify(this.objectForCard));
                object = { ...object, ...object.properties }
                delete object.properties;
                await this.postObject(object);
            }
            if (this.error) {
                this.showSnacker(this.error);
                return;
            }
            else {
                this.addCardOn_.data = !this.addCardOn_.data;
                this.notVisableCard();
            }
        },
        async editObject() {
            if ('type' in this.objectForCard) {
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
                if (!this.checkCorrectFields()) {
                    return;
                }

                let object = JSON.parse(JSON.stringify(this.objectForCard));
                object.properties = { ...object, ...object.properties }
                delete object.properties.properties;

                await this.putObject(object);
            }
            if (this.error) {
                this.showSnacker(this.error);
                return;
            }
            else {
                this.editCardOn_.data = !this.editCardOn_.data;
                this.infoCardOn_.data = !this.infoCardOn_.data;
            }
        },
        async changePassword() {
            if (this.password === this.password_again) {
                const user = {
                    id: this.user.id,
                    email: this.user.email,
                    password: this.password,
                }
                await this.putUser(user);

                if (this.error) {
                    this.showSnacker(this.error);
                    return;
                }
            }
            else {
                this.showSnacker('Пароли не совпадают');
                return;
            }
        },
        checkCorrectFields() {
            if ('groups' in this.objectForCard) {
                for (let key in this.objectForCard.properties) {
                    if (key !== 'password' && key != 'email' && this.objectForCard.properties[key] === '') {
                        this.showSnacker('Обязательные поля не могут быть пустыми');
                        return false;
                    }
                    else if (key === 'password' && this.objectForCard.properties[key].length < 8) {
                        this.showSnacker('Пароль не может юыть меньше 8 символов');
                        return false;
                    }
                }
                if (!this.objectForCard.groups.length) {
                    this.showSnacker('Выберите группы');
                    return false;
                }

                else if (!this.objectForCard.properties.email.toLowerCase()
                    .match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
                    this.showSnacker('Некорректный email');
                    return false;
                }
            }

            else if ('headers' in this.objectForCard.properties) {
                if (!this.objectForCard.properties.name) {
                    this.showSnacker('Введите имя типа');
                    return false;
                }
                else if (!this.objectForCard.properties.type) {
                    this.showSnacker('Введите тип геометрии');
                    return false;
                }
                else if (!this.objectForCard.properties.headers.length) {
                    this.showSnacker('Добавьте основные атрибуты');
                    return false;
                }
                else if (this.checkDoubleFields(this.objectForCard.properties)) {
                    this.showSnacker('Не может быть атрибутов с одинаковыми именами');
                    return false;
                }
                this.objectForCard.properties.image = this.objectForCard.image;
            }
            return true;
        },
        showSnacker(errorText) {
            this.errorMessege = errorText;
            this.snackbar = true;
        },
        async deleteObjectOnCard() {
            if (this.actions === 'getFeatures') {
                this.updateArrayEditMode({ item: this.objectForCard, type: 'delete' })
            }
            else {
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
                newPutobject = this.arrayEdit.put.filter(el => el.id === this.objectForCard.id);
            }

            this.updateObjectForCard(JSON.parse(JSON.stringify(newPutobject[0])));
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
        changeConflictField(field) {
            if (!this.infoCardOn.data) {
                let newPutObject = this.newData.filter(el => el.id === this.objectForCard.id)
                if (newPutObject[0].properties[field] === this.objectForCard.properties[field]) {
                    newPutObject = this.arrayEdit.put.filter(el => el.id === this.objectForCard.id);
                }
                this.objectForCard.properties[field] = newPutObject[0].properties[field];
            }
        },

        clickImage(element) {
            this.objectForCard.image = element.slice(4) + '.png'
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

.card_of_object {
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