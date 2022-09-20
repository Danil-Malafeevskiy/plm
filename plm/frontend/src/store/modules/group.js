import axios from "axios";

export default {
    actions: {
        async getAllGroups({ commit }) {
            await axios.get('/group').then((response) => {
                commit('updateAllGroups', response.data);
            })
        }, 

        async getAllUserGroups({ commit }){
            await axios.get('/user').then((response) => {
                let group = { ...response.data };
                commit('updateAllUserGroups', group.groups)
            })
        },

        async getGroup({ commit }, id) {
            await axios.get(`/group/${id}`).then((response) => {
                let group = { ...response.data };
                group.properties = { name: group.name };
                delete group.name;
                commit('updateObjectForCard', group);
            })
        },
        async getUsersOfGroup({ commit, state }, group = state.group) {
            await axios.get(`/user/admin?groups=${group.id}`).then((response) => {
                console.log(response.data);
                if (typeof response.data === 'object') {
                    commit('updateListItem', { items: response.data })
                }
                else {
                    commit('updateListItem', { items: [] })
                }
                commit('updateGroup', group);
            });
        },
        async postGroup({ dispatch }, group) {
            group.permissions = [];
            await axios.post('/group', group).then((response) => {
                console.log(response.data);
                dispatch('getAllGroups');
            })
        },
        async putGroup({ dispatch }, group) {
            group ={ ...group, ...group.properties};
            delete group.properties;
            await axios.put('/group', group).then((response) => {
                console.log(response.data);
                dispatch('getAllGroups');
            })
        },
        async deleteGroup({ dispatch }, id) {
            await axios.delete(`/group/${id}`).then((response) => {
                console.log(response.data);
                dispatch('getAllGroups');
            })
        },
    },
    mutations: {
        updateAllGroups(state, groups) {
            state.groups = groups;
            this.commit('updateListItem', { items: groups })
            this.commit('updateListType', groups)
        },
        updateGroup(state, group){
            state.group = group;
        }, 
        updateAllUserGroups(state, groups){
            state.userGroups = groups
            this.commit('updateListItem', { items: groups })
            this.commit('updateListType', groups)
        }
    },
    getters: {
        allGroups(state) {
            return state.groups;
        },
        currentGroup(state){
            return state.group;
        }, 
        allUserGroups(state){
            return state.userGroups
        }
    },
    state: {
        groups: [],
        group: {
            id: null,
            name: null
        },
        userGroups: []
    },
}