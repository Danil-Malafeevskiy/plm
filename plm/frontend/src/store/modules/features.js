import axios from "axios";

export default {
    actions: {
        async getFeatures(context) {
            await axios.get('/tower').then((response) => {
                const features = response.data;
                context.commit('updateFeatures', features);
            });
        },

        async postFeature(context, feature) {
            const res = await axios.post('/tower', feature).catch(error => console.log(error));
            console.log(res.data);
            context.dispatch('getFeatures');
        },

        async putFeature(context, feature) {
            await axios.put('/tower', feature).then((response) => {
                const feature = response.data;
                console.log(feature);
                context.dispatch('getFeatures');
            });
        },

        async deleteFeature(context, id) {
            await axios.delete(`/tower/${id}`).then((response) => {
                const feature = response.data;
                console.log(feature);
            });
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
                            else if (typeof (state.features[0][key][key1]) === 'number')
                                state.feature[key][key1] = 1;
                            else if (typeof (state.features[0][key][key1]) === 'boolean')
                                state.feature[key][key1] = false;
                        }
                    }
                }
            }
            delete state.feature.id;
        },
        updateFeature(state, feature){ 
            state.feature = feature;
        },
        filterForFeature(state, nameType){
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
        filterFeature(state){
            return state.filteredFeature;
        },
        featureName(state){
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