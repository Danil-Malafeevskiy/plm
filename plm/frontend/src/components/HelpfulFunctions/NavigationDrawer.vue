<template>
    <v-navigation-drawer app color="#DDDDDD" permanent
        style="max-width: 18.96% !important; min-width: 18.96% !important;">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title>
                    <v-btn @click="showCard = !showCard" class="ma-0 pa-0 btn_menu" elevation="0" fab depressed
                        retain-focus-on-click plain>
                        <v-icon left>mdi-menu</v-icon>
                    </v-btn>
                    <span class="text_in_span">База объектов</span>
                </v-list-item-title>
            </v-list-item-content>
        </v-list-item>

        <CardInLeftPanel v-show="showCard" :resetSelectItem="resetSelectItem" />

        <v-list dense nav>
            <p
                style="display: flex; font-size: 16px; color: #5E5E5E; justify-content: space-between; align-items: center;">

                Типы {{ allType.length }}

                <v-autocomplete @click:clear="clear()" id='search' dense append-icon hide-details hint="Поиск"
                    hide-no-data clearable solo label="Поиск">
                </v-autocomplete>


            </p>

            <v-list-item-group class="object__data" v-model="selectedItem" color="#E93030">

                <v-list-item v-for="key in allType" :key="key.id" link @click="changeObject(key)">

                    <v-list-item-title>
                        {{ key.name }}
                    </v-list-item-title>
                </v-list-item>
            </v-list-item-group>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';
//import $ from 'jquery'

import CardInLeftPanel from './CardInLeftPanel.vue';

export default {
    name: "CardInfo",
    comments: {
        CardInLeftPanel
    },
    data() {
        return {
            selectedTypeNameFeature: null,
            selectedItem: null,
            showCard: false,
        };
    },
    watch: {
        selectedItem: {
            handler() {
                if (this.selectedItem != null) {
                    if (document.querySelector('.text_in_span').innerHTML === "Пользователи") {
                        const object = {
                            properties: {
                                username: "",
                                password: "",
                            },
                            groups: [],
                            user_permissions: [],
                        }
                        this.upadateEmptyObject(object);
                        this.updateAction({
                            actionGet: 'getUsersOfGroup',
                            actionPost: 'postUser',
                            actionOneGet: 'getOneUser',
                            actionPut: 'putUser',
                            actionDelete: 'deleteUser',
                        });
                    }
                }
                // else {
                //     this.updateNameForArray('Пользователи');
                //     this.updateListType([]);
                //     let headers = [
                //         {
                //             "text": "id",
                //             "align": "start",
                //             "value": "id",
                //             "sortable": false
                //         },
                //         {
                //             "text": "name",
                //             "value": "name"
                //         }
                //     ];
                //     let object = {
                //         properties: {
                //             name: '',
                //         }
                //     }
                //     this.upadateEmptyObject(object);
                //     this.updateHeaders(headers);
                //     this.updateAction({
                //         actionGet: 'getAllGroups',
                //         actionPost: 'postGroup',
                //         actionOneGet: 'getGroup',
                //         actionPut: 'putGroup',
                //         actionDelete: 'deleteGroup',
                //     });
                //     this.getAllGroups();
                // }
            }
        },

        getList: {
            handler() {
                this.selectedItem = null;
            }

        },
    },
    computed: { ...mapGetters(['allFeatures', 'getList', 'allType', 'emptyObject', 'arrObjects']) },
    async mounted() {
        await this.getTypeObject();
    },

    methods: {
        ...mapActions(['getGroup', 'getTypeObject', 'getUsersOfGroup', 'filterForFeature', 'getAllGroups']),
        ...mapMutations(['upadateEmptyObject', 'updateHeaders', 'updateDrawType', 'updateAction', 'upadateTitle', 
                        'addArrayFromSelectedObject', 'updateNameForArray', 'updateListType']),
        getOneGroup(id) {
            this.getGroup(id);
        },

        async changeObject(objectType) {
            const domItem = document.querySelector('.text_in_span').innerHTML;
            this.upadateTitle(objectType.name);
            if (domItem === "Пользователи") {
                const headers = [
                    {
                        "text": "id",
                        "align": "start",
                        "value": "id",
                        "sortable": false
                    },
                    {
                        "text": "username",
                        "value": "username"
                    }
                ];
                this.updateHeaders(headers);
                this.getUsersOfGroup(objectType);
            }
            else {
                this.updateHeaders(objectType.headers);
                this.updateDrawType(objectType.type)
                await this.filterForFeature(objectType.id);

                for (let i in this.allFeatures) {
                    if (this.allFeatures[i].name === objectType.id) {
                        this.upadateEmptyObject(this.allFeatures[i]);
                        break;
                    }
                }
            }
        },

        resetSelectItem() {
            this.selectedItem = null;
            setTimeout(() => { this.showCard = !this.showCard; });
        }

        // clear() {
        //     this.getList.forEach(element => {
        //         $(".test:contains(" + element + "):hidden").show()
        //     });
        // },

        // search() {
        //     const value = document.getElementById('search').value;

        //     this.getList.forEach(element => {

        //         if (!element.toLowerCase().includes(value.toLowerCase())) {
        //             $("div:contains(" + element + "):last").parent().hide()
        //             $(".v-list-item:contains(" + element + "):last").hide()
        //         }

        //         else {
        //             $("div:contains(" + element + "):last").parent().show()
        //             $(".v-list-item:contains(" + element + "):last").show()
        //         }
        //     });
        // }
    },
    components: { CardInLeftPanel }
}
</script>

<style>
.btn_menu {
    background-color: #DDDDDD !important;
    width: 28px !important;
    height: 28px !important;
}

.btn_menu i {
    margin: 0 auto !important;
}
</style>