import axios from "axios";

export default{
    actions:{
        async postAuth(context, userData) {
            await axios.post('/tower/login', userData, this.state).then((response) => {
                const authResponse = response.data;
                
                if(response.data === 'Success login'){
                    const bool = true
                    console.log(authResponse);
                    context.commit('updateAuth', bool);
                } else {
                    const bool = false;
                    console.log(authResponse);
                    context.commit('updateAuth', bool);
                }
                
            });
        },
    },

    mutations:{
        updateAuth(state, bool){
            state.authBool = bool;
        },

    },
    getters:{
        getAuth(state){
            return state.authBool;
        }

    },
    state:{        
        authBool: null,
        userData: {
            username: null,
            password: null
        },
    },
}