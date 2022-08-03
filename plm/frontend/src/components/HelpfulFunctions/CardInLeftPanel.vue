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
                let list = [];
                if (this.selectedItem != null) {
                    if ((this.selectedItem != 3 && this.user.is_staff) || (this.selectedItem != 0 && this.user.is_active)) {
                        setTimeout(() => {
                            document.querySelector('.text_in_span').innerHTML = document.querySelector('.v-item--active .v-list-item__title').innerText;
                        })
                    }
                    if (this.selectedItem === 0) {
                        await this.getAllGroups();
                        for (let key in this.allGroups) {
                            list.push(this.allGroups[key].name);
                        }
                        let headers = [
                            {
                                text: 'id',
                                align: 'start',
                                sortable: false,
                                value: 'id',
                            },
                            { text: 'name', value: 'name' },
                        ]
                        this.updateListItem({ headers, items: this.allGroups, nameAction: 'getGroup' });
                    }
                    else if (this.selectedItem === 2) {
                        for (let key in this.allFeatures) {
                            list.push(this.allFeatures[key].name);
                        }
                        list = [...new Set(list)];
                    }
                    this.updateList(list);
                }
            }
        }
    },
    computed: mapGetters(['allFeatures', 'user', 'allGroups', 'getList']),
    methods: {
        ...mapActions(['logOut', 'getAllGroups']),
        ...mapMutations(['filterForFeature', 'updateList', 'updateListItem']),
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