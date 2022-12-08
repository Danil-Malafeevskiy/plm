<template>
    <div style="max-height: 53%">
        <div style="overflow-y: scroll; overflow-x: hidden; height: 100%">
            <v-card-text class="pa-0">
                <v-form class="form_for_card" :class="{
                    'edit_form': editCardOn.data || addCardOn.data
                }">
                    <v-row justify="start" style="padding-bottom: 0 !important;">
                        <v-col cols="2" sm="6" md="5" lg="6" v-if="infoCardOn_.data">
                            <v-card-text
                                v-if="'properties' in objectForCard && objectForCard.properties.first_name != undefined"
                                class="pa-0" style="font-size: 24px;">{{
                                        objectForCard.properties.first_name
                                }}
                            </v-card-text>
                            <v-card-text v-else-if="'properties' in objectForCard && 'name' in objectForCard"
                                class="pa-0" style="font-size: 24px;">
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
                                    :disabled="(!editMode && 'type' in objectForCard) || (user.permissions.filter(el => el.includes(objectForCard.group)).length != 2 && (!user.is_staff && !user.is_superuser))"
                                    :class="{ 'btn_disabled': !editMode && actions === 'getFeatures' }">
                                    <v-icon color="#A5A5A6">
                                        mdi-pencil
                                    </v-icon>
                                </v-btn>
                                <v-btn @click="deleteObjectOnCard()" class="ma-0 btn" fab small elevation="0"
                                    :disabled="(!editMode && 'type' in this.objectForCard) || (user.permissions.filter(el => el.includes(objectForCard.group)).length != 2 && (!user.is_staff && !user.is_superuser))"
                                    style="background-color: white !important"
                                    :class="{ 'btn_disabled': !editMode && actions === 'getFeatures' }">
                                    <v-icon color="#A5A5A6">
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
                            <v-col v-for="(f, index) in objectForCard.properties" :key="index" cols="2" sm="6" md="5"
                                lg="6" v-show="typeof (f) != 'object' && index != 'group' && index != 'image'">
                                <v-text-field
                                    v-if="index != 'password' && index != 'first_name' && index != 'last_name' && index != 'type' && index != 'all_obj'"
                                    v-model="objectForCard.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled :readonly="infoCardOn_.data">
                                </v-text-field>
                                <v-text-field v-else-if="index === 'password'" v-model="objectForCard.properties[index]"
                                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" :rules="[rules.min]"
                                    hint="Минимум 8 символов" :type="showPassword ? 'text' : 'password'"
                                    @click:append="showPassword = !showPassword" :label="index" :placeholder="index"
                                    filled :readonly="infoCardOn_.data">
                                </v-text-field>
                                <v-text-field
                                    v-else-if="!(index != 'first_name' && index != 'last_name' && index != 'email')"
                                    v-model="objectForCard.properties[index]" :label="index" :placeholder="index"
                                    :hide-details="infoCardOn.data || !user.is_superuser" filled
                                    :readonly="infoCardOn_.data || !user.is_superuser" :rules="[rules.required]">
                                </v-text-field>
                                <v-select v-else-if="index === 'type'" v-model="objectForCard.properties.type" filled
                                    lable="type" :items="types" :readonly="infoCardOn_.data">
                                </v-select>
                                <v-text-field v-else-if="index != 'all_obj'" v-model="objectForCard.properties[index]"
                                    :label="index" :placeholder="index" :hide-details="infoCardOn.data" filled
                                    :readonly="infoCardOn_.data" :rules="[rules.required]">
                                </v-text-field>
                            </v-col>
                        </template>
                        <template v-else-if="('name' in objectForCard)">
                            
                            <v-col v-if="editCardOn.data && Object.prototype.hasOwnProperty.call(objectForCard, 'attachFlag')">
                                <v-checkbox label="Открепить точку" v-model="objectForCard.attachFlag"></v-checkbox>
                            </v-col>

                            <v-col v-for="el in typeForFeature.headers" :key="el.text" cols="1" sm="6" md="5" lg="6"
                                v-show="el.text != 'id'">
                                <v-text-field v-if="el.text != 'id'" v-model="objectForCard.properties[el.text]"
                                    hide-details :label="el.text" :placeholder="el.text" filled
                                    :readonly="infoCardOn_.data">
                                </v-text-field>
                            </v-col>
                        </template>
                    </v-row>
                    <FormForDynamicField v-if="allListItem[0] !== user" :objectForCard="objectForCard"
                        :infoCardOn="infoCardOn" :checkEqualityOfFieads="checkEqualityOfFieads" />
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
                                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" hint="Минимум 8 символов"
                                placeholder="Новый пароль" :type="showPassword ? 'text' : 'password'" filled
                                :readonly="infoCardOn_.data" @click:append="showPassword = !showPassword"
                                :rules="[rules.min]">
                            </v-text-field>
                        </v-col>
                        <v-col cols="2" sm="6" md="5" lg="6">
                            <v-text-field v-model="password_again" label="Повторите пароль"
                                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" hint="Минимум 8 символов"
                                placeholder="Повторите пароль" :type="showPassword ? 'text' : 'password'" filled
                                :readonly="infoCardOn_.data" @click:append="showPassword = !showPassword"
                                :rules="[rules.min]">
                            </v-text-field>
                        </v-col>
                        <v-col cols="2" sm="6" md="5" lg="6"></v-col>
                        <v-col cols="2" sm="6" md="5" lg="6" style="display: flex; justify-content: flex-end">
                            <v-btn :disabled="password.length < 8 && password_again.length < 8" @click="changePassword"
                                class="ma-0" text v-if="editCardOn.data">
                                Изменить пароль
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </div>
        <div class="card__footer" v-if="addCardOn_.data">
            <v-btn text @click="$emit('notVisableCard'); addCardOn_.data = !addCardOn_.data" color="#787878">ОТМЕНА
            </v-btn>
            <v-btn text @click="addNewFeature()" color="#787878">Создать</v-btn>
        </div>
        <div class="card__footer" v-else-if="editCardOn.data">
            <v-btn @click="changeItem(isOldItem = !isOldItem)"
                v-if="newData.filter(el => el.id === objectForCard.id).length" color="#0F0CA7" text
                style="margin-right: 15px !important">
                оригинал
            </v-btn>

            <v-btn v-if="allListItem[0] != user" text color="#787878"
                @click="$emit('notVisableCard'); editCardOn_.data = !editCardOn_.data"
                style="margin-right: 15px !important">
                ОТМЕНА
            </v-btn>
            <v-btn text @click="editObject()" color="#787878">применить</v-btn>

        </div>
    </div>
