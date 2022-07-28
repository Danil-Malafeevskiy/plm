<template>
    <div class="text-center">
        <v-dialog v-model="dialog" width="500">
            <v-card class="gays">
                <div class="text-h6" style="text-align: center; padding-top: 2em;">
                    Здраствуйте, Василий!
                </div>

                <v-card-text>
                    <v-form @submit.prevent="onSubmit">
                        <v-row>
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-text-field v-model="userData.username" hide-details placeholder="vasyly@mail.com"
                                    filled>
                                </v-text-field>
                            </v-col>

                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-text-field v-model="userData.password" hide-details placeholder="Пароль" filled>
                                </v-text-field>
                            </v-col>

                        </v-row>
                        <div class="pa-0 btn">
                            <v-btn color="#EE5E5E" type="submit" style="width: 100%; color: white !important;"
                                @click="dialog = false">
                                ВОЙТИ
                            </v-btn>
                        </div>

                    </v-form>


                </v-card-text>


            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
export default {
    name: "AuthModal",
    data() {
        return {
            dialog: true,
            userData: {
                username: null,
                password: null 
            },
        }
    },
    watch: {
        allFeatures: function () {
            this.features = this.allFeatures;
        },
    },
    methods:{
        ...mapActions(['postAuth', 'allFeatures']),
        async onSubmit(){
            await this.postAuth(this.userData);
        },
    }
}
</script>

<style scoped>
.gays, 
.v-card,
.v-sheet{
    min-height: 38.9% !important;
    max-width: 51.85% !important;  
    background-color: #DDDDDD; 
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
}
.v-btn{
    min-height: 12.23% !important;
    max-height: 15% !important;
}
.btn{
    padding-left: 3% !important;
    padding-right: 3% !important;
}
</style>