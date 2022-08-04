import Vue from 'vue';
import Vuex from 'vuex';
import features from './modules/features';
import auth from './modules/auth'
import group from './modules/group'
import Var from './modules/var'
import typeObject from './modules/typeObject'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        features,
        auth,
        group,
        Var,
        typeObject
    }
});