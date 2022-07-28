<template>
    <div class="text-center" v-if="auth === 'GUEST'">
        <v-dialog v-model="dialog" width="500" overlay-color="white" overlay-opacity="0.8" persistent
            no-click-animation>
            <v-card class="title">
                <div class="text-h6" style="text-align: center; padding-top: 2em;">
                    Здраствуйте
                </div>


                <v-card-text>
                    <validation-observer ref="observer">
                        <v-form @submit.prevent="onSubmit">
                            <v-row>
                                <v-col cols="2" sm="6" md="5" lg="6">
                                    <v-text-field background-color="#F1F1F1" v-model="userData.username" hide-details
                                        placeholder="vasyly@mail.com" filled>
                                    </v-text-field>
                                </v-col>

                                <v-col cols="2" sm="6" md="5" lg="6">
                                    <v-text-field background-color="#F1F1F1"
                                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                        v-model="userData.password" :rules="[rules.min]" hint="Минимум 8 символов"
                                        placeholder="Пароль" :type="showPassword ? 'text' : 'password'" filled
                                        @click:append="showPassword = !showPassword">
                                    </v-text-field>
                                </v-col>

                            </v-row>
                            <div class="pa-0 btn">
                                <v-btn color="#EE5E5E" type="submit" :disabled="invalid"
                                    style="width: 100%; color: white !important;" @click="dialog = false">
                                    ВОЙТИ
                                </v-btn>
                            </div>

                        </v-form>

                    </validation-observer>
                </v-card-text>


            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "AuthModal",
    data() {
        return {
            dialog: true,
            showPassword: false,
            userData: {
                username: null,
                password: null
            },
            auth: null,
            rules: {
                min: v => v.length >= 8 || 'Минимум 8 символов',
            },
        }
    },
    watch: {
        allFeatures: function () {
            this.features = this.allFeatures;
        },
    },
    computed: mapGetters(['resultLogIn']),
    methods: {
        ...mapActions(['postAuth', 'allFeatures']),

        async onSubmit() {
            await this.postAuth(this.userData);
            if(this.resultLogIn){
                location.reload();
            }
            else{
                console.log('ошибка');
            }

        },
    },
    mounted() {
        this.auth = document.getElementById('auth').innerText;
    }

}
</script>

<style scoped>
.title,
.v-card,
.v-sheet {
    min-height: 38.9% !important;
    max-width: 51.85% !important;
    background-color: #DDDDDD;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    box-shadow: none !important;
}

.v-btn {
    min-height: 12.23% !important;
    max-height: 15% !important;
}

.btn {
    padding-left: 3% !important;
    padding-right: 3% !important;
}

.v-overlay.v-overlay--active {
    filter: blur(1px) !important;
    backdrop-filter: blur(4px) !important;
}
</style>