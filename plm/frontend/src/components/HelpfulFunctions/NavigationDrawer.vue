<template>
    <v-navigation-drawer v-if="list.length != 0" app color="#DDDDDD" permanent
        style="max-width: 18.96% !important; min-width: 18.96% !important;">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title>
                    <v-icon left>mdi-menu</v-icon>
                    База объектов
                </v-list-item-title>
            </v-list-item-content>
        </v-list-item>


        <v-list dense nav>
            <p
                style="display: flex; font-size: 16px; color: #5E5E5E; justify-content: space-between; align-items: center;">
                Типы {{ list.length }}<v-autocomplete :items="list" dense append-icon hide-details hint="Поиск"
                    clearable solo label="Поиск">
                </v-autocomplete>
            </p>
            <v-list-item-group v-model="selectedItem" color="#E93030">
                <v-list-item v-for="key in list" :key="key" link>

                    <v-list-item-title>
                        <v-list-item-icon v-if="key === 'Tower_1'">
                            <v-icon>mdi-transmission-tower</v-icon>
                        </v-list-item-icon>
                        <v-list-item-icon v-else-if="key === 'Substations'">
                            <v-icon>mdi-toy-brick</v-icon>
                        </v-list-item-icon>
                        <v-list-item-icon v-else>
                            <v-icon>mdi-vector-line</v-icon>
                        </v-list-item-icon>
                        {{ key }}
                    </v-list-item-title>

                </v-list-item>
            </v-list-item-group>
        </v-list>

    </v-navigation-drawer>
    <v-navigation-drawer v-else app color="#DDDDDD" permanent
        style="max-width: 2.86% !important; min-width: 2.86% !important;">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title>
                    <v-icon left>mdi-menu</v-icon>
                    База объектов
                </v-list-item-title>
            </v-list-item-content>
        </v-list-item>
    </v-navigation-drawer>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';

export default {
    name: 'CardInfo',
    data() {
        return {
            selectedItem: null,
            list: [],
        }
    },
    watch: {
        allFeatures: {
            handler() {
                this.list = [];
                for (let key in this.allFeatures) {
                    this.list.push(this.allFeatures[key].name);
                }
                this.list = [... new Set(this.list)];
            }
        },
        selectedItem: {
            handler() {
                const domItem = document.querySelector('.v-item-group').childNodes[this.selectedItem];
                this.filterForFeature(domItem.childNodes[0].innerText);
            }
        },
    },
    computed: { ...mapGetters(['allFeatures']) },
    methods: {
        ...mapMutations(['filterForFeature']),
    },
}
</script>

<style>
</style>