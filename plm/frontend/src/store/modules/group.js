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
                commit('updateObjectForCard', response.data);
            })
        }
    },
    mutations: {
        updateAllGroups(state, groups){
            state.groups = groups;
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