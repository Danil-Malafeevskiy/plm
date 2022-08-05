import axios from "axios";

export default{
    actions: {
        async getAllGroups({ commit }){
            await axios.get('/group').then((response) => {
                //console.log(response.data);
                commit('updateAllGroups', response.data);
            })
        },
        async getGroup({commit}, id){
            await axios.get(`/group/${id}`).then((response) => {
                //console.log(response.data);
                let group = response.data;
                group.properties = { ...group };
                for (let i in group) {
                    if (i != 'properties' && i != 'id') {
                        delete group[i];
                    }
                }
                commit('updateObjectForCard', response.data);
            })
        },
        async postGroup({ dispatch }, group){
            await axios.post('/group', group).then((response) => {
                console.log(response.data);
                dispatch('getAllGroups');
            })
        },
        async putGroup({ dispatch }, group){
            await axios.put('/group', group).then((response) => {
                console.log(response.data);
                dispatch('getAllGroups');
            })
        },
        async deleteGroup({dispatch}, id){
            await axios.delete(`/group/${id}`).then((response) => {
                console.log(response.data);
                dispatch('getAllGroups');
            })
        },
    },
    mutations: {
        updateAllGroups(state, groups){
            state.groups = groups;
            this.commit('updateListItem', {items: groups})
            this.commit('updateListType', groups)
        },
    },
    getters: {
        allGroups(state){
            return state.groups;
        }
    },
    state: {
        groups: [],
    },
}