import axios from "axios";

export default {
    actions: {
        async getTypeObject({ commit }) {
            await axios.get('/dataset').then((response) => {
                //console.log(response.data);
                commit('updateListType', response.data);
            });
        },
        async getOneTypeObject({ commit }, id) {
            await axios.get(`/dataset/${id}`).then((response) => {
                console.log(response.data, 1);
                commit('updateOneType', response.data);
            });
        },
        async postTypeObject({ dispatch }, newType) {
            await axios.post('/dataset', newType, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject');
            })
        },
        async putTypeObject({ dispatch }, type) {
            await axios.put('/dataset', type, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject');
            });
        },
        async deleteTypeObject({ dispatch }, id) {
            await axios.delete(`/dataset/${id}`).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject');
            })
        }
    },
    mutations: {
        updateListType(state, list) {
            state.listType = list;
        },
        updateOneType(state, type){
            state.type = type;
        }
    },
    getters: {
        allType(state) {
            return state.listType;
        },
        oneType(state){
            return state.type
        }
    },
    state: {
        listType: [],
        type: null,
    },
}