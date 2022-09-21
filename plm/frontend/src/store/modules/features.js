import axios from "axios";
import Vue from "vue";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

function getStrId(features) {
    let strId = [];
    for (let i in features) {
        strId.push(features[i].id);
    }
    return strId;
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
        async putFeature({ commit }, features) {
            let data;
            if ('put' in features) {
                data = [...features.put, ...features.post, getStrId(features.delete), features.messege];
            }
            else {
                data = [...features, [], '']
            }
            await axios.put(`/tower`, data, {headers:{"Content-Type" : "application/json"}}).then((response) => {
                console.log(response.data);
                if(typeof response.data === 'string'){
                    commit('updateIsGetAllChange');
                }
            }).catch(error => console.log(error)); 
        },
        async deleteFeature({ commit }, feature){
            await axios.put('/tower', [ getStrId(feature), '']).then((response) => {
                console.log(response.data);
                if(typeof response.data === 'string'){
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
        async filterForFeatureForMap({ commit }, typeId){
            await axios.get(`/tower?name=${typeId}`).then((response) => {
                commit('updateFeatureForMap', response.data);
            })
        },
        async uploadFileWithFeature(ctx, file) {
            await axios.put('/tower/upload', file, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            }).then((response) => console.log(response.data))
        },
        async getFeatureForMap({ commit }, id){
            await axios.get(`/tower/${id}`).then((response) => {
                commit('updateFeatureInMap', response.data[0])
            });
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
        updateArrayEditMode(state, { item, type }) {
            switch (type) {
                case 'post':
                    state.arrayEditMode.post.push(item);
                    break;

                case 'put':
                    if ('id_' in item) {
                        for (let key in state.arrayEditMode.post) {
                            if (state.arrayEditMode.post[key].id_ === item.id_) {
                                Vue.set(state.arrayEditMode.post, key, item);
                            }
                        }
                    }
                    else {
                        state.arrayEditMode.delete = state.arrayEditMode.delete.filter(el => el.id != item.id);
                        if (state.arrayEditMode.put.find(el => el.id === item.id)) {
                            for (let key in state.arrayEditMode.put) {
                                if (state.arrayEditMode.put[key].id === item.id) {
                                    Vue.set(state.arrayEditMode.put, key, item);
                                }
                            }
                        }
                        else {
                            state.arrayEditMode.put.push(item);
                        }
                    }
                    break;

                case 'delete':
                    if ('id_' in item) {
                        state.arrayEditMode.post = state.arrayEditMode.post.filter(el => el.id_ != item.id_);
                    }
                    else {
                        state.arrayEditMode.put = state.arrayEditMode.put.filter(el => el.id != item.id);

                        if (state.arrayEditMode.delete.find(el => el.id === item.id)) {
                            state.arrayEditMode.delete = state.arrayEditMode.delete.filter(el => el.id != item.id);
                        }
                        else {
                            state.arrayEditMode.delete.push(item);
                        }
                    }
                    break;
            }

        },
        resetArrayEditMode(state) {
            state.arrayEditMode = {
                put: [],
                post: [],
                delete: [],
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
        updataFeatureForMap(state, features){
            state.featureForMap = features;
        },
        updateFeatureInMap(state, feature){
            state.featureInMap = feature;
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
        newData(state) {
            return state.newData;
        },
        featureForMap(state){
            return state.featureForMap;
        },
        featureInMap(state){
            return state.featureInMap;
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
            put: [],
            post: [],
            delete: [],
            messege: '',
        },
        newData: [],
        featureForMap: [],
        featureInMap: {}
    },
}