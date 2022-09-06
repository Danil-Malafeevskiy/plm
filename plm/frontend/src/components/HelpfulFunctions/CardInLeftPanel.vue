<template>
    <v-card class="card_test">
        <v-list dense nav>
            <v-list-item-group class="menu" v-model="selectedItem" color="#E93030">
                <v-list-item v-if="user.is_staff">
                    <v-list-item-title>
                        Пользователи
                    </v-list-item-title>
                </v-list-item>
                <v-list-item v-if="user.is_staff">
                    <v-list-item-title>
                        Типы объектов
                    </v-list-item-title>
                </v-list-item>
                <v-list-item v-if="user.is_staff">
                    <v-list-item-title>
                        База объектов
                    </v-list-item-title>
                </v-list-item>
                <v-list-item @click="logOutAndResolve()">
                    <v-list-item-title>
                        {{ user.username }}
                    </v-list-item-title>

                    <v-list-item-icon>
                        <v-icon>mdi-logout-variant</v-icon>
                    </v-list-item-icon>

                </v-list-item>
            </v-list-item-group>
        </v-list>
    </v-card>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';

export default {
    name: 'CardInLeftPanel',
    props: ['resetSelectItem'],
    data() {
        return {
            selectedItem: 2,
        }
    },
    watch: {
        selectedItem: {
            async handler() {
                this.updatefilterForFeature([]);
                this.upadateTitle('');
                if (this.selectedItem != null) {
                    if ((this.selectedItem != 3 && this.user.is_staff) || (this.selectedItem != 0 && this.user.is_active)) {
                        setTimeout(() => {
                            document.querySelector('.text_in_span').innerHTML = document.querySelector('.v-item--active .v-list-item__title').innerText;
                        })
                    }
                    this.resetSelectItem();
                    switch (this.selectedItem) {
                        case 0: {
                            this.onUsers();
                            break;
                        }
                        case 1: {
                            this.onDataSet();
                            break;
                        }
                        case 2:
                            this.onFeatures();
                            break;
                    }
                }
            }
        }
    },
    computed: mapGetters(['allFeatures', 'user', 'allGroups', 'getList', 'allType', 'actions']),
    methods: {
        ...mapActions(['logOut', 'getAllGroups', 'getTypeObject']),
        ...mapMutations(['updatefilterForFeature', 'updateList', 'updateListItem', 'upadateEmptyObject',
            'updateAction', 'updateHeaders', 'updateListType', 'updateNameForArray', 'updateOneType', 'upadateTitle']),
        logOutAndResolve() {
            this.logOut();
            location.reload();
        },
        onFeatures() {
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
        async onDataSet() {
            this.updateNameForArray('Типы объектов');
            let object = {
                properties: {
                    name: '',
                    type: '',
                    headers: [],
                    properties: [],
                }
            }
            let headers = [
                {
                    "text": "name",
                    "align": "start",
                    "value": "name",
                    "sortable": false
                },
                {
                    "text": "type",
                    "value": "type"
                }
            ];
            this.updateHeaders(headers);
            this.updateAction({
                actionGet: 'getTypeObject',
                actionPost: 'postTypeObject',
                actionOneGet: 'getOneTypeObject',
                actionPut: 'putTypeObject',
                actionDelete: 'deleteTypeObject',
            });
            if (this.allType != []) {
                await this.getTypeObject();
            }
            this.updateListItem({ items: this.allType });
            this.updateListType([]);
            this.upadateEmptyObject(object);
        },
        onUsers() {
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
                permissions: [],
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
        }
    },
    mounted() {
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