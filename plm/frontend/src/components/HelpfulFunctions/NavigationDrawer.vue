<template>
    <v-navigation-drawer app color="#DDDDDD" permanent
        style="max-width: 18.96% !important; min-width: 18.96% !important;">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title>
                    <v-btn @click="showCard = !showCard" class="pa-0 ma-0 btn_menu" elevation="0" fab depressed
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

                Типы {{ fiteredAllTypes.length }}

                <v-autocomplete @click:clear="clear" clearable v-click-outside="clear" id='search' dense append-icon
                    hide-details hint="Поиск" hide-no-data solo label="Поиск" @update:search-input="search">
                </v-autocomplete>


            </p>

            <v-list-item-group class="object__data" v-model="selectedItem" color="#E93030">

                <v-list-item class="pa-3" v-for="key in fiteredAllTypes" :key="key.id" link @click="changeObject(key)"
                    style="border-radius: 8px !important;">

                    <v-list-item-title class="pa-1">
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
            fiteredAllTypes: [],
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
            }
        },

        getList: {
            handler() {
                this.selectedItem = null;
            }

        },
        allType: {
            handler() {
                if (this.fiteredAllTypes.length === 0) {
                    this.clear();
                }
                else {
                    const searchText = document.querySelector('#search').value;
                    this.fiteredAllTypes = this.allType.filter(el => el.name.toLowerCase().includes(searchText.toLowerCase()));
                }
            }
        }
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
        },
        search(searchText) {
            if (searchText != null) {
                this.fiteredAllTypes = this.allType.filter(el => el.name.toLowerCase().includes(searchText.toLowerCase()));
                if (this.fiteredAllTypes.lenght === 0) {
                    this.clear()
                }
            }
        },
        clear() {
            this.fiteredAllTypes = this.allType;
        },
    },
    components: { CardInLeftPanel }
}
</script>

<style>
.btn_menu {
    background-color: #DDDDDD !important;
    width: 28px !important;
    height: 28px !important;
    position: absolute;
    bottom: 9px;
}

.text_in_span {
    margin-left: 35px;
}
</style>