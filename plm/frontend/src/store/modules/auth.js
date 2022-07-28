import axios from "axios";

export default{
    actions:{
        async postAuth(context, userData) {
            await axios.post('/tower/login', userData).then((response) => {
                const features = response.data;
                console.log(features);
            });
        },
    },

    mutations:{

    },
    getters:{

    },
    state:{        
        features: [],
        userData: {
            username: null,
            password:null
        },
    },
}