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
                let user = response.data;
                user.properties = { ...user };
                delete user.properties.id;
                delete user.properties.image;
                for (let key in user) {
                    if (key != 'properties' && key != 'id' && key != 'image') {
                        if (typeof user[key] === 'object') {
                            delete user.properties[key];
                        }
                        else {
                            delete user[key];
                        }
                    }
                }
                commit('updateObjectForCard', user);
            })
        },

        async postUser({ dispatch, commit }, newUser) {
            console.log(newUser);
            await axios.post('/user/admin', newUser).then((response) => {
                if (typeof response.data === 'object') {
                    for (let i in response.data) {
                        commit('updateError', response.data[i]);
                    }
                }
                else {
                    dispatch('getUsersOfGroup');
                }
            })
        },
        async putUser({ dispatch, state, getters, commit }, user) {
            user = { ...user, ...user.properties };
            delete user.properties;
            user.username = user.email;
            console.log(user);
            await axios.put('/user/admin', user).then((response) => {
                if (getters.allListItem[0] !== state.user) {
                    dispatch('getUsersOfGroup');
                    if (user.id === state.user.id) {
                        dispatch('getUser');
                    }
                }
                else if (getters.allListItem[0] === state.user) {
                    if (typeof response.data === 'object') {
                        for (let i in response.data) {
                            commit('updateError', response.data[i]);
                        }
                    }
                    else if ('password' in user) {
                        dispatch('logOut');
                    }
                }
                console.log(response.data)
            })
        },
        async deleteUser({ dispatch }, idUser) {
            await axios.delete(`/user/admin?id=${idUser}`).then(() => {
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