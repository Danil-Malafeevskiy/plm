import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async getFeatures({ commit, state, dispatch }) {
            await axios.get('/tower').then((response) => {
                commit('updateFeatures', response.data);
                if (state.featureTypeId != null) {
                    dispatch('filterForFeature');
                }
            }).catch(error => console.log(error));
        },

        async getOneFeature({ commit }, id) {
            await axios.get(`/tower/${id}`).then((response) => {
                commit('updateObjectForCard', response.data[0]);
            }).catch(error => console.log(error));
        },

        async postFeature({ dispatch }, feature) {
            await axios.post('/tower', feature).then((response) => {
                console.log(response.data);
                dispatch('getFeatures');
            }).catch(error => console.log(error));
        },

        async putFeature(ctx, feature) {
            await axios.put('/tower', feature).then((response) => {
                const feature = response.data;
                console.log(feature);
            }).catch(error => console.log(error));
        },

        async deleteFeature(ctx, id) {
            await axios.delete(`/tower/${id}`).then((response) => {
                const feature = response.data;
                console.log(feature);
            }).catch(error => console.log(error));
        },
        async filterForFeature({ commit, state }, typeId = state.featureTypeId) {
            state.featureTypeId = typeId;
            await axios.get(`/tower?name=${typeId}`).then((response) => {
                commit('updatefilterForFeature', response.data);
            })
        }
    },
    mutations: {
        updateFeatures(state, features) {
            state.features = features;
        },
        updateResultPost(state, bool) {
            state.resultPost = bool;
        },
        updateResultPut(state, bool) {
            state.resultPut = bool;
        },
        updatefilterForFeature(state, arrFeature) {
            state.filteredFeature = arrFeature;
            let items = [];
            state.filteredFeature.forEach(element => {
                let item = { ...element.properties };
                item.id = element.id;
                items.push(item);
            });
            this.commit('updateListItem', { items }, { root: true });
        },
        updatefeatureTypeId(state, nameType) {
            state.featureTypeId = nameType;
        },
        updateArrayEditMode(state, { item, type }) {
            switch (type) {
                case 'put':
                    if (state.arrayEditMode.put.filter(el => el.id === item.id).length === 0) {
                        state.arrayEditMode[type].push(item);
                    }
                    else {
                        for (let key in state.arrayEditMode.put) {
                            if (state.arrayEditMode.put[key].id === item.id) {
                                state.arrayEditMode.put[key] = item;
                            }
                        }
                    }
                    break;
                case 'delete':
                    if (state.arrayEditMode.delete.filter(el => el.id === item.id).length === 0) {
                        state.arrayEditMode[type].push(item);
                    }
                    else {
                        state.arrayEditMode.delete = state.arrayEditMode.delete.filter(el => el.id != item.id);
                    }
                    break;
            }







        },
        resetArrayEditMode(state) {
            state.arrayEditMode = {
                put: [],
                post: [],
                delete: [],
            }
        }
    },
    getters: {
        allFeatures(state) {
            return state.features;
        },
        getResultPost(state) {
            return state.resultPost;
        },
        getResultPut(state) {
            return state.resultPut;
        },
        getFeature(state) {
            return state.feature;
        },
        getTypeId(state) {
            return state.featureTypeId;
        },
        arrayEditMode(state) {
            return state.arrayEditMode;
        }
    },
    state: {
        features: [],
        filteredFeature: [],
        featureTypeId: null,
        feature: {
            type: 'Feature',
            keyerties: {},
            geometry: {},
        },
        arrayEditMode: {
            put: [],
            post: [],
            delete: [],
        }
    },
}