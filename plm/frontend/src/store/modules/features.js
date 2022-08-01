import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export default {
    actions: {
        async getFeatures(context) {
            await axios.get('/tower').then((response) => {
                const features = response.data;
                context.commit('updateFeatures', features);
            }).catch(error => console.log(error));
        },

        async getOneFeature(context, id){
            await axios.get(`/tower/${id}`).then((response) => {
                const feature = response.data;
                context.commit('updateOneFeature', feature[0]);
            }).catch(error => console.log(error));
        },

        async postFeature(context, feature) {
            await axios.post('/tower', feature, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => {
                console.log(response.data);
                context.dispatch('getFeatures');
            }).catch(error => console.log(error));
        },

        async putFeature(context, feature, ) {
            await axios.put('/tower', feature, {
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => {
                const feature = response.data;
                console.log(feature);
                context.dispatch('getFeatures');
            }).catch(error => console.log(error));
        },

        async deleteFeature(context, id) {
            await axios.delete(`/tower/${id}`).then((response) => {
                const feature = response.data;
                console.log(feature);
            }).catch(error => console.log(error));
            context.dispatch('getFeatures');
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
        updateOneFeature(state, feature) {
            state.feature = feature;
        },
        filterForFeature(state, nameType) {
            state.featureNameType = nameType;
            state.filteredFeature = state.features.filter(r => (` ${r.name}` === state.featureNameType))
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
        filterFeature(state) {
            return state.filteredFeature;
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