import Vue from "vue";

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
            state.emptyObject = { ...object };
        },
        updateHeaders(state, headers) {
            state.headers = headers;
        },
        updateDrawType(state, drawType) {
            state.drawType = drawType;
        },
        upadateTitle(state, title){
            state.toolbarTitle = title;
            this.commit('updateNameForArray', title);
        },
        updateSelectedObejcts(state, {objects, name}){
            state.selectedObjects[`${name}`] = objects;
        },
        updateNameForArray(state, name){
            state.nameForArray = name;
            if(!(name in state.selectedObjects)){
                Vue.set(state.selectedObjects, name, []);
            }
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
            return state.selectedObjects;
        },
        nameArray(state){
            return state.nameForArray;
        },
        actions(state){
            return state.actionGet;
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
        headers: [{ text: '' }],
        drawType: '',
        toolbarTitle: null,
        nameForArray: null,
        selectedObjects: {},
    },
}