export default {
    actions: {
    },
    mutations: {
        updateList(state, list){
            state.list = [];
            state.list = list;
        }
    },
    getters: {
        getList(state){
            return state.list;
        }
    },
    state: {
        list: [],
    },
}