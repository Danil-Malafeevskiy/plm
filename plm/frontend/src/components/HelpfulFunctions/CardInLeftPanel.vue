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
                <v-list-item>
                    <v-list-item-title>
                        {{ user.username }}
                    </v-list-item-title>
                    <v-btn elevation="0" class="ma-0 pa-0 btn_menu" icon fab depressed retain-focus-on-click plain >
                        <v-icon @click="logOutAndResolve()">mdi-logout-variant</v-icon>
                    </v-btn>
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
            selectedItem: null,
        }
    },
    watch: {
        selectedItem: {
            async handler() {
                this.filterForFeature(null);

                if (this.selectedItem != null) {
                    if (this.selectedItem != 3) {
                        setTimeout(() => {
                            document.querySelector('.text_in_span').innerHTML = document.querySelector('.v-item--active .v-list-item__title').innerText;
                        })
                    }
                    if (this.selectedItem === 0) {
                        await this.getAllGroups();
                        let list = [];
                        for (let key in this.allGroups) {
                            list.push(this.allGroups[key].name);
                        }
                        this.updateList(list);
                    }
                    else if (this.selectedItem === 2) {
                        let list = [];
                        for (let key in this.allFeatures) {
                            list.push(this.allFeatures[key].name);
                        }
                        list = [...new Set(list)];
                        this.updateList(list);
                    }
                }
            }
        }
    },
    computed: mapGetters(['allFeatures', 'user', 'allGroups', 'getList']),
    methods: {
        ...mapActions(['logOut', 'getAllGroups']),
        ...mapMutations(['filterForFeature', 'updateList']),
        logOutAndResolve() {
            this.logOut();
            location.reload();
        },
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