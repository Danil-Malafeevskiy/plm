export default {
    actions: {
        async getAllObject({ dispatch, state }) {
            await dispatch(`${state.actionGet}`);
        },
        async getOneObject({ dispatch, state }, id) {
            await dispatch(`${state.actionOneGet}`, id);
        },
        async postObject({ dispatch, state }, object) {
            await dispatch(`${state.actionPost}`, object)
        },
        async putObject({ dispatch, state }, object) {
            await dispatch(`${state.actionPut}`, object);
        },
        async deleteObject({ dispatch, state }, id) {
            await dispatch(`${state.actionDelete}`, id);
        },
    },
    mutations: {
        updateList(state, list) {
            state.list = [];
            state.list = list;
        },
        updateListItem(state, data) {
            state.listItem = data.items;
        },
        updateAction(state, nameAction) {
            state.actionGet = nameAction.actionGet;
            state.actionPost = nameAction.actionPost;
            state.actionPut = nameAction.actionPut;
            state.actionDelete = nameAction.actionDelete;
            state.actionOneGet = nameAction.actionOneGet;
        },
        updateObjectForCard(state, object) {
            state.objectForCard = object;
        },
        upadateEmptyObject(state, object) {
            state.emptyObject = JSON.parse(JSON.stringify(object));
            delete state.emptyObject.id;
            this.commit('updateFieldEmptyObject');
        },
        updateFieldEmptyObject(state, object = state.emptyObject) {
            for (let i in object) {
                if (i != 'headers') {
                    switch (typeof object[i]) {
                        case 'string':
                            object[i] = '';
                            break;
                        case 'boolean':
                            object[i] = false;
                            break;
                        case 'object':
                            this.commit('updateFieldEmptyObject', object[i]);
                            break;
                        default:
                            object[i] = 0;
                            break;
                    }
                }
            }
        },
        updateHeaders(state, headers) {
            state.headers = headers;
        },
        updateDrawType(state, drawType) {
            state.drawType = drawType;
        },
        upadateTitle(state, title){
            state.toolbarTitle = title;
        },
        updateSelectedObejcts(state, {objects, name}){
            state.slectedObjects[`${name}`] = objects;
            console.log(state.slectedObjects)
        },
        addSelectedObject(state, object, name){
            console.log(name);
            state.slectedObjects[`${name}`].push(object);
            console.log(state.slectedObjects);
        },
        addArrayFromSelectedObject(state, name){
            state.slectedObjects[`${name}`] = [];
            console.log(state.slectedObjects)
        }
    },
    getters: {
        getList(state) {
            return state.list;
        },
        allListItem(state) {
            return state.listItem;
        },
        functionGetOneObject(state) {
            return state.functionGetOneObject;
        },
        getObjectForCard(state) {
            return state.objectForCard;
        },
        emptyObject(state) {
            return state.emptyObject;
        },
        headers(state) {
            return state.headers;
        },
        drawType(state) {
            return state.drawType;
        },
        getToolbarTitle(state){
            return state.toolbarTitle;
        },
        arrObjects(state){
            return state.slectedObjects;
        }
    },
    state: {
        list: [],
        listItem: [],
        actionGet: 'getFeatures',
        actionOneGet: 'getOneFeature',
        actionPost: 'postFeature',
        actionPut: 'putFeature',
        actionDelete: 'deleteFeature',
        objectForCard: null,
        emptyObject: {},
        headers: {},
        drawType: '',
        toolbarTitle: null,
        slectedObjects: {},
    },
}