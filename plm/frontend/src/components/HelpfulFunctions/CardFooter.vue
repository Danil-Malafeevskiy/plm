<template>
    <div class="card__footer">
        <template v-if="addCardOn.data">
            <v-btn text @click="$emit('notVisableCard'); addCardOn_.data = !addCardOn_.data" color="#787878">ОТМЕНА
            </v-btn>
            <v-btn text @click="addNewFeature()" color="#787878">Создать</v-btn>
        </template>
        <template v-else-if="editCardOn.data">
            <v-btn v-if="allListItem[0] != user" text color="#787878"
                @click="$emit('notVisableCard'); editCardOn_.data = !editCardOn_.data"
                style="margin-right: 15px !important">
                ОТМЕНА
            </v-btn>
            <v-btn text @click="editObject()" color="#787878">применить</v-btn>
        </template>
    </div>
</template>
<script>
import { v4 as uuidv4 } from 'uuid';
import { mapGetters, mapMutations, mapActions } from 'vuex';

export default {
    name: 'CardFooter',
    props: ['infoCardOn', 'editCardOn', 'addCardOn', 'objectForCard_'],
    data() {
        return {
            editCardOn_: this.editCardOn,
            addCardOn_: this.addCardOn,
            infoCardOn_: this.infoCardOn,
            objectForCard: this.objectForCard_,
        }
    },
    watch: {
        objectForCard_() {
            this.objectForCard = this.objectForCard_;
        },
    },
    computed: {
        ...mapGetters(['allListItem', 'user'])
    },
    methods: {
        ...mapActions(['putObject', 'deleteObject', 'postObject']),
        ...mapMutations(['updateArrayEditMode', 'updateObjectForCard', 'updateError', 'deleteItemFromNewData']),
        async addNewFeature() {
            if (this.objectForCard.name && typeof this.objectForCard.name === 'number') {
                if (!this.objectForCard.geometry.coordinates.length) {
                    this.$emit('showSnacker', 'Создайте объект на карте!');
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
                this.$emit('showSnacker', this.error);
                return;
            }
            else {
                this.addCardOn_.data = !this.addCardOn_.data;
                this.$emit('notVisableCard');
            }
        },
        async editObject() {
            if ('type' in this.objectForCard) {
                console.log(this.objectForCard.geometry.coordinates);
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
                this.$emit('showSnacker', this.error);
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
        checkCorrectFields() {
            if ('groups' in this.objectForCard) {
                for (let key in this.objectForCard.properties) {
                    if (key !== 'password' && key != 'email' && this.objectForCard.properties[key] === '') {
                        this.$emit('showSnacker', 'Обязательные поля не могут быть пустыми');
                        return false;
                    }
                    else if (key === 'password' && this.objectForCard.properties[key].length < 8) {
                        this.$emit('showSnacker', 'Пароль не может юыть меньше 8 символов');
                        return false;
                    }
                }
                if (!this.objectForCard.groups.length) {
                    this.$emit('showSnacker', 'Выберите группы');
                    return false;
                }

                else if (!this.objectForCard.properties.email.toLowerCase()
                    .match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
                    this.$emit('showSnacker', 'Некорректный email');
                    return false;
                }
            }

            else if ('headers' in this.objectForCard.properties) {
                if (!this.objectForCard.properties.name) {
                    this.$emit('showSnacker', 'Введите имя типа');
                    return false;
                }
                else if (!this.objectForCard.properties.type) {
                    this.$emit('showSnacker', 'Введите тип геометрии');
                    return false;
                }
                else if (!this.objectForCard.properties.headers.length) {
                    this.$emit('showSnacker', 'Добавьте основные атрибуты');
                    return false;
                }
                else if (this.checkDoubleFields(this.objectForCard.properties)) {
                    this.$emit('showSnacker', 'Не может быть атрибутов с одинаковыми именами');
                    return false;
                }
                this.objectForCard.properties.image = this.objectForCard.image;
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
    z-index: 5;
    left: 0;
    right: 0;
    bottom: 0;
    justify-content: flex-end;
    border-top: 1px solid #E0E0E0;
    border-radius: 0 0 12px 12px !important;
    background-color: white;
}
</style>