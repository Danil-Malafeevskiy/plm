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

        <CardInLeftPanel v-show="showCard" />

        <v-list dense nav>
            <p
                style="display: flex; font-size: 16px; color: #5E5E5E; justify-content: space-between; align-items: center;">

                Типы {{ getList.length }}

                <v-autocomplete
                    @click:clear="clear()" 
                    id='search'
                    dense 
                    append-icon 
                    hide-details 
                    hint="Поиск" 
                    hide-no-data
                    clearable
                    solo 
                    :value="value"
                    label="Поиск"
                    @update:search-input="search()"
                >
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
import $ from 'jquery'

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
                    const domItem = document.querySelector(".object__data").childNodes[this.selectedItem];
                    this.filterForFeature(domItem.childNodes[0].innerText);
                }
                // else {
                //     this.filterForFeature(null);
                // }
            }
        },

        getList: {
            handler() {
                this.selectedItem = null;
            }
=
        },
        // allType: {
        //     handler(){
        //         console.log(this.allType);
        //     }
        // }
    },
    computed: { ...mapGetters(['allFeatures', 'getList', 'allType', 'emptyObject']) },
=
    methods: {
        ...mapActions(['getGroup', 'getTypeObject']),
        ...mapMutations(['filterForFeature', 'upadateEmptyObject', 'updateFeatureNameType', 'updateHeaders', 'updateDrawType']),
        getOneGroup(id) {
            this.getGroup(id);
        },

        changeObject(objectType) {
            this.updateHeaders(objectType.headers);
            this.updateDrawType(objectType.type)
            this.filterForFeature(objectType.name);
            
            for (let i in this.allFeatures) {
                if (this.allFeatures[i].name === objectType.name) {
                    this.upadateEmptyObject(this.allFeatures[i]);
                    break;
                }
            }
        }
    },



        // clear() {
        //     this.getList.forEach(element => {
        //         $(".test:contains(" + element + "):hidden").show()
        //     });
        // },

        search() {
            const value = document.getElementById('search').value;

            this.getList.forEach(element => {

                if (!element.toLowerCase().includes(value.toLowerCase())) {
                    $("div:contains(" + element + "):last").parent().hide()
                    $(".v-list-item:contains(" + element + "):last").hide()
                }

                else  {
                    $("div:contains(" + element + "):last").parent().show()
                    $(".v-list-item:contains(" + element + "):last").show()
                }
            });
        },



    },
    async mounted() {
        await this.getTypeObject();

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