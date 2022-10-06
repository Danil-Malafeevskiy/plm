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

        <CardInLeftPanel v-show="showCard" :resetSelectItem="resetSelectItem" :visableCard="visableCard"
            :editCardOn="editCardOn" :visableVersions="visableVersions" :notVisableVersions="notVisableVersions"
            :versionsPage="versionsPage" :infoCardOn="infoCardOn" />

        <v-list dense nav>
            <p
                style="display: flex; font-size: 16px; color: #5E5E5E; justify-content: space-between; align-items: center;">
                Типы {{ fiteredAllTypes.length }}
                <v-autocomplete @click:clear="clear" multiple clearable id='search' dense append-icon hide-details
                    hint="Поиск" hide-no-data solo label="Поиск" @update:search-input="search">
                </v-autocomplete>
            </p>
            <v-slide-y-transition>
                <v-list-item-group v-if="fiteredAllTypes.length" class="object__data" v-model="selectedItem"
                    color="#E93030">
                    <v-list-item class="pa-3" v-for="key in fiteredAllTypes" :key="key.id" link
                        style="border-radius: 8px !important;" @click="changeObject(key)">
                        <v-list-item-title class="pa-1" v-if="typeof key === 'object'">
                            <div class="name">
                                <div>{{ key.name }}</div>
                                <template v-if="'all_obj' in key">
                                    <div v-if="key.group in arrayEditMode"
                                        style="font-size: 16px; color: #A5A5A6; margin-left: auto;">
                                        {{key.all_obj + arrayEditMode[key.group].post.filter(el => el.name ===
                                        key.id).length}}
                                    </div>
                                    <div v-else style="font-size: 16px; color: #A5A5A6; margin-left: auto;">
                                        {{key.all_obj}}
                                    </div>
                                </template>
                                <template v-else-if="'all_user' in key && actions !== 'getTypeObject'">
                                    <div style="font-size: 16px; color: #A5A5A6; margin-left: auto;">{{key.all_user}}
                                    </div>
                                </template>
                                <template v-else-if="'all_type' in key && actions === 'getTypeObject'">
                                    <div style="font-size: 16px; color: #A5A5A6; margin-left: auto;">{{key.all_type}}
                                    </div>
                                </template>
                            </div>
                        </v-list-item-title>
                        <v-list-item-title class="pa-1" v-else>
                            <div>{{ key }}</div>
                        </v-list-item-title>
                    </v-list-item>
                </v-list-item-group>
            </v-slide-y-transition>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';
import CardInLeftPanel from './CardInLeftPanel.vue';

export default {
    name: "CardInfo",
    comments: {
        CardInLeftPanel
    },
    props: ['addCardOn', 'visableCard', 'editCardOn', 'visableVersions', 'notVisableVersions', 'versionsPage', 'infoCardOn'],
    data() {
        return {
            selectedItem: null,
            showCard: false,
            fiteredAllTypes: [],
            objectType: null,
        };
    },
    watch: {
        selectedItem: {
            async handler(newValue, oldValue) {
                if (this.selectedItem != null) {
                    if (document.querySelector('.text_in_span').innerHTML === "Пользователи") {
                        this.updateAction({
                            actionGet: 'getUsersOfGroup',
                            actionPost: 'postUser',
                            actionOneGet: 'getOneUser',
                            actionPut: 'putUser',
                            actionDelete: 'deleteUser',
                        });
                        if (oldValue === null) {
                            const object = {
                                properties: {
                                    first_name: "",
                                    last_name: "",
                                    email: "",
                                },
                                groups: [],
                                permissions: [],
                            }
                            this.upadateEmptyObject(object);
                        }
                    }
                }
                else {
                    this.upadateTitle('');
                    let domItem = document.querySelector('.text_in_span').innerHTML;
                    if (domItem === "Пользователи") {
                        const headers = [
                            {
                                "text": "id",
                                "align": "start",
                                "value": "id",
                                "sortable": false
                            },
                            {
                                "text": "name",
                                "value": "name"
                            }
                        ];
                        this.updateAction({
                            actionGet: 'getAllGroups',
                            actionPost: 'postGroup',
                            actionOneGet: 'getGroup',
                            actionPut: 'putGroup',
                            actionDelete: 'deleteGroup',
                        });
                        this.updateListItem({ items: this.allGroups });
                        this.updateHeaders(headers);
                        if (oldValue === null) {
                            const object = {
                                properties: {
                                    name: '',
                                },
                            }
                            this.upadateEmptyObject(object);
                        }
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
                    if (this.allType.length && typeof this.allType[0] === 'object') {
                        this.fiteredAllTypes = this.allType.filter(el => el.name.toLowerCase().includes(searchText.toLowerCase()));
                    }
                    else {
                        this.fiteredAllTypes = this.allType.filter(el => el.toLowerCase().includes(searchText.toLowerCase()));
                    }
                }
            }
        }
    },
    computed: { ...mapGetters(['allFeatures', 'getList', 'allType', 'emptyObject', 'allGroups', 'oneType', 'arrayEditMode', 'actions', 'getToolbarTitle']) },
    methods: {
        ...mapActions(['getGroup', 'getTypeObject', 'getUsersOfGroup', 'filterForFeature', 'getOneTypeObjectForFeature', 'getAllTypeInGroup', 'getFilteredVersions']),
        ...mapMutations(['upadateEmptyObject', 'updateHeaders', 'updateDrawType', 'updateAction', 'upadateTitle',
            'updateListType', 'updateListItem']),
        getOneGroup(id) {
            this.getGroup(id);
        },

        async changeObject(objectType) {
            if (this.getToolbarTitle != objectType.name) {
                this.objectType = objectType;
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
                            "text": "full_name",
                            "value": "full_name"
                        },
                        {
                            "text": "email",
                            "value": "email"
                        }
                    ];
                    this.updateHeaders(headers);
                    this.getUsersOfGroup(objectType);
                }
                else if (domItem === "Типы объектов") {
                    console.log(objectType);
                    this.getAllTypeInGroup(objectType.name);
                }
                else if (domItem === "Версии системы") {
                    this.getFilteredVersions(objectType);
                }
                else {
                    await this.getOneTypeObjectForFeature({ id: objectType.id });
                    this.objectType = this.oneType;
                    this.updateHeaders(this.objectType.headers);
                    this.updateDrawType(this.objectType.type);
                    await this.filterForFeature(this.objectType.id);
                }
            }
        },
        resetSelectItem() {
            setTimeout(() => { this.showCard = !this.showCard; });
            this.selectedItem = null;
        },
        search(searchText) {
            if (searchText != null) {
                this.fiteredAllTypes = this.allType.filter(el => el.name.toLowerCase().includes(searchText.toLowerCase()));
            }
        },
        clear() {
            this.fiteredAllTypes = this.allType;
        },
    },
    components: { CardInLeftPanel },
    mounted() {
        setTimeout(async () => {
            await this.getTypeObject();
        }, 500);
    },
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


.name {
    display: flex;
}
</style>