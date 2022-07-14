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
            context.commit('updateResultPost', (res.data === 'Success new'));
            context.dispatch('getFeatures');
        },

        async putFeature(context, feature) {
            await axios.put('/tower', feature).then((response) => {
                const feature = response.data;
                context.commit('updateResultPut', (feature === 'Success up'));
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
        updateResultPost(state, bool){
            state.resultPost = bool;
        },
        updateResultPut(state, bool){
            state.resultPut = bool;
        }
    },
    getters: {
        allFeatures(state) {
            return state.features;
        },
        getResultPost(state){
            return state.resultPost;
        },
        getResultPut(state){
            return state.resultPut;
        }
    },
    state: {
        features: [],
        resultPost: null,
        resultPut: null,
    },
}