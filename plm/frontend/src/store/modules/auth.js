import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async logIn({ commit }, userData) {
            await axios.post('/tower/login', userData).then((response) => {
                commit('updateAuth', response.data === 'Success login');
            });
        },
        async logOut({ commit }) {
            await axios.get('/tower/logout').then((response) => {
                commit('updateAuth', !response.data === 'Success logout')
            })
        },
        async getUser({ commit }) {
            await axios.get('/user').then((response) => {
                commit('updateAuth', true);
                commit('updateUser', response.data);
            }).catch((error) => {
                console.log(error);
                commit('updateAuth', false);
            })
        },
        async getOneUser({ commit }, idUser) {
            await axios.get(`/user/admin/${idUser}`).then((response) => {
                //console.log(response.data);
                let user = response.data;
                user.properties = { ...user };
                delete user.properties.id;
                for (let key in user) {
                    if (key != 'properties' && key != 'id') {
                        if (typeof user[key] === 'object') {
                            delete user.properties[key];
                        }
                        else {
                            delete user[key];
                        }
                    }
                }
                console.log(user);
                commit('updateObjectForCard', user);
            })
        },
        async postUser({ dispatch, getters }, newUser) {
            await axios.post('/user/admin', newUser).then((response) => {
                newUser.id = response.data.id;
                newUser.groups = [getters.currentGroup.name];
                newUser.user_permissions = [];
                delete newUser.password
                dispatch('putUser', newUser);
            })
        },
        async putUser({ dispatch, state }, user) {
            user = { ...user, ...user.properties};
            delete user.properties;
            console.log(user);
            await axios.put('/user/admin', user).then((response) => {
                console.log(response.data);
                dispatch('getUsersOfGroup');
                if (user.id === state.user.id){
                    dispatch('getUser');
                }
            })
        },
        async deleteUser({ dispatch }, idUser) {
            await axios.delete(`/user/admin/${idUser}`).then((response) => {
                console.log(response.data);
                dispatch('getUsersOfGroup');
            })
        }
    },

    mutations: {
        updateAuth(state, bool) {
            state.authBool = bool;
        },
        updateUser(state, user) {
            state.user = user;
        },
        updateAllUsers(state, users) {
            state.allUsers = users;
        }
    },
    getters: {
        getAuth(state) {
            return state.authBool;
        },
        user(state) {
            return state.user;
        }
    },
    state: {
        authBool: null,
        user: null,
        allUsers: [],
    },
}