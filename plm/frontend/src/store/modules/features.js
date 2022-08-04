import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async getFeatures({ commit, state }) {
            await axios.get('/tower').then((response) => {
                const features = response.data;
                commit('updateFeatures', features);
                if (state.featureNameType != null) {
                    commit('filterForFeature');
                }
            }).catch(error => console.log(error));
        },

        async getOneFeature({ commit }, id) {
            await axios.get(`/tower/${id}`).then((response) => {
                const feature = response.data;
                commit('updateObjectForCard', feature[0]);
            }).catch(error => console.log(error));
        },

        async postFeature({ dispatch }, feature) {
            await axios.post('/tower', feature, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => {
                console.log(response.data);
                dispatch('getFeatures');
            }).catch(error => console.log(error));
        },

        async putFeature({ dispatch }, feature,) {
            await axios.put('/tower', feature, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => {
                const feature = response.data;
                console.log(feature);
                dispatch('getFeatures');
            }).catch(error => console.log(error));
        },

        async deleteFeature({ dispatch }, id) {
            await axios.delete(`/tower/${id}`).then((response) => {
                const feature = response.data;
                console.log(feature);
            }).catch(error => console.log(error));
            dispatch('getFeatures');
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
        emptyFeature(state) {
            for (let key in state.features[0]) {
                if (key === 'properties') {
                    for (let key1 in state.features[0][key]) {
                        if (key1 != 'id') {
                            if (typeof (state.features[0][key][key1]) === 'string')
                                state.feature[key][key1] = "";
                            else if (typeof (state.features[0][key][key1]) === 'boolean')
                                state.feature[key][key1] = false;
                            else
                                state.feature[key][key1] = 1;
                        }
                    }
                }
            }
            delete state.feature.id;
        },
        filterForFeature(state, nameType = state.featureNameType) {
            state.featureNameType = nameType;
            state.filteredFeature = state.features.filter(r => (` ${r.name}` === state.featureNameType));
            let headers = [
                {
                    text: 'Номер опоры',
                    align: 'start',
                    sortable: false,
                    value: 'Номер опоры',
                },
                { text: 'ВЛ', value: 'ВЛ' },
                { text: 'Тип опоры', value: 'Тип опоры' },
                { text: 'Материал', value: 'Материал' },
            ];
            let items = [];
            state.filteredFeature.forEach(element => {
                let test = element.properties;
                test.id = element.id;
                items.push(test);
            });
            this.commit('updateListItem', {items, headers, nameAction: 'getOneFeature'}, { root:true });
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
        featureName(state) {
            return state.featureNameType;
        }
    },
    state: {
        features: [],
        filteredFeature: [],
        featureNameType: null,
        feature: {
            type: 'Feature',
            properties: {},
            geometry: {},
        },
    },
}