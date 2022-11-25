<template>
    <v-slide-y-transition>
        <v-card class="card_test" style="z-index: 2 !important;">
            <v-list dense nav>
                <v-list-item-group class="menu" v-model="selectedItem" mandatory color="#E93030">
                    <v-list-item v-if="user && user.is_staff">
                        <v-list-item-title>
                            Пользователи
                        </v-list-item-title>
                    </v-list-item>
                    <v-list-item v-if="user && user.is_staff">
                        <v-list-item-title>
                            Типы объектов
                        </v-list-item-title>
                    </v-list-item>

                    <v-list-item v-if="user">
                        <v-list-item-title>
                            Версии системы
                        </v-list-item-title>
                    </v-list-item>

                    <v-list-item v-if="user">
                        <v-list-item-title>
                            База объектов
                        </v-list-item-title>
                    </v-list-item>

                    <v-list-item v-if="user">
                        <v-list-item-title>
                            <v-avatar color="#72ABEA" size="35">
                                <span v-if="!(user.image)" class="white--text text-h11">
                                    {{ user.first_name.slice(0, 1) }}{{ user.last_name.slice(0, 1) }}
                                </span>
                                <img v-else :src="user.image">
                            </v-avatar>

                            {{ user.first_name }} {{ user.last_name }}
                        </v-list-item-title>

                        <v-list-item-icon @click="logOutAndResolve()">
                            <v-icon>mdi-logout-variant</v-icon>
                        </v-list-item-icon>

                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-card>
    </v-slide-y-transition>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';
export default {
    name: 'CardInLeftPanel',
    props: ['resetSelectItem', 'visableCard', 'editCardOn', 'visableVersions', 'notVisableVersions', 'versionsPage', 'infoCardOn'],
    data() {
        return {
            selectedItem: 3,
            initials: null,
            editCardOn_: this.editCardOn,
            groupsOfUser: [],
            infoCardOn_: this.infoCardOn,
        }
    },
    watch: {
        selectedItem: {
            async handler() {
                this.updatefilterForFeature([]);
                this.upadateTitle('');
                if (this.selectedItem != null) {
                    setTimeout(() => {
                        document.querySelector('.text_in_span').innerHTML = document.querySelector('.v-item--active .v-list-item__title').innerText;
                    })
                    if (this.user.is_staff || this.user.is_superuser) {
                        switch (this.selectedItem) {
                            case 0: {
                                this.onGroups();
                                break;
                            }
                            case 1: {
                                this.onDataSet();
                                break;
                            }
                            case 2: {
                                this.onVersions();
                                break;
                            }
                            case 3: {
                                this.onFeatures();
                                break;
                            }
                            case 4: {
                                this.onUser();
                                break;
                            }
                        }
                    }
                    else {
                        switch (this.selectedItem) {
                            case 1: {
                                this.onFeatures();
                                break;
                            }
                            case 2: {
                                this.onUser();
                                break;
                            }
                            case 0: {
                                this.onVersions();
                                break;
                            }
                        }
                    }
                    await this.resetSelectItem();
                }
            }
        },
    },
    computed: mapGetters(['allFeatures', 'user', 'allGroups', 'getList', 'allType', 'actions', 'getObjectForCard', 'allVersions', 'allUserGroups']),
    methods: {
        ...mapActions(['logOut', 'getAllGroups', 'getTypeObject', 'getOneObject', 'getVersions', 'getAllTypeForTable', 'allGroupForNav', 'getUser']),
        ...mapMutations(['updatefilterForFeature', 'updateList', 'updateListItem', 'upadateEmptyObject',
            'updateAction', 'updateHeaders', 'updateListType', 'updateNameForArray', 'updateOneType', 'upadateTitle', 'updateVersions', 'updateAllUserGroups']),
        logOutAndResolve() {
            this.logOut();
            location.reload();
        },
        async onUser() {
            this.notVisableVersions()
            this.updateAction({
                actionOneGet: 'getOneUser',
                actionPut: 'putUser',
            });
            this.updateListType([]);
            this.updateListItem({ items: [this.user] });
            setTimeout(() => {
                this.infoCardOn_.data = true;
                this.visableCard();
            }, 500)
        },
        onFeatures() {
            this.notVisableVersions()
            this.updateNameForArray('База объектов');
            this.updateListType([]);
            this.getTypeObject();
            this.updateAction({
                actionGet: 'getFeatures',
                actionOneGet: 'getOneFeature',
                actionPost: 'postFeature',
                actionPut: 'putFeature',
                actionDelete: 'deleteFeature',
            });
        },
        onDataSet() {
            this.notVisableVersions();
            this.updateListType([]);
            this.updateNameForArray('Типы объектов');
            let object = {
                properties: {
                    name: '',
                    type: '',
                    headers: [],
                    properties: [],
                    group: '',
                    all_group_type: [],
                    group_type: [],
                    ruls: [],
                },
                image: '',
            }
            let headers = [
                {
                    "text": "name",
                    "value": "name",
                },
            ];
            this.updateHeaders(headers);
            this.updateAction({
                actionGet: 'getTypeObject',
                actionPost: 'postTypeObject',
                actionOneGet: 'getOneTypeObject',
                actionPut: 'putTypeObject',
                actionDelete: 'deleteTypeObject',
            });
            this.allGroupForNav();
            this.upadateEmptyObject(object);
        },
        onGroups() {
            this.notVisableVersions()
            this.updateNameForArray('Пользователи');
            this.updateListType([]);
            let headers = [
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
            let object = {
                properties: {
                    name: '',
                },
            }
            this.upadateEmptyObject(object);
            this.updateHeaders(headers);
            this.updateAction({
                actionGet: 'getAllGroups',
                actionPost: 'postGroup',
                actionOneGet: 'getGroup',
                actionPut: 'putGroup',
                actionDelete: 'deleteGroup',
            });
            this.getAllGroups();
        },
        onVersions() {
            this.visableVersions()
            this.updateListType([]);
            this.updateAction({
                actionGet: '',
                actionPost: '',
                actionOneGet: '',
                actionPut: '',
                actionDelete: '',
            });
            this.updateListType(this.groupsOfUser);
            this.updateNameForArray('Версии системы');
        },
    },
    async mounted() {
        await this.getUser();
        if ('groups' in this.user) {
            this.groupsOfUser = [...this.user.groups];
        }
        if(!this.user.is_staff && !this.user.is_superuser){
            this.selectedItem = 1;
        }
    }
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

.card_test {
    font-size: 16px !important;
    left: 16px !important;
    right: 16px !important;
    top: 50px !important;
    position: fixed;
    z-index: 1 !important;
    border-radius: 4px !important;
    box-shadow: 0px 8px 10px rgba(0, 0, 0, 0.14), 0px 3px 14px rgba(0, 0, 0, 0.12), 0px 5px 5px rgba(0, 0, 0, 0.2);
}
</style>