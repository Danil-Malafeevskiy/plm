import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async sendEmail({ commit }, emailData) {
            await axios.post('/password-reset-request', emailData).then((response) => {
                console.log(response.data)
                commit('updateEmail', response.data);
            });
        },

        async checkoutPasswordReset({ commit }, path) {
            await axios.get(`/${path}/get`).then((response) => {
                commit('updateUserToken', response.data)
            })
        },

        async changePassword({ commit }, data) {
            await axios.put('/password-setnew', data).then((response) => {
                commit('updateValidateErrors', response.data);
            })
        },

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
                if (typeof response.data === 'object' && !('id' in response.data)) {
                    for (let i in response.data) {
                        commit('updateError', response.data[i]);
                    }
                }
                else {
                    dispatch('getUsersOfGroup');
                    dispatch('allGroupForNav');
                }
            })
        },
        async putUser({ dispatch, state, getters, commit }, user) {
            user = { ...user, ...user.properties };
            delete user.properties;
            user.username = user.email;
            console.log(user);
            await axios.put('/user/admin', user).then((response) => {
                if (typeof response.data === 'object') {
                    for (let i in response.data) {
                        commit('updateError', response.data[i]);
                    }
                }
                else if (getters.allListItem[0] !== state.user) {
                    dispatch('getUsersOfGroup');
                    dispatch('allGroupForNav');
                    if (user.id === state.user.id) {
                        dispatch('getUser');
                    }
                }
                else if (getters.allListItem[0] === state.user && 'password' in user && !getters.error) {
                    dispatch('logOut');
                }
            })
        },
        async deleteUser({ dispatch }, idUser) {
            await axios.delete(`/user/admin?id=${idUser}`).then(() => {
                dispatch('getUsersOfGroup');
                dispatch('allGroupForNav');
            })
        },

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
        },
        updateEmail(state, email) {
            state.email = email
        },
        updateUserToken(state, token) {
            state.userResetPasswordData = token
        },
        updateValidateErrors(state, erorrs) {
            state.validateErrors = erorrs
        }
    },
    getters: {
        getAuth(state) {
            return state.authBool;
        },
        user(state) {
            return state.user;
        },
        userResetPasswordData(state) {
            return state.userResetPasswordData
        },

        validateErrors(state) {
            return state.validateErrors
        },

        validateEmailErrors(state) {
            return state.email
        }
    },
    state: {
        authBool: null,
        user: null,
        allUsers: [],
        email: null,
        userResetPasswordData: null,
        validateErrors: null,
    },
}