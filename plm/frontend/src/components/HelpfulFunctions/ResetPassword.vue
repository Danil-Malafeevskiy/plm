<template><div class="text-center">
    <v-dialog v-model="dialog" width="500" overlay-color="white" overlay-opacity="0.8" persistent no-click-animation
        style="filter: blur(1px) !important; backdrop-filter: blur(4px) !important;">
        <v-card class="title" v-if="userResetPasswordData.success">
            <div class="text-h6" style="text-align: center; padding: 44px 0;">
                Создайте новый пароль
            </div>
            <v-card-text>
                <v-form @submit.prevent="onSubmit" style="padding: 0 50px">
                    <v-text-field background-color="#F1F1F1" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        v-model="resetPassword" placeholder="Пароль" :rules="[rules.required, rules.min]"
                        :type="showPassword ? 'text' : 'password'" filled @click:append="showPassword = !showPassword">
                    </v-text-field>

                    <v-text-field background-color="#F1F1F1" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        v-model="resetPassword_" placeholder="Пароль" :rules="[rules.required, rules.min]"
                        :type="showPassword ? 'text' : 'password'" filled @click:append="showPassword = !showPassword">
                    </v-text-field>

                    <div class="btn">
                        <v-btn :disabled="disabledBool" class="pa-0 ma-0" color="#EE5E5E" type="submit"
                            style="width: 100%; height: 45px; color: white !important;">
                            Изменить
                        </v-btn>
                    </div>
                </v-form>
            </v-card-text>
        </v-card>

        <v-card class="title" v-else>
            <div class="text-h6" style="text-align: center; padding: 44px 0;">
                Эта функция недоступна
            </div>
            <div class="reset-password">
                <v-btn block text @click="toMainPath">Назад</v-btn>
            </div>
        </v-card>

        <div v-for="(el, index) in validateErrors" :key="el" id="alert" style="position:absolute;">
            <v-alert  type="error" v-if="index === 'non_field_errors'">
                <div v-for="item in el" :key="item">
                    <p>{{item}}</p>
                </div>
            </v-alert>
            <v-alert  type="success" v-else>
                <p>Успешно</p>
            </v-alert>
        </div>
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
            resetPassword: null, 
            resetPassword_: null,
            userResetPasswordData_: null,
            disabledBool: true,
            rules: {
                required: value => !!value || (this.disabledBool = true) && 'Обязательное поле',
                min: v => v.length >= 8 || (this.disabledBool = true) && 'Минимум 8 символов',
            },
        }
    },
    watch: {
        getAuth: function (){
            this.bool = this.authBool;
        },
        userResetPasswordData: {
            handler(){
                this.userResetPasswordData_ = this.userResetPasswordData
            }
        },

        resetPassword: {
            handler(){
                if(this.resetPassword === this.resetPassword_){
                    this.disabledBool = false
                } else {
                    this.disabledBool = true
                }
            }
        },
        resetPassword_: {
            handler(){
                if(this.resetPassword === this.resetPassword_){
                    this.disabledBool = false
                } else {
                    this.disabledBool = true
                }
            }
        }
    },
    computed: mapGetters(['userResetPasswordData', 'validateErrors']),
    methods: {
        ...mapActions(['checkoutPasswordReset', 'changePassword']),

        async onSubmit() {
            let userPasswordData = {
                password: this.resetPassword,
                token: this.userResetPasswordData_.token,
                uidb64: this.userResetPasswordData_.uidb64
            }
            await this.changePassword(userPasswordData)
            if(this.validateErrors.non_field_errors){
                console.log(this.validateErrors)
            } else {
                document.getElementById('alert').style.display = 'none'
                window.location.href = '/'
            }
        },

        toMainPath(){
            window.location.href = '/'
        }

    },
    mounted() {
        let path = window.location.pathname.slice(1)
        this.checkoutPasswordReset(path)
    }

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


