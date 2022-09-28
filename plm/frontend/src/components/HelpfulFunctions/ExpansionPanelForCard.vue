<template>
    <div>
        <div style="margin: 0 0 10px 24px"
            v-if="'properties' in objectForCard && ('username' in objectForCard.properties || 'type' in objectForCard.properties)">
            <v-expansion-panels accordion flat class="pa-0 ma-0">
                <v-expansion-panel class="pa-0 ma-0">
                    <v-expansion-panel-header class="pa-0 ma-0">
                        Группы
                    </v-expansion-panel-header>


                    <v-expansion-panel-content class="ma-0 pa-0">
                        <v-row class="pa-2 ma-0">
                            <template v-if="'groups' in objectForCard">
                                <v-col v-for="(f, index) in userGroups" :key="f" cols="2" sm="6" md="5" lg="6"
                                    class="pa-0 ma-0">

                                    <v-checkbox v-model="objectForCard_.groups" :label="f" :value="userGroups[index]"
                                        :readonly="infoCardOn.data" class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                ">
                                    </v-checkbox>
                                </v-col>
                            </template>
                            <template v-else>
                                <v-col v-for="(f, index) in userGroups" :key="index" cols="2" sm="6" md="5" lg="6"
                                    class="pa-0 ma-0">
                                    <v-radio-group multiple hide-details class="ma-0 pa-0"
                                        v-model="objectForCard_.properties.group">
                                        <v-radio :label="f" :value="userGroups[index]" :readonly="infoCardOn.data"
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
        <div style="margin: 0 0 10px 24px" v-if="'permissions' in objectForCard">
            <v-expansion-panels accordion flat class="pa-0 ma-0">
                <v-expansion-panel>

                    <v-expansion-panel-header class="pa-0 ma-0">
                        Права
                    </v-expansion-panel-header>


                    <v-expansion-panel-content  cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                        <v-expansion-panels accordion flat class="pa-0 ma-0">
                            <v-expansion-panel v-for="el in groups" id="permission" :key="el" cols="2" sm="6" md="5"
                                lg="6" class="pa-0 ma-0">

                                <v-expansion-panel-header class="pa-0 ma-0" style="margin-left: 0.5em !important;">
                                    {{ el }}
                                </v-expansion-panel-header>

                                <v-expansion-panel-content class="ma-0 pa-0" >
                                    <v-row class="pa-2 ma-0">
                                        <v-col v-for="(name, index) in permissionList" :key="name" cols="2" sm="6" 
                                            md="5" lg="6" class="pa-0 ma-0">
                                            <v-checkbox v-if="name.includes(el[0].toLowerCase() + el.slice(1))"
                                                v-model="objectForCard_.permissions" :readonly="infoCardOn.data"
                                                class="ma-2" color="#E93030" :value="permissionList[index]" style="
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
            usersAdmin: [],
        }
    },
    watch: {
        objectForCard: {
            handler() {
                this.objectForCard_ = this.objectForCard;
                if (this.user.is_superuser) {
                    if (this.currentGroup.name === 'Admin' || this.usersAdmin.includes(this.objectForCard_.id) || this.objectForCard_.groups.includes('Admin')) {
                        this.permissionList = [...this.user.admin_permissions];
                        this.objectForCard_.groups.push('Admin')
                    }
                } else {
                    this.permissionList = [...this.user.user_permissions];
                }
                this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)]
                this.groupsPermissions();
            }
        },

        'objectForCard.groups': {
            handler(){
                this.objectForCard_ = this.objectForCard;

                if (this.objectForCard_.groups.includes('Admin') && this.user.is_superuser) {
                    this.usersAdmin.push(this.objectForCard.id);
                    this.usersAdmin = [...new Set(this.usersAdmin)]
                    this.permissionList = [...this.user.admin_permissions]
                } else {
                    this.usersAdmin.filter(el => el.id != this.objectForCard.id);
                    this.permissionList = [...this.user.user_permissions]
                }

                if (this.cardVisable.data) {
                    this.objectForCard_.permissions = this.permissionList
                } 

                this.groupsPermissions();
            }
        },

        allGroups: {
            handler() {
                if (this.user.is_superuser) {
                    this.allGroups_ = this.allGroups
                    this.allGroups_.forEach(element => {
                        if (element.name === 'Admin') {
                            this.groupAdminId = element.id
                        }
                    });
                    this.getAllUsersForAdmin(this.groupAdminId);
                }
            }
        },
        allUsersForAdmin: {
            handler() {
                if (this.user.is_superuser) {
                    this.usersAdmin = this.allUsersForAdmin.map(element => element.id);
                }
            }
        },

        currentGroup: {
            handler(){
                if (this.user.is_superuser) {
                    if (this.cardVisable.data && !this.infoCardOn.data && this.currentGroup.name === 'Admin') {
                        this.permissionList = [...this.user.admin_permissions]
                        this.objectForCard_.groups.push(this.currentGroup.name)
                    } else if (this.cardVisable.data && !this.infoCardOn.data && this.currentGroup.name) {
                        this.permissionList = [...this.user.user_permissions];
                        this.objectForCard_.groups.push(this.currentGroup.name)
                    } else if (this.usersAdmin.includes(this.objectForCard_.id)) {
                        this.permissionList = [...this.user.admin_permissions]
                        this.objectForCard_.groups.push('Admin')
                    } else {
                        this.permissionList = [...this.user.user_permissions];
                    }
                }
                this.groupsPermissions();
                this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)]
            },
            deep: true,
        }
    },
    computed: mapGetters(['user', 'currentGroup', 'allGroups', 'allUsersForAdmin']),
    methods: {
        ...mapActions(['getAllUsersForAdmin', 'getAllGroups']),
        ...mapMutations(['updateAllUsersForAdmin', 'updateAllGroups']),
        groupsPermissions() {
            this.groups = []
            for (let i = 0; i < this.permissionList.length; ++i) {
                let el = this.permissionList[i].split(" ").pop();
                el = el[0].toUpperCase() + el.slice(1);
                this.groups.push(el);
            }
            this.groups = [...new Set(this.groups)]
        },
    },

    mounted() {
        this.userGroups = [...this.user.groups];
        this.groupsPermissions();
    }
}
</script>

<style>

</style>