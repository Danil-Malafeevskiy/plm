<template>
    <div>
        <v-checkbox v-if="user.is_superuser && actions === 'getUsersOfGroup'" v-model="userAdmin" label="Admin" :readonly="objectForCard !== emptyObject" class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                    margin-left: 24px !important;
                                ">
        </v-checkbox>
        <div style="margin: 0 0 10px 24px"
            v-if="'properties' in objectForCard &&  ((userAdmin &&'first_name' in objectForCard.properties) || 'type' in objectForCard.properties)">
            <v-expansion-panels accordion flat class="pa-0 ma-0">
                <v-expansion-panel class="pa-0 ma-0">
                    <v-expansion-panel-header class="pa-0 ma-0">
                        Группы
                    </v-expansion-panel-header>


                    <v-expansion-panel-content class="ma-0 pa-0">
                        <v-row class="pa-2 ma-0">
                            <template v-if="'groups' in objectForCard">
                                <v-col v-for="(f, index) in user.groups" :key="f" cols="2" sm="6" md="5" lg="6"
                                    class="pa-0 ma-0" v-show="f != 'Admin'">

                                    <v-checkbox v-model="objectForCard_.groups" :label="f" :value="user.groups[index]"
                                        :readonly="infoCardOn.data" class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                ">
                                    </v-checkbox>
                                </v-col>
                            </template>
                            <template v-else>
                                <v-col v-for="(f, index) in user.groups" :key="index" cols="2" sm="6" md="5" lg="6"
                                    class="pa-0 ma-0">
                                    <v-radio-group hide-details class="ma-0 pa-0"
                                        v-model="objectForCard_.properties.group">
                                        <v-radio :label="f" :value="user.groups[index]" :readonly="infoCardOn.data"
                                            class="ma-2" color="#E93030" on-icon="mdi-checkbox-marked"
                                            off-icon="mdi-checkbox-blank-outline" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                ">
                                        </v-radio>
                                    </v-radio-group>
                                </v-col>
                            </template>
                        </v-row>
                    </v-expansion-panel-content>

                </v-expansion-panel>
            </v-expansion-panels>
        </div>
        <div style="margin: 0 0 10px 24px" v-else-if="'permissions' in objectForCard">
            <v-expansion-panels accordion flat class="pa-0 ma-0">
                <v-expansion-panel>

                    <v-expansion-panel-header class="pa-0 ma-0">
                        Группы
                    </v-expansion-panel-header>


                    <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                        <v-expansion-panels accordion flat class="pa-0 ma-0">
                            <v-expansion-panel v-for="el in user.groups" id="permission" :key="el" cols="2" sm="6"
                                md="5" lg="6" class="pa-0 ma-0">

                                <v-expansion-panel-header class="pa-0 ma-0" style="margin-left: 0.5em !important;" v-show="el != 'Admin'">
                                    {{ el }}
                                </v-expansion-panel-header>

                                <v-expansion-panel-content class="ma-0 pa-0">
                                    <v-row class="pa-2 ma-0">
                                        <v-col v-for="(name, index) in user.user_permissions" :key="name" cols="2"
                                            sm="6" md="5" lg="6" class="pa-0 ma-0" v-show="name.includes(el)">
                                            <v-checkbox @click="changeGroups(el)"
                                                v-model="objectForCard_.permissions" :readonly="infoCardOn.data"
                                                class="ma-2" color="#E93030" :value="user.user_permissions[index]"
                                                style="
                                                                        min-height: 37.53% !important; 
                                                                        max-height: 37.53% !important;
                                                                    " :label="name">
                                            </v-checkbox>

                                        </v-col>
                                    </v-row>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-expansion-panel-content>

                </v-expansion-panel>
            </v-expansion-panels>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex';

export default {
    name: 'ExpansionPanel',
    props: ['objectForCard', 'infoCardOn', 'cardVisable'],
    data() {
        return {
            groups: [],         // Группы прав
            userGroups: [],
            permissionList: [], // список всех прав
            groupsForType: [],
            objectForCard_: this.objectForCard,
            adminPermissions: null,
            userPermissions: null,
            groupAdminId: null,
            allGroups_: this.allGroups,
            userAdmin: false,
            group: '',
        }
    },
    watch: {
        objectForCard: {
            async handler() {
                this.objectForCard_ = this.objectForCard;
                console.log(this.objectForCard_)
            }
        },
        'objectForCard.permissions': {
            handler() {
                if (this.group) {
                    if (this.objectForCard_.permissions.find(el => el.includes(this.group))) {
                        this.objectForCard_.groups.push(this.group);
                        this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)];
                    }
                    else {
                        this.objectForCard_.groups = this.objectForCard_.groups.filter(el => el != this.group);
                    }
                    console.log(this.objectForCard_.groups);
                }
            }
        },
        userAdmin: {
            handler() {
                if(this.userAdmin){
                    this.objectForCard_.groups.push('Admin');
                }
                else{
                    this.objectForCard_.groups = this.objectForCard_.groups.filter(el => el != 'Admin');
                }
                console.log(this.objectForCard_.groups);
            }
        }
    },
    computed: mapGetters(['user', 'currentGroup', 'allGroups', 'allUsersForAdmin', 'emptyObject', 'actions']),
    methods: {
        ...mapActions(['getAllUsersForAdmin', 'getAllGroups', 'getUser']),
        ...mapMutations(['updateAllUsersForAdmin', 'updateAllGroups']),
        changeGroups(group) {
            this.group = group;
        }
    },

    async mounted() {
        await this.getUser();
    }
}
</script>

<style>

</style>