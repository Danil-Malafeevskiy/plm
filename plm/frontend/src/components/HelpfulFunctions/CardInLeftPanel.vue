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
    data() {
        return {
            selectedItem: 2,
        }
    },
    watch: {
        selectedItem: {
            async handler() {
                this.filterForFeature(null);
                if (this.selectedItem != null) {
                    if ((this.selectedItem != 3 && this.user.is_staff) || (this.selectedItem != 0 && this.user.is_active)) {
                        setTimeout(() => {
                            document.querySelector('.text_in_span').innerHTML = document.querySelector('.v-item--active .v-list-item__title').innerText;
                        })
                    }
                    switch (this.selectedItem) {
                        case 0: {
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
                            this.updateHeaders(headers);
                            this.updateAction({
                                actionGet: 'getAllGroups',
                                actionPost: 'postGroup',
                                actionOneGet: 'getGroup',
                                actionPut: 'putGroup',
                                actionDelete: 'deleteGroup',
                            });
                            this.getAllGroups();
                            break;
                        }
                        case 1: {
                            let object = {
                                properties: {
                                    name: '',
                                    type: '',
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
                            break;
                        }
                        case 2:
                            this.getTypeObject();
                            this.updateAction({
                                actionGet: 'getFeatures',
                                actionOneGet: 'getOneFeature',
                                actionPost: 'postFeature',
                                actionPut: 'putFeature',
                                actionDelete: 'deleteFeature',
                            });
                            break;
                    }
                }
            }
        }
    },
    computed: mapGetters(['allFeatures', 'user', 'allGroups', 'getList', 'allType']),
    methods: {
        ...mapActions(['logOut', 'getAllGroups', 'getTypeObject']),
        ...mapMutations(['filterForFeature', 'updateList', 'updateListItem', 'upadateEmptyObject',
            'updateAction', 'updateHeaders', 'updateListType']),
        logOutAndResolve() {
            this.logOut();
            location.reload();
        },
    },
    mounted() {
    }
}
</script>

<style>
.card_test {
    left: 16px !important;
    right: 16px !important;
    top: 50px !important;
    position: fixed;
    z-index: 1 !important;
    border-radius: 12px !important;
}
</style>