import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async postAuth({ commit }, userData) {
            await axios.post('/tower/login', userData).then((response) => {
                console.log(response.data);
                commit('updateAuth', response.data === 'Success login');
            });
        },
        async logOut({ commit }) {
            await axios.get('/tower/logout').then((response) => {
                console.log(response.data);
                commit('updateAuth', !response.data === 'Success logout')
            })
        },
        async getUser({ commit }){
            await axios.get('/user').then((response) => {
                console.log(response.data);
                commit('updateAuth', true);
                commit('updateUser', response.data);
            }).catch((error) => {
                console.log(error);
                commit('updateAuth', false);
            })
        }
    },

    mutations: {
        updateAuth(state, bool) {
            state.authBool = bool;
        },
        updateUser(state, user){
            state.user = user;
        }
    },
    getters: {
        getAuth(state) {
            return state.authBool;
        },
        user(state){
            return state.user;
        }
    },
    state: {
        authBool: null,
        user: null,
    },
}