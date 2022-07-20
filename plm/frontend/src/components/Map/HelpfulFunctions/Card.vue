<template>
    <v-card v-if="cardVisable_.data" width="38.05%">
        <div class="card__window" v-if="addCardOn_.data">
            <p style="display: none;">{{ feature }}</p>
            <v-file-input class="pa-0 ma-0" height="37.53%" color="#EE5E5E" :prepend-icon="icon.mdiImagePlusOutline"
                hide-input></v-file-input>
            <div style="overflow-y: scroll; overflow-x: hidden;">
                <v-card-text class="pa-0">
                    <v-form>
                        <v-row justify="start">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text style="font-size: 24px; padding: 16px 0;">Создание объекта</v-card-text>
                            </v-col>
                            <v-col v-for="(f, index) in feature.properties" :key="f.number_support" cols="2" sm="6"
                                md="5" lg="6">
                                <v-text-field v-model="feature.properties[index]"
                                    :value="feature.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
            </div>

            <div class="card__footer">
                <v-btn color="white" depressed @click="notVisableCard(); addCardOn_.data = !addCardOn_.data">ОТМЕНА</v-btn>
                <v-btn color="white" depressed @click="addNewFeature()">Создать</v-btn>
            </div>

        </div>
        <div class="card__window" v-else-if="infoCardOn_.data">
            <v-file-input disabled class="pa-0 ma-0" height="37.53%" color="#EE5E5E"
                :prepend-icon="icon.mdiImagePlusOutline" hide-input></v-file-input>
            <div style="overflow-y: scroll; overflow-x: hidden;">
                <v-card-text class="pa-0">
                    <v-form @submit.prevent="onSubmit">
                        <v-row justify="start">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text class="pa-0" style="font-size: 24px;">{{ feature.properties.name_tap }}
                                </v-card-text>
                            </v-col>
                            <v-col class="pa-0" cols="2" sm="6" md="5" lg="6">
                                <v-card-text class="pa-0"
                                    style="font-size: 24px; display: flex; justify-content: flex-end;">
                                    <v-btn
                                        @click="editCardOn_.data = !editCardOn_.data; infoCardOn_.data = !infoCardOn_.data;"
                                        class="ma-0" fab small elevation="0" color="white">
                                        <v-icon>
                                            {{ icon.mdiPencil }}
                                        </v-icon>
                                    </v-btn>
                                    <v-btn
                                        @click="deleteFeature(feature.id); infoCardOn_.data = !infoCardOn_.data; notVisableCard()"
                                        class="ma-0" fab small elevation="0" color="white">
                                        <v-icon>
                                            {{ icon.mdiDeleteOutline }}
                                        </v-icon>
                                    </v-btn>
                                </v-card-text>
                            </v-col>
                            <v-col v-for="(f, index) in feature.properties" :key="f.number_support"
                                v-show="index != 'name_tap' && index != 'id'" cols="2" sm="6" md="5" lg="6">
                                <v-text-field readonly v-model="feature.properties[index]"
                                    :value="feature.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
            </div>
        </div>

        <div class="card__window" v-else-if="editCardOn.data">
            <v-file-input class="pa-0 ma-0" height="37.53%" color="#EE5E5E" :prepend-icon="icon.mdiImagePlusOutline"
                hide-input></v-file-input>
            <div style="overflow-y: scroll; overflow-x: hidden;">
                <v-card-text class="pa-0">
                    <v-form @submit.prevent="onSubmit">
                        <v-row justify="start">
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-card-text style="font-size: 24px; padding: 16px 0;">Редактирование</v-card-text>
                            </v-col>
                            <v-col v-for="(f, index) in feature.properties" :key="f.number_support"
                                v-show="index != 'id'" cols="2" sm="6" md="5" lg="6">
                                <v-text-field v-model="feature.properties[index]"
                                    :value="feature.properties[index]" hide-details :label="index"
                                    :placeholder="index" filled>
                                </v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-card-text>
            </div>

            <div class="card__footer">
                <v-btn color="white" depressed @click="notVisableCard(); addCardOn_.data = !addCardOn_.data">ОТМЕНА</v-btn>
                <v-btn color="white" depressed @click="editFeature()">Редактирование</v-btn>
            </div>
        </div>
    </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'CardInfo',
    props: ['cardVisable', 'addCardOn', 'infoCardOn', 
    'editCardOn', 'icon', 'getFeature', 'visableCard', 'notVisableCard', 'addNewFeature', 'editFeature'],
    data () {
        return{
            cardVisable_: this.cardVisable,
            addCardOn_: this.addCardOn,
            infoCardOn_: this.infoCardOn,
            editCardOn_: this.editCardOn,
            feature: this.getFeature,
        }
    },
    watch: {
    cardVisable: function () {
      this.cardVisable_ = this.cardVisable;
    },
    getFeature: function(){
        this.feature = this.getFeature;
    }
  },
  methods: mapActions(['deleteFeature']),

}
</script>