<template>
    <div style="min-height: 100%">
        <v-card
            v-if="'properties' in objectForCard && 'type' in objectForCard.properties && objectForCard.properties.type === 'Point'"
            class="one_picture pa-0 ma-0 background_color_gray" tile flat
            style="width: 100% !important; overflow-y: scroll !important;"
            :style="{ 'min-height': heightPicture, 'max-height': heightPicture }">

            <v-row no-gutters justify="start">
                <v-col v-for="(el, index) in listMdiIcons" :key="index" md="3" lg="4" style="max-width: 48px !important"
                    class="ma-0">
                    <v-radio-group hide-details class="pa-0 ma-0" v-model="objectForCard.image">
                        <v-radio :value="el" :readonly="infoCardOn_.data" class="ma-2" color="#E93030" :on-icon="el"
                            :off-icon="el" style="
                                    min-height: 2em !important; 
                                    min-width: 2em !important;
                                "></v-radio>
                    </v-radio-group>
                </v-col>
            </v-row>
        </v-card>
        <v-file-input v-else-if="'properties' in objectForCard && 'type' in objectForCard.properties" accept="image/*"
            class="pa-0 ma-0 background_color_red" :prepend-icon="icon" :disabled="infoCardOn_.data" hide-input
            :style="{ 'min-height': heightPicture, 'max-height': heightPicture }">
        </v-file-input>

        <v-file-input v-else-if="!objectForCard.image" @change="fileToBase64" accept="image/*" :class="{
            'background_color_red': !('properties' in objectForCard && 'first_name' in objectForCard.properties),
            'background_color_gray': ('properties' in objectForCard && 'first_name' in objectForCard.properties)
        }" class="pa-0 ma-0" :prepend-icon="icon" :disabled="infoCardOn_.data" hide-input style="z-index: 1"
            :style="{ 'min-height': heightPicture, 'max-height': heightPicture }">
        </v-file-input>
        <template v-else-if="objectForCard.image && !infoCardOn_.data">
            <div class="background_img"></div>
            <v-btn class="btn_del_img ma-3 pa-0" elevation="0" icon @click="objectForCard.image = ''">
                <v-icon color="white">
                    mdi-delete-outline
                </v-icon>
            </v-btn>
        </template>

        <template v-if="!('properties' in objectForCard && 'type' in objectForCard.properties)">
            <v-img v-if="objectForCard.image" :src="objectForCard.image" :class="{
                'one_picture': infoCardOn_.data,
                'not_one_picture': !infoCardOn_.data,
            }" width="100%" style="max-height: 37.53%"></v-img>
        </template>
    </div>
</template>

<script>
import { mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket } from '@mdi/js'


export default {
    name: 'PictureForCard',
    props: ['objectForCard_', 'infoCardOn_'],
    data() {
        return {
            objectForCard: this.objectForCard_,
            icon: mdiImagePlusOutline,
            listMdiIcons: [mdiImagePlusOutline, mdiTransmissionTower, mdiPineTree, mdiAirplane, mdiApple, mdiBiohazard, mdiBluetooth, mdiBottleWine, mdiBucket],
        }
    },
    watch: {
        objectForCard_() {
            this.objectForCard = this.objectForCard_;
        }
    },
    computed: {
        heightPicture() {
            if (this.conflictCard)
                return '24.48%'
            else
                return '37.5%'
        }
    },
    methods: {
        fileToBase64(file) {
            const reader = new FileReader();

            reader.onload = (e) => {
                this.objectForCard.image = e.target.result;
            };
            reader.readAsDataURL(file);
        },
    }
}
</script>

<style>
.v-file-input {
    min-height: 37.53%;
    max-height: 37.53%;
    border-radius: 12px 12px 0 0;
}

.background_color_red {
    background-color: #EE5E5E !important;
}

.background_color_gray {
    background-color: #DDDDDD !important;
}

.card__img {
    align-items: flex-start;
}

.v-icon--link .v-icon__svg {
    min-width: 133.33px !important;
    min-height: 133.33px !important;
    fill: #FFFFFF !important;
}

.one_picture {
    position: relative !important;
    border-radius: 12px 12px 0 0 !important;
}

.not_one_picture {
    position: absolute !important;
    top: 0;
    border-radius: 12px 12px 0 0 !important;
    z-index: 0;
}

.background_img {
    z-index: 1;
    position: absolute;
    left: 0;
    right: 0;
    background-color: #000;
    opacity: 0.3;
    min-height: 37.53%;
    max-height: 37.53%;
    border-radius: 12px 12px 0 0;
}

.v-input .v-input__prepend-outer {
    margin: auto !important;
}

.btn_del_img {
    position: absolute;
    z-index: 2;
    right: 0;
}
</style>