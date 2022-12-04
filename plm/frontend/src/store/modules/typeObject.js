import axios from "axios";

function getUrl(user){
    let url;
    if(user.is_staff || user.is_superuser){
        url = '/dataset/admin';
    }
    else{
        url = '/dataset';
    }
    return url;
}

export default {
    actions: {
        async getTypeObject({ commit, getters }, change = false) {
            await axios.get(getUrl(getters.user)).then((response) => {
                if (!change) {
                    commit('updateListType', response.data);
                }
                else {
                    commit('updateListItem', { items: response.data });
                }
            });
        },
        async getAllType({ commit }) {
            await axios.get('/dataset').then((response) => {
                commit('updateAllTypeForMap', response.data);
            })
        },
        async getAllTypeForUpload({ commit }) {
            await axios.get('/dataset').then((response) => {
                commit('updateAllTypeForUpload', response.data);
            })
        },
        async getOneTypeObject({ commit, getters }, id) {
            switch (typeof id) {
                case 'number': {
                    await axios.get(getUrl(getters.user) + `/${id}`).then((response) => {
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
                    })
                    break;
                }
                case 'object': {
                    await axios.get(getUrl(getters.user) + `/${id.id}`).then((response) => {
                        commit('updateTypeForLayer', response.data);
                    })
                    break;
                }
            }
        },
        async getOneTypeObjectForFeature({ commit, getters }, { id, forFeature = false }) {
            await axios.get(getUrl(getters.user) + `/${id}`).then((response) => {
                commit('updateOneType', { type: response.data, forFeature });
            });
        },
        async postTypeObject({ dispatch, commit, state }, newType) {
            console.log(newType);
            await axios.post('/dataset/admin', newType).then((response) => {
                if (typeof response.data === 'object') {
                    for (let i in response.data) {
                        commit('updateError', response.data[i]);
                    }
                }
                else if (typeof response.data === 'string') {
                    commit('updateIsGetAllChange');
                }
                if (state.pastGroup != null) {
                    dispatch('getAllTypeInGroup', state.pastGroup);
                }
                else {
                    dispatch('getAllTypeForTable');
                }
                dispatch('allGroupForNav');
            })
        },
        async putTypeObject({ dispatch, commit, state }, type) {
            console.log(type);
            let putType = { ...type.properties };
            for (let key in type) {
                if (key != 'properties') {
                    putType[key] = type[key]
                }
            }
            console.log(putType);
            await axios.put('/dataset/admin', putType).then((response) => {
                if (typeof response.data === 'object') {
                    for (let i in response.data) {
                        commit('updateError', response.data[i]);
                    }
                }
                else if (typeof response.data === 'string') {
                    commit('updateIsGetAllChange');
                }
                if (state.pastGroup != null) {
                    dispatch('getAllTypeInGroup', state.pastGroup);
                }
                else{
                    dispatch('getAllTypeForTable');
                }
                dispatch('allGroupForNav');
            });
        },
        async deleteTypeObject({ dispatch, commit, state }, id) {
            await axios.delete(`/dataset/admin?id=${[id.map(el => el.id)]}`).then((response) => {
                console.log(response.data);
                if (typeof response.data === 'string') {
                    commit('updateIsGetAllChange');
                }
                if (state.pastGroup != null) {
                    dispatch('getAllTypeInGroup', state.pastGroup);
                }
                else {
                    dispatch('getAllTypeForTable');
                }
                dispatch('allGroupForNav');
            })
        },
        async getSortType({ commit }, drawType) {
            await axios.get(`/dataset?type=${drawType}`).then((response) => {
                commit('updateSelectedDrawType', response.data);
            })
        },
        async getAllTypeForTable({ commit }) {
            await axios.get('/dataset').then((response) => {
                commit('updateAllTypeForTable', response.data)
            })
        },
        async getAllTypeInGroup({ commit, state }, group) {
            state.pastGroup = group;
            await axios.get(`/dataset?group=${group}`).then((response) => {
                commit('updateAllTypeForTable', response.data);
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
        },
        updateTypeForLayer(state, type) {
            state.typeForLayer = type;
        },
        updateSelectedDrawType(state, type) {
            state.selectedDrawType = type;
        },
        updateAllTypeForMap(state, types) {
            state.allTypeForMap = types;
        },
        updateAllTypeForTable(state, types) {
            state.allTypeForTable = types;
            this.commit('updateListItem', { items: types });
        },
        updateAllTypeForUpload(state, types){
            state.allTypeForUpload = types;
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
        },
        typeForLayer(state) {
            return state.typeForLayer;
        },
        selectedDrawType(state) {
            return state.selectedDrawType;
        },
        allTypeForMap(state) {
            return state.allTypeForMap;
        },
        allTypeForTable(state) {
            return state.allTypeForTable
        },
        allTypeForUpload(state){
            return state.allTypeForUpload;
        }
    },
    state: {
        listType: [],
        allTypeForMap: [],
        allTypeForUpload: [],
        type: null,
        typeForFeature: {
            id: 0,
            headers: [],
            properties: [],
        },
        typeForLayer: {},
        selectedDrawType: [],
        allTypeForTable: [],
        pastGroup: null,
    },
}