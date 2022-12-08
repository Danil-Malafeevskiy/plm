import axios from "axios";
import Vue from "vue";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

function getEditedFeatures(arrayEdited, type) {
    let array = [];
    for (let key in arrayEdited) {
        if (key != 'message') {
            array = [...array, ...arrayEdited[key][type]];
        }
    }
    return array;
}

export default {
    actions: {
        async getFeatures({ commit }) {
            await axios.get('/tower').then((response) => {
                commit('updateFeatures', response.data);
            }).catch(error => console.log(error));
        },
        async getOneFeature({ commit }, id) {
            await axios.get(`/tower/${id}`).then((response) => {
                commit('updateObjectForCard', response.data[0]);
            }).catch(error => console.log(error));
        },

        async getOneFeatureId({ commit }, id) {
            await axios.get(`/tower/${id}`).then((response) => {
                commit('updateOneFeature', response.data[0]);
            }).catch(error => console.log(error));
        },
        
        async putFeature({ commit }, features) {
            await axios.put(`/tower`, features, { headers: { "Content-Type": "application/json" } }).then((response) => {
                console.log(response.data);
                if (typeof response.data === 'string') {
                    commit('updateIsGetAllChange');
                    commit('updateConflictArrays', []);
                }
            }).catch(error => {
                if(error.response.status === 409){
                    commit('updateConflictArrays', error.response.data)
                }
            });
        },
        async deleteFeature({ commit }, features) {
            console.log(features)
            await axios.put('/tower', features).then((response) => {
                console.log(response.data);
                if (typeof response.data === 'string') {
                    commit('updateIsGetAllChange');
                }
            })
        },
        async filterForFeature({ commit, state }, typeId = state.featureTypeId) {
            state.featureTypeId = typeId;
            await axios.get(`/tower?name=${typeId}`).then((response) => {
                commit('updatefilterForFeature', response.data);
            })
        },
        async filterForFeatureForMap({ commit }, typeId) {
            await axios.get(`/tower?name=${typeId}`).then((response) => {
                commit('updateFeatureForMap', response.data);
            })
        },
        async uploadFileWithFeature({ commit }, file) {
            await axios.put('/tower/upload', file, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            }).then((response) => {
                console.log(response.data)
                if (typeof response.data === 'object') {
                    for (let i in response.data) {
                        commit('updateError', response.data[i]);
                    }
                }
            }).catch(error => console.log(error.response.data))
        },
        async getFeatureForMap({ commit }, id) {
            await axios.get(`/tower/${id}`).then((response) => {
                commit('updateFeatureInMap', response.data[0])
            });
        },
        setOffPointsFlag({commit}, flag){
            commit('updateOffPointsFlag', flag);
        }
    },
    mutations: {
        updateFeatures(state, features) {
            state.features = features;
        },
        updateResultPost(state, bool) {
            state.resultPost = bool;
        },
        updateResultPut(state, bool) {
            state.resultPut = bool;
        },
        updatefilterForFeature(state, arrFeature) {
            state.filteredFeature = arrFeature;
            let items = [];
            state.filteredFeature.forEach(element => {
                let item = { ...element.properties };
                item.id = element.id;
                items.push(item);
            });
            this.commit('updateListItem', { items }, { root: true });
        },
        updatefeatureTypeId(state, nameType) {
            state.featureTypeId = nameType;
        },
        updateOneFeature(state, data) {
            state.oneFeature = data;
        },
        updateArrayEditMode(state, { item, type }) {
            if (!(item.group in state.arrayEditMode)) {
                Vue.set(state.arrayEditMode, item.group, {
                    put: [],
                    post: [],
                    delete: [], 
                    offPoints: [],
                });
            }
            switch (type) {
                case 'post':
                    state.arrayEditMode[item.group].post.push(item);
                    state.arrayEdit.post.push(item);
                    break;

                case 'put':
                    if ('id_' in item) {
                        for (let key in state.arrayEditMode[item.group].post) {
                            if (state.arrayEditMode[item.group].post[key].id_ === item.id_) {
                                Vue.set(state.arrayEditMode[item.group].post, key, item);
                            }
                        }
                        state.arrayEdit.post = getEditedFeatures(state.arrayEditMode, 'post');
                    }
                    else {
                        state.arrayEditMode[item.group].delete = state.arrayEditMode[item.group].delete.filter(el => el.id != item.id);
                        state.arrayEdit.delete = state.arrayEdit.delete.filter(el => el.id != item.id);

                        if (state.arrayEditMode[item.group].put.find(el => el.id === item.id)) {
                            for (let key in state.arrayEditMode[item.group].put) {
                                if (state.arrayEditMode[item.group].put[key].id === item.id) {
                                    Vue.set(state.arrayEditMode[item.group].put, key, item);
                                }
                            }
                        }
                        else {
                            state.arrayEditMode[item.group].put.push(item);
                        }
                    }
                    state.arrayEdit.put = getEditedFeatures(state.arrayEditMode, 'put');
                    break;

                case 'delete':
                    if ('id_' in item) {
                        state.arrayEditMode[item.group].post = state.arrayEditMode[item.group].post.filter(el => el.id_ != item.id_);
                        state.arrayEdit.post = state.arrayEdit.post.filter(el => el.id_ != item.id_);
                    }
                    else if(!('delete' in item)) {
                        state.arrayEditMode[item.group].put = state.arrayEditMode[item.group].put.filter(el => el.id != item.id);
                        state.arrayEdit.put = state.arrayEdit.put.filter(el => el.id != item.id);

                        if (state.arrayEditMode[item.group].delete.find(el => el.id === item.id)) {
                            state.arrayEditMode[item.group].delete = state.arrayEditMode[item.group].delete.filter(el => el.id != item.id);
                        }
                        else {
                            state.arrayEditMode[item.group].delete.push(item);
                        }
                    }
                    else{
                        state.arrayEditMode[item.group].delete = [...state.arrayEditMode[item.group].delete, ...item.delete];
                        state.arrayEditMode[item.group].delete = [...new Set(state.arrayEditMode[item.group].delete)];
                    }
                    state.arrayEdit.delete = getEditedFeatures(state.arrayEditMode, 'delete');

                    break;
                
                case 'offPoints':
                    if(Object.prototype.hasOwnProperty.call(item, 'attachFlag')){
                        state.arrayEditMode[item.group].offPoints.push(item);
                        state.arrayEdit.offPoints.push(item);
                    }
                    break;
            }

        },
        deleteObjectFromArrayEditMode(state, object) {
            if (object.group in state.arrayEditMode) {
                state.arrayEditMode[object.group].put = state.arrayEditMode[object.group].put.filter(el => el.id != object.id);
                state.arrayEditMode[object.group].delete = state.arrayEditMode[object.group].delete.filter(el => el.id != object.id);
                state.arrayEdit.put = state.arrayEdit.put.filter(el => el.id != object.id);
                state.arrayEdit.put = state.arrayEdit.put.filter(el => el.id != object.id);
            }
        },
        resetArrayEditMode(state) {
            state.arrayEditMode = {
                message: '',
            }
            state.arrayEdit = {
                put: [],
                post: [],
                delete: [],
                offPoints: [],
            }
        },
        updateNewData(state, item) {
            state.newData.push(item);
        },
        deleteItemFromNewData(state, item) {
            state.newData = state.newData.filter(el => el.id != item.id);
        },
        resetNewData(state) {
            state.newData = [];
        },
        updateFeatureForMap(state, features) {
            state.featureForMap = features;
        },
        updateFeatureInMap(state, feature) {
            state.featureInMap = feature;
        },
        updateConflictArrays(state, newConlicts){
            state.conflictArrays = newConlicts;
        },
        updateOffPointsFlag(state, flag){
            state.offPointsFlag = flag;
        }
    },
    getters: {
        allFeatures(state) {
            return state.features;
        },
        getResultPost(state) {
            return state.resultPost;
        },
        getResultPut(state) {
            return state.resultPut;
        },
        getFeature(state) {
            return state.feature;
        },
        getTypeId(state) {
            return state.featureTypeId;
        },
        arrayEditMode(state) {
            return state.arrayEditMode;
        },
        arrayEdit(state) {
            return state.arrayEdit;
        },
        newData(state) {
            return state.newData;
        },
        featureForMap(state) {
            return state.featureForMap;
        },
        featureInMap(state) {
            return state.featureInMap;
        },
        conflictArrays(state){
            return state.conflictArrays;
        }, 
        oneFeature(state){
            return state.oneFeature;
        },
        offPointsFlag(state){
            return state.offPointsFlag;
        }
    },
    state: {
        features: [],
        filteredFeature: [],
        featureTypeId: null,
        feature: {
            type: 'Feature',
            keyerties: {},
            geometry: {},
        },
        arrayEditMode: {
            message: '',
        },
        arrayEdit: {
            put: [],
            post: [],
            delete: [],
            offPoints: [],
        },
        newData: [],
        featureForMap: [],
        featureInMap: {},
        conflictArrays: [],
        oneFeature: {},
        offPointsFlag: false,
    },
}