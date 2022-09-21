import axios from "axios";

export default {
    actions: {

        async getVersions({ commit }) {
            await axios.get('/version').then((response) => {
                commit('updateVersions', response.data)
                // console.log(response.data)
            })
        },

        async getFilteredVersions({ commit, state }, group) {
            state.pastGroupVersion = group;
            await axios.get(`/version?dataset=${group}`).then((response) => {
                commit('updateFilteredVersions', response.data)
                // console.log(response.data)
            })
        },

        async putVersion({ dispatch, state },id){
            axios.put(`/version/${id}`).then((response) => {
                if (state.pastGroupVersion){
                    dispatch('getFilteredVersions', state.pastGroupVersion);
                }
                else{
                    dispatch('getVersions');
                }
                console.log(response.data)
            })
        },

        async putLastVersion({dispatch},id){
            let lastVersion = {'flag' : true}
            axios.put(`/version/${id}`, lastVersion).then((response) => {
                console.log(response.data)
                dispatch('getVersions');
                dispatch('getFeatures');
                
            })
        },
    },
    mutations: {
        updateVersions(state, versions) {
            state.versions = versions
        },
        updateFilteredVersions(state, filteredVersions){
            state.versions = filteredVersions
        }
    },
    getters: {
        allVersions(state) {
            return state.versions
        },
    },
    state: {
        versions: [],
        pastGroupVersion: null,
    }
}