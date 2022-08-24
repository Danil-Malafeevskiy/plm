<template>
    <v-card class="card_of_object" v-show="cardVisable_.data === true">
        <div class="card__window">
            <p style="display: none;">{{ emptyObject }}</p>
            <p style="display: none">{{ getObjectForCard }}</p>
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

                            <div v-for="(f, index) in emptyObject.properties" :key="f.number_support"
                                v-show="index === 'username'" class="ma-1" style="width: 100%">
                                <div v-if="index === 'username'">
                                    <v-expansion-panels  accordion flat class="pa-0 ma-0">
                                        <v-expansion-panel class="pa-0 ma-0">
                                            <v-expansion-panel-header class="pa-0 ma-0">
                                                Группы 
                                            </v-expansion-panel-header>

                                            <v-expansion-panel-content class="ma-0 pa-0">
                                                <v-row class="pa-2 ma-0">
                                                    <v-col v-for="(f, index) in userGroups" :key="f" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                        
                                                        <v-checkbox 
                                                            v-model="emptyObject.properties.groups"
                                                            :label="f"
                                                            :value="userGroups[index]"
                                                            class="ma-2"
                                                            color="#E93030"
                                                            
                                                            style="
                                                                min-height: 37.53% !important; 
                                                                max-height: 37.53% !important;
                                                            " 
                                                            >
                                                        </v-checkbox>
                                                    </v-col>
                                                </v-row>
                                            </v-expansion-panel-content>

                                        </v-expansion-panel>

                                        <v-expansion-panel  class="pa-0 ma-0" >
                                            <v-expansion-panel-header class="pa-2" >
                                                Права
                                            </v-expansion-panel-header>
                                            
                                            <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                <v-expansion-panels  accordion flat class="pa-0 ma-0">
                                                    <v-expansion-panel v-for="el in groups" id="permission" :key="el" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">

                                                        <v-expansion-panel-header class="pa-0 ma-0" style="margin-left: 0.5em !important;">
                                                            {{el}}
                                                        </v-expansion-panel-header>

                                                        <v-expansion-panel-content  class="ma-0 pa-0">
                                                            <div v-for="(name, index) in permissionList" :key="name" class="pa-0 ma-0">
                                                                <v-checkbox 
                                                                    v-if="name.includes(el[0].toLowerCase() + el.slice(1))"
                                                                    v-model="emptyObject.properties.user_permissions"
                                                                    class="ma-2"
                                                                    color="#E93030"
                                                                    :value="permissionList[index]"
                                                                    style="
                                                                        min-height: 37.53% !important; 
                                                                        max-height: 37.53% !important;
                                                                    " 
                                                                    :label="name">
                                                                </v-checkbox>
                                                            </div>
                                                            
                                                        </v-expansion-panel-content>

                                                    </v-expansion-panel>
                                                </v-expansion-panels>
                                                
                                            </v-expansion-panel-content>

                                        </v-expansion-panel>
                                    </v-expansion-panels>

                                </div>
                                <div v-else style="display: none;"></div>
                            </div>
                            
                        </v-row>
                        <v-row justify="start" v-else-if="infoCardOn_.data">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text v-if="getObjectForCard.name != null" class="pa-0" style="font-size: 24px;">
                                    {{ oneType }}
                                </v-card-text>
                                <v-card-text v-else-if="getObjectForCard.properties.username != null" class="pa-0"
                                    style="font-size: 24px;">{{
                                    getObjectForCard.properties.username
                                    }}
                                </v-card-text>
                                <v-card-text v-else class="pa-0" style="font-size: 24px;">{{
                                    getObjectForCard.properties.name
                                    }}
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
                            <v-col v-for="(f, index) in getObjectForCard.properties" :key="index"
                                v-show="typeof (f) != 'boolean' && index != 'name_tap' && index != 'id' && index != 'username'"
                                cols="2" sm="6" md="5" lg="6">

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
                            <div v-for="(f, index) in getObjectForCard.properties" :key="f.number_support"
                                v-show="index === 'username'" class="ma-1" style="width: 100%">
                                <div v-if="index === 'username'">
                                    <v-expansion-panels  accordion flat class="pa-0 ma-0">
                                        <v-expansion-panel class="pa-0 ma-0">
                                            <v-expansion-panel-header class="pa-2">
                                                Группы 
                                            </v-expansion-panel-header>

                                            <v-expansion-panel-content class="ma-0 pa-0">
                                                <v-row class="pa-2 ma-0">
                                                    <v-col v-for="(f, index) in getObjectForCard.groups" v-show="index != 'id'" :key="f.username" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                        <v-checkbox 
                                                            :v-model="getObjectForCard.groups[index]"
                                                            class="ma-2"
                                                            color="#E93030"
                                                            readonly
                                                            :input-value="f === f" 
                                                            style="
                                                                min-height: 37.53% !important; 
                                                                max-height: 37.53% !important;
                                                            " 
                                                            :label="f">
                                                        </v-checkbox>
                                                    </v-col>
                                                    <v-col v-for="(f, index) in getObjectForCard.avaible_group" v-show="index != 'id'" :key="f.username" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                        <v-checkbox 
                                                            :v-model="getObjectForCard.avaible_group[index]"
                                                            class="ma-2"
                                                            color="#E93030"
                                                            readonly
                                                            :input-value="f != f"  
                                                            style="
                                                                min-height: 37.53% !important; 
                                                                max-height: 37.53% !important;
                                                            " 
                                                            :label="f">
                                                        </v-checkbox>
                                                    </v-col>
                                                </v-row>
                                            </v-expansion-panel-content>

                                        </v-expansion-panel>


                                        <v-expansion-panel  class="pa-0 ma-0" @click="groupsPermissions()">
                                            <v-expansion-panel-header class="pa-2">
                                                Права
                                            </v-expansion-panel-header>
                                            
                                            <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                <v-expansion-panels accordion flat class="pa-0 ma-0">
                                                    <v-expansion-panel v-for="el in groups" id="permission" :key="el" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">

                                                        <v-expansion-panel-header class="pa-0 ma-0" style="margin-left: 0.5em !important;">
                                                            {{el}}
                                                        </v-expansion-panel-header>

                                                        <v-expansion-panel-content  class="ma-0 pa-0">
                                                            <div v-for="name in getObjectForCard.user_permissions" :key="name">
                                                                <v-checkbox 
                                                                    v-if="name.includes(el[0].toLowerCase() + el.slice(1))"
                                                                    :v-model="getObjectForCard.user_permissions[index]"
                                                                    class="ma-2"
                                                                    color="#E93030"
                                                                    readonly
                                                                    :input-value="name === name"  
                                                                    style="
                                                                        min-height: 37.53% !important; 
                                                                        max-height: 37.53% !important;
                                                                    " 
                                                                    :label="name">
                                                                </v-checkbox>
                                                            </div>
                                                            <div v-for="name in getObjectForCard.avaible_user_permission" :key="name">
                                                                <v-checkbox 
                                                                    v-if="name.includes(el[0].toLowerCase() + el.slice(1))"
                                                                    :v-model="getObjectForCard.user_permissions[index]"
                                                                    class="ma-2"
                                                                    color="#E93030"
                                                                    readonly
                                                                    :input-value="name != name"  
                                                                    style="
                                                                        min-height: 37.53% !important; 
                                                                        max-height: 37.53% !important;
                                                                    " 
                                                                    :label="name">
                                                                </v-checkbox>
                                                            </div>
                                                            
                                                            
                                                        </v-expansion-panel-content>

                                                    </v-expansion-panel>
                                                </v-expansion-panels>
                                                
                                            </v-expansion-panel-content>

                                        </v-expansion-panel>
                                    </v-expansion-panels>

                                </div>
                                <div v-else style="display: none;"></div>
                            </div>
                            
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
                            <div v-for="(f, index) in getObjectForCard.properties" :key="f.number_support"
                                v-show="index === 'username'" class="ma-1" style="width: 100%">
                                <div v-if="index === 'username'">
                                    <v-expansion-panels  accordion flat class="pa-0 ma-0">
                                        <v-expansion-panel class="pa-0 ma-0">
                                            <v-expansion-panel-header class="pa-2">
                                                Группы 
                                            </v-expansion-panel-header>

                                            <v-expansion-panel-content class="ma-0 pa-0">
                                                <v-row class="pa-2 ma-0">
                                                    <v-col v-for="(f, index) in userGroups" :key="f" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                        
                                                        <v-checkbox 
                                                            v-model="getObjectForCard.groups"
                                                            :label="f"
                                                            :value="userGroups[index]"
                                                            class="ma-2"
                                                            color="#E93030"
                                                            
                                                            style="
                                                                min-height: 37.53% !important; 
                                                                max-height: 37.53% !important;
                                                            " 
                                                            >
                                                        </v-checkbox>
                                                    </v-col>
                                                </v-row>
                                            </v-expansion-panel-content>

                                        </v-expansion-panel>

                                        <v-expansion-panel  class="pa-0 ma-0" @click="groupsPermissions()">
                                            <v-expansion-panel-header class="pa-2">
                                                Права
                                            </v-expansion-panel-header>
                                            
                                            <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                                <v-expansion-panels  accordion flat class="pa-0 ma-0">
                                                    <v-expansion-panel v-for="el in groups" :key="el" id="permission" cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">

                                                        <v-expansion-panel-header class="pa-0 ma-0" style="margin-left: 0.5em !important;">
                                                            {{el}}
                                                        </v-expansion-panel-header>

                                                        <v-expansion-panel-content  class="ma-0 pa-0">
                                                            <div v-for="(name, index) in permissionList" :key="name">
                                                                <v-checkbox 
                                                                    v-if="name.includes(el[0].toLowerCase() + el.slice(1))"
                                                                    v-model="getObjectForCard.user_permissions"
                                                                    class="ma-2"
                                                                    color="#E93030"
                                                                    :value="permissionList[index]"
                                                                    style="
                                                                        min-height: 37.53% !important; 
                                                                        max-height: 37.53% !important;
                                                                    " 
                                                                    :label="name">
                                                                </v-checkbox>
                                                            </div>
                                                            <!-- <div v-for="name in getObjectForCard.avaible_user_permission" :key="name">
                                                                <v-checkbox 
                                                                    v-if="name.includes(el)"
                                                                    v-model="getObjectForCard.avaible_user_permission"
                                                                    :value="getObjectForCard.avaible_user_permission[index]"
                                                                    class="ma-2"
                                                                    color="#E93030"
                                                                    style="
                                                                        min-height: 37.53% !important; 
                                                                        max-height: 37.53% !important;
                                                                    " 
                                                                    :label="name">
                                                                </v-checkbox>
                                                            </div> -->
                                                            
                                                            
                                                        </v-expansion-panel-content>

                                                    </v-expansion-panel>
                                                </v-expansion-panels>
                                                
                                            </v-expansion-panel-content>

                                        </v-expansion-panel>
                                    </v-expansion-panels>

                                </div>
                                <div v-else style="display: none;"></div>
                            </div>
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
            groups: [],         // Группы прав
            userGroups: [],
            permissionList: [], // список всех прав 
            
        }
    },
    watch: {
        cardVisable: {
            handler() {
                this.cardVisable_ = this.cardVisable;
                if (this.cardVisable_.data) {
                    // if (document.querySelector('.v-navigation-drawer').clientWidth * 100 / 1920 < 18) {
                         document.querySelector('.card_of_object').style.cssText = 'width: 38.05% !important; left: 60.28% !important;';
                    // }
                    // else {
                    //     document.querySelector('.card_of_object').style.cssText = 'width: 31.91% !important; left: 67.22% !important;';
                    // }
                }
            }, deep: true
        },
        getFeature: function () {
            this.feature = this.getFeature;
        },
        user: {
            handler(){
                console.log(this.user.avaible_group)
                this.userGroups = [...this.user.groups, ...this.user.avaible_group]
                this.permissionList = [...this.user.user_permissions, ...this.user.avaible_user_permission]
                this.groupsPermissions()
            },
            deep: true,
        } 
    },
    computed: {
        ...mapGetters(['getTypeId', 'filterFeature', 'getFeature', 'getObjectForCard', 'emptyObject', 'oneType', 'user']),
    },
    methods: {
        ...mapActions(['deleteObject', 'putObject', 'postObject', 'getOneObject', 'getAllObject']),
        ...mapMutations(['updateFunction']),
        async addNewFeature() {
            if (this.emptyObject.name != null) {
                this.emptyObject.name = this.getTypeId;
                console.log(this.emptyObject)
                await this.postObject([this.emptyObject]);
                this.filterForFeature();
                this.getAllObject();
            }
            else {
                await this.postObject(this.emptyObject.properties);
            }
            this.addCardOn_.data = !this.addCardOn_.data;
            this.notVisableCard();
        },
        async editObject() {
            await this.putObject(this.getObjectForCard);
            if(this.getObjectForCard.anme != null){
                this.filterForFeature();
                this.getAllObject();
            }
            this.getOneObject(this.getObjectForCard.id);
            this.editCardOn_.data = !this.editCardOn_.data;
            this.infoCardOn_.data = !this.infoCardOn_.data;
        },
        groupsPermissions() {
            for(let i =0; i < this.permissionList.length; ++i){
                let el = this.permissionList[i].split(" ").pop();
                el = el[0].toUpperCase() + el.slice(1);
                this.groups.push(el);
            }
            // for (let i = 0; i < this.getObjectForCard.avaible_user_permission.length; ++i) {
            //     this.groups.push(this.getObjectForCard.avaible_user_permission[i].split(" ").pop());
            // }
            this.groups = [...new Set(this.groups)]
        }
    },

    mounted(){
        var el = document.querySelector('v-label').innerHTML
        console.log(el)
    },
}
</script>

<style>

#permission{
    margin-top: 0 !important;
    margin-left: 1em !important;
}

.v-expansion-panel-content__wrap{
    padding: 0 !important;
}

.v-application--is-ltr .v-expansion-panel-header__icon{
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