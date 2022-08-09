import axios from "axios";

export default {
    actions: {
        async getTypeObject({ commit }, change = false) {
            await axios.get('/dataset').then((response) => {
                if (!change) {
                    commit('updateListType', response.data);
                }
                else{
                    commit('updateListItem', {items: response.data});
                }
            });
        },
        async getOneTypeObject({ commit }, id) {
            await axios.get(`/dataset/${id}`).then((response) => {
                let result = response.data;
                result.properties = { ...result };
                for (let i in result) {
                    if (i != 'properties' && i != 'id') {
                        delete result[i];
                    }
                }
                commit('updateObjectForCard', result);
                commit('updateOneType', response.data);
            });
        },
        async postTypeObject({ dispatch }, newType) {
            newType.headers = [
                {
                    "text": "Номер опоры",
                    "align": "start",
                    "value": "Номер опоры",
                    "sortable": false
                },
                {
                    "text": "ВЛ",
                    "value": "ВЛ"
                },
                {
                    "text": "Тип опоры",
                    "value": "Тип опоры"
                },
                {
                    "text": "Материал",
                    "value": "Материал"
                }
            ]

            console.log(newType);
            await axios.post('/dataset', newType).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject', true);
            })
        },
        async putTypeObject({ dispatch }, type) {
            for(let key in type.properties){
                type[key] = type.properties[key];
            }
            delete type.properties;
            await axios.put('/dataset', type).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject', true);
            });
        },
        async deleteTypeObject({ dispatch }, id) {
            await axios.delete(`/dataset/${id}`).then((response) => {
                console.log(response.data);
                dispatch('getTypeObject', true);
            })
        }
    },
    mutations: {
        updateListType(state, list) {
            state.listType = list;
        },
        updateOneType(state, type) {
            state.type = type;
        }
    },
    getters: {
        allType(state) {
            return state.listType;
        },
        oneType(state) {
            return state.type
        }
    },
    state: {
        listType: [],
        type: null,
    },
}