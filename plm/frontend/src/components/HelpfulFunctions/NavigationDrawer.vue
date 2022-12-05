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
            <p v-if="actions === 'getFeatures'"
                style="display: flex; font-size: 16px; color: #5E5E5E; justify-content: space-between; align-items: center;">
                Типы {{ fiteredAllTypes.length }}
                <v-autocomplete @click:clear="clear" multiple clearable id='search' dense append-icon hide-details
                    hint="Поиск" hide-no-data solo label="Поиск" @update:search-input="search">
                </v-autocomplete>
            </p>
            <p v-else
                style="display: flex; font-size: 16px; color: #5E5E5E; justify-content: space-between; align-items: center;">
                Группы {{ fiteredAllTypes.length }}
                <v-autocomplete @click:clear="clear" multiple clearable id='search' dense append-icon hide-details
                    hint="Поиск" hide-no-data solo label="Поиск" @update:search-input="search">
                </v-autocomplete>
            </p>
            <v-slide-y-transition>
                <v-list-item-group v-if="fiteredAllTypes.length" class="object__data" v-model="selectedItem"
                    color="#E93030" :mandatory="actions && actions !== 'getAllGroups' && actions != 'getUsersOfGroup'">
                    <v-list-item class="mb-2 pa-3" v-for="(key, index) in fiteredAllTypes" :key="key.id" link
                        style="border-radius: 8px !important;" @click="changeObject(key, index)">
                        <v-list-item-title style="z-index: 1" class="pa-1" v-if="typeof key === 'object'">
                            <div class="name">
                                <div>{{ key.name }} <span
                                        v-if="actions === 'getFeatures' && (user.groups.length > 1 || user.is_superuser)">({{ key.group }})</span>
                                </div>
                                <template v-if="'all_obj' in key">
                                    <div v-if="key.group in arrayEditMode"
                                        style="font-size: 16px; color: #A5A5A6; margin-left: auto;">
                                        {{ key.all_obj + arrayEditMode[key.group].post.filter(el => el.name ===
                                                key.id).length
                                        }}
                                    </div>
                                    <div v-else style="font-size: 16px; color: #A5A5A6; margin-left: auto;">
                                        {{ key.all_obj }}
                                    </div>
                                </template>
                                <template v-else-if="'all_user' in key && actions !== 'getTypeObject'">
                                    <div style="font-size: 16px; color: #A5A5A6; margin-left: auto;">{{ key.all_user }}
                                    </div>
                                </template>
                                <template v-else-if="'all_type' in key && actions === 'getTypeObject'">
                                    <div style="font-size: 16px; color: #A5A5A6; margin-left: auto;">{{ key.all_type }}
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
                    if (this.actions === "getAllGroups") {
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
                    if (this.actions === "getUsersOfGroup") {
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
                if (!this.fiteredAllTypes.length) {
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
        },
        actions: {
            handler() {
                if (this.fiteredAllTypes.length && this.actions !== 'getAllGroups') {
                    this.selectedItem = 0;
                    this.changeObject(this.fiteredAllTypes[0]);
                }
            }
        }
    },
    computed: { ...mapGetters(['allFeatures', 'getList', 'allType', 'emptyObject', 'allGroups', 'oneType', 'arrayEditMode', 'actions', 'getToolbarTitle', 'allTypeForTable', 'user']) 
                    
},
    methods: {
        ...mapActions(['getGroup', 'getTypeObject', 'getUsersOfGroup', 'filterForFeature', 'getOneTypeObjectForFeature', 'getAllTypeInGroup', 'getFilteredVersions']),
        ...mapMutations(['upadateEmptyObject', 'updateHeaders', 'updateDrawType', 'updateAction', 'upadateTitle',
            'updateListType', 'updateListItem']),
        getOneGroup(id) {
            this.getGroup(id);
        },

        async changeObject(objectType, index) {
            if (this.selectedItem != index) {
                this.objectType = objectType;
                this.upadateTitle({
                    title: typeof objectType === 'string' ? objectType : objectType.name,
                    group: 'group' in objectType ? objectType.groups : objectType
                });
                switch (this.actions) {
                    case 'getUsersOfGroup':
                    case 'getAllGroups': {
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
                        break;
                    }

                    case 'getTypeObject':
                        await this.getAllTypeInGroup(objectType.name);
                        console.log(this.allTypeForTable);
                        this.emptyObject.properties.all_group_type = this.allTypeForTable.map(el => el.name);
                        break;

                    case 'getFeatures':
                        await this.getOneTypeObjectForFeature({ id: objectType.id });
                        this.objectType = this.oneType;
                        this.updateDrawType(this.objectType.type);
                        this.filterForFeature(this.objectType.id);
                        break;

                    default:
                        this.getFilteredVersions(objectType);
                        break;
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
            if (this.fiteredAllTypes.length && this.actions !== 'getAllGroups') {
                this.selectedItem = 0;
                this.changeObject(this.fiteredAllTypes[0]);
            }
        }, 1000);
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
    font-weight: 500;
    margin-left: 35px;
    color: #787878;
}

.name {
    display: flex;
}

.v-list-item__title {
    z-index: 1 !important;
}

.theme--light.v-list-item--active:hover::before,
.theme--light.v-list-item--active::before {
    opacity: 1 !important;
    background-color: #FDEDED !important;
    border-radius: 8px !important;
    transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}
</style>