</template>
<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import ExpansionPanelForCard from './ExpansionPanelForCard.vue'
import FormForDynamicField from './FormForDynamicField.vue';
import { v4 as uuidv4 } from 'uuid';

export default {
    name: 'StandartFormCard',
    components: {
        ExpansionPanelForCard,
        FormForDynamicField,
    },
    props: ['objectForCard_', 'infoCardOn', 'editCardOn', 'addCardOn', 'editMode', 'cardVisable'],
    data() {
        return {
            objectForCard: this.objectForCard_,
            editCardOn_: this.editCardOn,
            addCardOn_: this.addCardOn,
            infoCardOn_: this.infoCardOn,
            rules: {
                required: value => !!value || 'Обязательное поле',
                min: v => v !== undefined ? v.length >= 8 : !!v || 'Минимум 8 символов',
            },
            snackbar: false,
            offPointsFlag_: false,
            isOldItem: false,
            errorMessege: '',
            password: '',
            password_again: '',
            types: ['Point', 'LineString', 'Polygon'],
            postIndex: null, 
            pointIndex: null,
        }
    },
    watch: {
        snackbar: {
            handler() {
                if (!this.snackbar) {
                    this.updateError(null);
                }
            }
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
        offPointsFlag_: {
            handler() {
                this.setOffPointsFlag(this.offPointsFlag_)
            }
        },
        objectForCard_: {
            handler() {
                this.objectForCard = this.objectForCard_;
            }
        }
    },
    computed: {
        ...mapGetters(['allListItem', 'user', 'typeForFeature', 'actions', 'newData'])
    },
    methods: {
        ...mapActions(['setOffPointsFlag', 'putObject', 'deleteObject', 'postObject']),
        ...mapMutations(['updateArrayEditMode', 'updateObjectForCard', 'updateError', 'deleteItemFromNewData']),
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
                if (!this.checkCorrectFields()) {
                    return;
                }

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
                this.$emit('notVisableCard');
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
                object.properties = { ...object, ...object.properties };

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
            if (this.offPointsFlag_ && this.objectForCard.geometry.type === 'Point') {
                this.updateArrayEditMode({ item: this.objectForCard, type: 'offPoints' })
            }
        },
        async deleteObjectOnCard() {
            if (this.actions === 'getFeatures') {
                this.updateArrayEditMode({ item: this.objectForCard, type: 'delete' })
            }
            else {
                this.deleteObject(this.objectForCard.id)
            }
            this.infoCardOn_.data = !this.infoCardOn_.data;
            this.$emit('notVisableCard');

            if (this.objectForCard.geometry.type === 'Point') {
                let havePointInLinePost = []
                this.arrayEdit.post.forEach((element, index) => {
                    if (element.geometry.type === 'LineString') {
                        havePointInLinePost.push(element.geometry.coordinates.some((el) => {
                            if (el[0] === this.objectForCard.geometry.coordinates[0] && el[1] === this.objectForCard.geometry.coordinates[1]) {
                                this.postIndex = index
                                return el[0] === this.objectForCard.geometry.coordinates[0] && el[1] === this.objectForCard.geometry.coordinates[1]
                            }
                        }))
                    }
                });
                havePointInLinePost = havePointInLinePost.some((el) => {
                    return el
                })

                if (havePointInLinePost) {
                    this.arrayEdit.post[this.postIndex].geometry.coordinates.forEach((coord, index) => {
                        if (coord[0] === this.objectForCard.geometry.coordinates[0] && coord[1] === this.objectForCard.geometry.coordinates[1]) {
                            this.pointIndex = index
                        }
                    });
                    if (this.pointIndex != this.arrayEdit.post[this.postIndex].geometry.coordinates.length && this.pointIndex != 0) {
                        this.arrayEdit.post[this.postIndex].geometry.coordinates.splice(this.pointIndex, 1)
                    }
                } else {
                    let havePointInLinePut = []
                    this.arrayEdit.put.forEach((element, index) => {
                        if (element.geometry.type === 'LineString') {
                            havePointInLinePut.push(element.geometry.coordinates.some((el) => {
                                if (el[0] === this.objectForCard.geometry.coordinates[0] && el[1] === this.objectForCard.geometry.coordinates[1]) {
                                    this.postIndex = index
                                    return el[0] === this.objectForCard.geometry.coordinates[0] && el[1] === this.objectForCard.geometry.coordinates[1]
                                }
                            }))
                        }
                    });
                    havePointInLinePut = havePointInLinePut.some((el) => {
                        return el
                    })

                    if (havePointInLinePut) {
                        this.arrayEdit.put[this.postIndex].geometry.coordinates.forEach((coord, index) => {
                            if (coord[0] === this.objectForCard.geometry.coordinates[0] && coord[1] === this.objectForCard.geometry.coordinates[1]) {
                                this.pointIndex = index
                            }
                        });

                        if (this.pointIndex != this.arrayEdit.put[this.postIndex].geometry.coordinates.length && this.pointIndex != 0) {
                            this.arrayEdit.put[this.postIndex].geometry.coordinates.splice(this.pointIndex, 1)
                        }
                        console.log(this.arrayEdit.put[this.postIndex].geometry.coordinates)
                    }


                }

            }

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
       
        editOn() {
            this.editCardOn_.data = !this.editCardOn_.data;
            this.infoCardOn_.data = !this.infoCardOn_.data;
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
        }
    }
}
</script>

<style>
.card__footer {
    display: flex;
    position: absolute;
    z-index: 1;
    left: 0;
    right: 0;
    bottom: 0;
    justify-content: flex-end;
    border-top: 1px solid #E0E0E0;
    border-radius: 0 0 12px 12px !important;
    background-color: white;
}

.form_for_card{
    padding: 24px;
    position: absolute;
    bottom: 0;
    top: 37.53%;
    left: 0;
    right: 0;
    overflow: hidden scroll;
}

.edit_form{
    bottom: 69px !important;
    padding: 24px 24px 0 24px !important;
}

.btn {
    background-color: white !important;
}

.btn_disabled {
    opacity: 0.5;
}
</style>