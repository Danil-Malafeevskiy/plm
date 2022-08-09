import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async getFeatures({ commit, state }) {
            await axios.get('/tower').then((response) => {
                commit('updateFeatures', response.data);
                if (state.featureNameType != null) {
                    commit('filterForFeature');
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

        async putFeature({ dispatch }, feature,) {
            await axios.put('/tower', feature).then((response) => {
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
        filterForFeature(state, nameType = state.featureNameType) {
            state.featureNameType = nameType;
            state.filteredFeature = state.features.filter(r => (`${r.name}` === state.featureNameType));
            let items = [];
            state.filteredFeature.forEach(element => {
                let item = JSON.parse(JSON.stringify(element.properties));
                item.id = element.id;
                items.push(item);
            });
            this.commit('updateListItem', { items }, { root: true });
        },
        updateFeatureNameType(state, nameType){
            state.featureNameType = nameType;
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
            keyerties: {},
            geometry: {},
        },
    },
}