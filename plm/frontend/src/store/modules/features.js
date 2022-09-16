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
                // if (state.featureTypeId != null) {
                //     dispatch('filterForFeature');
                // }
            }).catch(error => console.log(error));
        },

        async getOneFeature({ commit }, id) {
            await axios.get(`/tower/${id}`).then((response) => {
                commit('updateObjectForCard', response.data[0]);
            }).catch(error => console.log(error));
        },

        async postFeature({ dispatch }, feature) {
            await axios.post('/tower', feature).then((response) => {
                console.log(response.data);
                dispatch('getFeatures');
            }).catch(error => console.log(error));
        },

        async putFeature(ctx, features) {
            let data;
            if ('put' in features) {
                data = [...features.put, ...features.post, getStrId(features.delete), features.messege];
            }
            else {
                data = [...features, [], '']
            }
            await axios.put(`/tower`, data).then((response) => {
                console.log(response.data);
            }).catch(error => console.log(error)); 
        },

        async deleteFeature(ctx, features) {
            console.log(getStrId(features));
            await axios.put(`/tower`, [getStrId(features), '']).then((response) => {
                console.log(response.data);
            }).catch(error => console.log(error));
        },
        async filterForFeature({ commit, state }, typeId = state.featureTypeId) {
            state.featureTypeId = typeId;
            await axios.get(`/tower?name=${typeId}`).then((response) => {
                commit('updatefilterForFeature', response.data);
            })
        },

        async uploadFileWithFeature(ctx, file) {
            await axios.put('/tower/upload', file, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            }).then((response) => console.log(response.data))
        },

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
                    Vue.set(state.arrayEditMode.post, state.arrayEditMode.post.length, item);
                    break;

                case 'put':
                    if ('id_' in item) {
                        Vue.set(state.arrayEditMode.post, item.id_ - 1, item);
                    }
                    else {
                        state.arrayEditMode.delete = state.arrayEditMode.delete.filter(el => el.id != item.id);

                        if (state.arrayEditMode.put.filter(el => el.id === item.id).length) {
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

                        if (!state.arrayEditMode.delete.filter(el => el.id === item.id).length) {
                            state.arrayEditMode.delete.push(item);
                        }
                        else {
                            state.arrayEditMode.delete = state.arrayEditMode.delete.filter(el => el.id != item.id);
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
    },
}