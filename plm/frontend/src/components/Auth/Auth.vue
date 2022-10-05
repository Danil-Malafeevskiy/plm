<template>
    <div class="text-center" id='auth'>
        <v-dialog v-model="dialog" width="500" overlay-color="white" overlay-opacity="0.8" persistent
            no-click-animation style="filter: blur(1px) !important; backdrop-filter: blur(4px) !important;">

            <v-card class="title" v-if="!resetBool">
                <div class="text-h6" style="text-align: center; padding: 44px 0;">
                    Здраствуйте!
                </div>
                <v-card-text>
                    <v-form @submit.prevent="onSubmit" style="padding: 0 50px">
                        <v-row>
                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-text-field background-color="#F1F1F1" v-model="userData.username"
                                    placeholder="vasyly@mail.com" filled>
                                </v-text-field>
                            </v-col>

                            <v-col cols="2" sm="6" md="5" lg="6">
                                <v-text-field background-color="#F1F1F1"
                                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" v-model="userData.password"
                                    placeholder="Пароль"
                                    :type="showPassword ? 'text' : 'password'" filled
                                    @click:append="showPassword = !showPassword">
                                </v-text-field>
                            </v-col>

                        </v-row>
                        <div class="btn">
                            <v-btn class="pa-0 ma-0" color="#EE5E5E" type="submit" style="width: 100%; height: 45px; color: white !important;">
                                ВОЙТИ
                            </v-btn>
                        </div>
                        <div class="reset-password">
                            <v-btn @click="onResetPassword">Забыли пароль?</v-btn>
                        </div>
                    </v-form>
                </v-card-text>
            </v-card>

            <v-card class="title" v-else-if="resetBool">
                <div class="text-h6" style="text-align: center; padding: 44px 0;">
                    Впишите адресс электронной почты
                </div>
                <v-card-text>
                    <v-form @submit.prevent="onSendEmail" style="padding: 0 50px">
                        <v-text-field background-color="#F1F1F1" v-model="emailForResetPassword"
                            placeholder="vasyly@mail.com" filled>
                        </v-text-field>
                        
                        <div class="btn">
                            <v-btn class="pa-0 ma-0" color="#EE5E5E" type="submit" style="width: 100%; height: 45px; color: white !important;">
                                Восстановить пароль
                            </v-btn>
                        </div>
                        <div class="reset-password">
                            <v-btn @click="onResetPassword">Назад</v-btn>
                        </div>
                    </v-form>
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
            emailForResetPassword: null, 
            resetBool: false,
        }
    },
    watch: {
        getAuth: function (){
            this.bool = this.authBool;
        }
    },
    computed: mapGetters(['getAuth']),
    methods: {
        ...mapActions(['logIn']),

        async onSubmit() {
            await this.logIn(this.userData)
            if (this.getAuth){
                location.reload();
            } else{
                this.userData.username = '';
                this.userData.password = '';
            }
        },

        async onResetPassword(){
            this.resetBool = !this.resetBool
        },

        async onSendEmail() {
            console.log('sended')
            this.resetBool = false
        }
    },

}
</script>

<style scoped>
.title,
.v-card,
.v-sheet {
    min-height: 37% !important;
    max-width: 47.85% !important;
    background-color: #DDDDDD;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    box-shadow: none !important;
    border-radius: 12px !important;
}

.v-btn {
    min-height: 12.23% !important;
    max-height: 15% !important;
}

.text_centre{
    border-radius: 12px;
}

.btn {
    padding-top: 12px
}

</style>


