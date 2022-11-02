<template>
    <div>
        <div style="display: flex">
            <v-checkbox v-if="user.is_superuser && actions === 'getUsersOfGroup'" v-model="objectForCard_.is_staff"
                label="Admin" :readonly="infoCardOn.data" class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                    margin-left: 24px !important;
                                ">
            </v-checkbox>
            <v-checkbox v-if="user.is_superuser && actions === 'getUsersOfGroup'" v-model="objectForCard_.is_superuser"
                label="Super User" :readonly="infoCardOn.data" class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                    margin-left: 24px !important;
                                ">
            </v-checkbox>
        </div>
        <div style="margin: 0 0 10px 24px"
            v-if="'properties' in objectForCard && ((objectForCard_.is_staff && 'first_name' in objectForCard.properties) || 'type' in objectForCard.properties)">
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
                        Права
                    </v-expansion-panel-header>


                    <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                        <div v-for="el in user.groups" :key="el" style="display: flex; justify-content: space-between;"
                            v-show="el != 'Admin'">
                            <span class="mt-3">{{ el }}</span>
                            <div style="display: flex">
                                <v-checkbox @click="changeGroups(el)" v-model="objectForCard_.permissions"
                                    :readonly="infoCardOn.data" class="ma-2" color="#E93030"
                                    :value="user.user_permissions.filter(element => element.includes(el))[1]" style="
                                        min-height: 37.53% !important; 
                                        max-height: 37.53% !important;">
                                </v-checkbox>
                                <v-icon class="mt-1  mr-2" style="max-height: 34px">mdi-book-open-blank-variant</v-icon>
                                <v-checkbox @click="changeGroups(el)" v-model="objectForCard_.permissions"
                                    :readonly="infoCardOn.data" class="ma-2" color="#E93030"
                                    :value="user.user_permissions.filter(element => element.includes(el))[0]" style="
                                        min-height: 37.53% !important; 
                                        max-height: 37.53% !important;">
                                </v-checkbox>
                                <v-icon class="mt-1" style="max-height: 34px">mdi-pencil</v-icon>
                            </div>
                        </div>
                    </v-expansion-panel-content>

                </v-expansion-panel>
            </v-expansion-panels>
        </div>
        <div style="margin: 0 0 10px 24px" v-else-if="'users' in objectForCard">
            <v-expansion-panels accordion flat class="pa-0 ma-0">
                <v-expansion-panel>

                    <v-expansion-panel-header class="pa-0 ma-0">
                        Пользователи
                    </v-expansion-panel-header>


                    <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                        <v-row class="pa-2 ma-0">
                            <v-col v-for="el in user.all_users" :key="el" cols="2" sm="6" md="5" lg="6"
                                class="pa-0 ma-0">
                                <v-checkbox v-model="objectForCard_.users" :readonly="infoCardOn.data" class="ma-2"
                                    color="#E93030" :value="el" :label="el" style="
                                        min-height: 37.53% !important; 
                                        max-height: 37.53% !important;">
                                </v-checkbox>
                            </v-col>
                        </v-row>
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
        }
    },
    watch: {
        objectForCard: {
            async handler() {
                this.objectForCard_ = this.objectForCard;
                console.log(this.objectForCard_)
            }
        },
        'objectForCard.is_staff': {
            handler() {
                if (this.objectForCard.is_staff && !this.objectForCard.is_superuser) {
                    this.objectForCard_.groups.push('Admin');
                    this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)];
                }
                else {
                    this.objectForCard_.groups = this.objectForCard_.groups.filter(el => el != 'Admin');
                }
            }
        },
        'objectForCard.is_superuser': {
            handler() {
                if (this.objectForCard.is_staff && this.objectForCard.is_superuser) {
                    this.objectForCard_.groups = this.objectForCard_.groups.filter(el => el != 'Admin');

                }
                else if (this.objectForCard.is_staff) {
                    this.objectForCard_.groups.push('Admin');
                    this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)];
                }
                else if (this.objectForCard.is_superuser) {
                    this.objectForCard_.is_staff = true;
                }
            }
        }
    },
    computed: mapGetters(['user', 'currentGroup', 'allGroups', 'allUsersForAdmin', 'emptyObject', 'actions']),
    methods: {
        ...mapActions(['getAllUsersForAdmin', 'getAllGroups', 'getUser']),
        ...mapMutations(['updateAllUsersForAdmin', 'updateAllGroups']),
        changeGroups(group) {
            if (this.objectForCard_.permissions.find(el => el.includes(group) && el.includes('Изменение'))) {
                this.objectForCard_.permissions.push(`Просмотр объектов ${group}`);
                this.objectForCard_.groups.push(group);

                this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)];
                this.objectForCard_.permissions = [...new Set(this.objectForCard_.permissions)];
            }
            else if (this.objectForCard_.permissions.find(el => el.includes(group))) {
                this.objectForCard_.groups.push(group);
                this.objectForCard_.groups = [...new Set(this.objectForCard_.groups)];
            }
            else {
                this.objectForCard_.groups = this.objectForCard_.groups.filter(el => el != group);
            }
        },
    },

    async mounted() {
        await this.getUser();
    }
}
</script>

<style>

</style>