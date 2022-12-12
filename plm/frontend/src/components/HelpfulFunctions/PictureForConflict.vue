<template>
    <div style="max-height: 22.48% !important;
    min-height: 22.48% !important; z-index: 5">
        <div v-if="objectForConflict_ && objectForCard && objectForConflict_.image !== notConflictObject.image && notConflictObject.id === objectForConflict_.id"
            class="conflict_pictures">
            <v-img v-if="objectForConflict_.image" :src="objectForConflict_.image" class="two_pictures">
            </v-img>
            <v-file-input v-else class="pa-0 ma-0 two_background_color_red" :prepend-icon="icon" disabled hide-input>
            </v-file-input>
            <v-btn small icon @click="changeImage" style="
                                        max-height: 100% !important;
                                        margin: auto 0 !important;
                                    ">
                <v-icon v-if="notConflictObject.image === objectForCard.image">
                    mdi-arrow-right</v-icon>
                <v-icon v-else>mdi-arrow-left</v-icon>
            </v-btn>
            <v-img v-if="notConflictObject.image" :src="notConflictObject.image" class="two_pictures">
            </v-img>
            <v-file-input v-else class="pa-0 ma-0 two_background_color_red" :prepend-icon="icon" disabled hide-input>
            </v-file-input>
        </div>

        <template v-else-if="notConflictObject">
            <v-img v-if="notConflictObject.image" :src="notConflictObject.image" class="one_picture">
            </v-img>

            <v-file-input v-else class="pa-0 ma-0 background_color_red" :prepend-icon="icon" disabled hide-input>
            </v-file-input>
        </template>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { mdiImagePlusOutline } from '@mdi/js';

export default {
    name: 'PictureForConflict',
    porps: ['objectForCard_', 'objectForConflict', 'conflictCard'],
    data() {
        return {
            objectForCard: this.objectForCard_,
            objectForConflict_: this.objectForConflict,
            notConflictObject: {},
            icon: mdiImagePlusOutline,
        }
    },
    watch: {
        getObjectForCard: {
            handler() {
                this.getOjects();
            }
        },
        newData: {
            handler(){
                this.getOjects();
            }
        }
    },
    computed: {
        ...mapGetters(['getObjectForCard', 'newData']),
    },
    methods: {
        changeImage() {
            this.objectForCard.image = this.notConflictObject.image === this.objectForCard.image ? this.objectForConflict_.image : this.notConflictObject.image;
        },
        getOjects() {
            if (this.newData.length) {
                this.objectForCard = this.getObjectForCard;
                this.notConflictObject = JSON.parse(JSON.stringify(this.objectForCard));
                this.objectForConflict_ = this.newData.find(el => this.objectForCard.id === el.id);
            }
        }
    },
    mounted() {
    }
}
</script>

<style scoped>
.card__img {
    align-items: flex-start;
}

.v-icon--link::after {
    background-color: rgba(255, 255, 255, 0) !important;
}

.background_color_red {
    background-color: #EE5E5E !important;
    max-height: 100% !important;
    min-height: 100% !important;
    border-radius: 12px 12px 0 0;
}

.background_color_gray {
    background-color: #DDDDDD !important;
}

.btn_del_img {
    position: absolute;
    z-index: 2;
    right: 0;
}

.one_picture {
    position: relative !important;
    max-height: 100% !important;
    min-height: 100% !important;
    border-radius: 12px 12px 0 0 !important;
}

.conflict_pictures {
    display: flex;
    justify-content: space-between;
    background-color: #C9C8ED;
    padding: 34px 50px;
    border-radius: 12px 12px 0 0;
    max-height: 100%;
}

.two_pictures {
    max-width: 42% !important;
    border-radius: 4px;
}

.two_background_color_red {
    background-color: #EE5E5E !important;
    max-width: 42% !important;
    border-radius: 4px;
}
</style>