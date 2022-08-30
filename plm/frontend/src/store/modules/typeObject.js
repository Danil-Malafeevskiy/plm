import axios from "axios";

export default {
    actions: {
        async getTypeObject({ commit }, change = false) {
            await axios.get('/dataset').then((response) => {
                if (!change) {
                    commit('updateListType', response.data);
                }
                else {
                    commit('updateListItem', { items: response.data });
                }
            });
        },
        async getOneTypeObject({ commit }, id) {
            await axios.get(`/dataset/admin/${id}`).then((response) => {
                let result = { ...response.data };
                result.properties = { ...result };
                delete result.properties.id;
                delete result.properties.image;
                for (let i in result) {
                    if (i != 'properties' && i != 'id' && i != 'image') {
                        delete result[i];
                    }
                }
                commit('updateObjectForCard', result);
            });
        },
        async getOneTypeObjectForFeature({ commit }, { id, forFeature = false }) {
            await axios.get(`/dataset/${id}`).then((response) => {
                commit('updateOneType', { type: response.data, forFeature });
            });
        },
        async postTypeObject({ dispatch }, newType) {
            await axios.post('/dataset/admin', newType).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject', true);
            })
        },
        async putTypeObject({ dispatch }, type) {
            let putType = { ...type.properties };
            putType.id = type.id;
            await axios.put('/dataset/admin', putType).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject', true);
            });
        },
        async deleteTypeObject({ dispatch }, id) {
            await axios.delete(`/dataset/admin/${id}`).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject', true);
            })
        }
    },
    mutations: {
        updateListType(state, list) {
            state.listType = list;
        },
        updateOneType(state, { type, forFeature }) {
            if (forFeature) {
                state.typeForFeature = type;
            }
            else {
                state.type = type;
            }
        }
    },
    getters: {
        allType(state) {
            return state.listType;
        },
        oneType(state) {
            return state.type
        },
        typeForFeature(state) {
            return state.typeForFeature;
        }
    },
    state: {
        listType: [],
        type: null,
        typeForFeature: {
            id: 0,
            headers: [],
            properties: [],
        },
    },
}