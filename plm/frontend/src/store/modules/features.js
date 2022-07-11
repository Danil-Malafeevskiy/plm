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
            await axios.post('/tower', feature).then((response) => {
                const feature = response.data;
                console.log(feature);
            });
            context.dispatch('getFeatures');
        },

        async putFeature(context, feature) {
            await axios.put('/tower', feature).then((response) => {
                const feature = response.data;
                console.log(feature);
            });
            context.dispatch('getFeatures');
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
    },
    getters: {
        allFeatures(state) {
            return state.features;
        },
    },
    state: {
        features: [],
    },
}