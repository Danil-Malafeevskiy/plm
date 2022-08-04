<template>
    <v-navigation-drawer app color="#DDDDDD" permanent
        style="max-width: 18.96% !important; min-width: 18.96% !important;">
        <v-list-item>
            <v-list-item-content>
                <v-list-item-title>
                    <v-btn @click="showCard = !showCard" class="ma-0 pa-0 btn_menu" elevation="0" fab>
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
                Типы {{ allType.length }}<v-autocomplete :items="allType" dense append-icon hide-details hint="Поиск"
                    clearable solo label="Поиск">
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
        getList: {
            handler() {
                this.selectedItem = null;
            }
        }
    },
    computed: { ...mapGetters(['allFeatures', 'getList', 'allType', 'emptyObject']) },
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