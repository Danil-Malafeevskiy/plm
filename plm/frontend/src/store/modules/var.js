export default {
    actions: {
        async getOneObject({dispatch, state}, id){
            await dispatch(`${state.nameAction}`, id);
        }
    },
    mutations: {
        updateList(state, list) {
            state.list = [];
            state.list = list;
        },
        updateListItem(state, data) {
            state.listItem.headers = data.headers;
            state.listItem.data = data.items;
            this.commit('updateFunction', data.nameAction);
        },
        updateFunction(state, nameAction) {
            state.nameAction = nameAction;
        },
        updateObjectForCard(state, object){
            state.objectForCard = object;
        }
    },
    getters: {
        getList(state) {
            return state.list;
        },
        allListItem(state) {
            return state.listItem;
        },
        functionGetOneObject(state){
            return state.functionGetOneObject;
        },
        getObjectForCard(state){
            return state.objectForCard;
        }
    },
    state: {
        list: [],
        listItem: {
            headers: [],
            data: [],
        },
        nameAction: null,
        objectForCard: null,
    },
}