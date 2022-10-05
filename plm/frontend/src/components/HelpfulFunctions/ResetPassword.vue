<template>
    <div class="text-center" >
        <v-dialog v-model="dialog" width="500" overlay-color="white" overlay-opacity="0.8" persistent
            no-click-animation style="filter: blur(1px) !important; backdrop-filter: blur(4px) !important;">
            <v-card class="title">
                <div class="text-h6" style="text-align: center; padding: 44px 0;">
                    Создайте новый пароль
                </div>
                <v-card-text>
                    <v-form @submit.prevent="onSubmit" style="padding: 0 50px">
                        <v-text-field background-color="#F1F1F1"
                            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" v-model="resetPassword"
                            placeholder="Пароль"
                            :type="showPassword ? 'text' : 'password'" filled
                            @click:append="showPassword = !showPassword">
                        </v-text-field>
                        
                        <div class="btn">
                            <v-btn class="pa-0 ma-0" color="#EE5E5E" type="submit" style="width: 100%; height: 45px; color: white !important;">
                                Изменить
                            </v-btn>
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
            resetPassword: null, 
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
            console.log('reseted')
            window.location.href = '/'
        },

        // async onSendEmail() {
        //     console.log('sended')
        // }
    },
    mounted() {
        // setTimeout(() =>{
        //     console.log(this.getAuth);
        // }, 1000)
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


