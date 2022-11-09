<template>
    <div>
        <div style="display: flex" v-if="user && user.is_superuser && actions === 'getUsersOfGroup'">
            <v-checkbox v-model="objectForCard_.is_staff" label="Admin" :readonly="infoCardOn.data" class="ma-2"
                color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                    margin-left: 24px !important;
                                ">
            </v-checkbox>
            <v-checkbox v-model="objectForCard_.is_superuser" label="Super User" :readonly="infoCardOn.data"
                class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                    margin-left: 24px !important;
                                ">
            </v-checkbox>
        </div>
        <div style="margin: 0 0 10px 24px"
            v-if="'properties' in objectForCard && 'all_group_type' in objectForCard.properties">
            <v-expansion-panels accordion flat class="pa-0 ma-0">
                <v-expansion-panel class="pa-0 ma-0">

                    <v-expansion-panel-header class="pa-0 ma-0">
                        Запрет на пересечение
                    </v-expansion-panel-header>

                    <v-expansion-panel-content class="ma-0 pa-0">
                        <v-row class="pa-2 ma-0">
                            <v-col v-for="(f) in objectForCard.properties.all_group_type" :key="f" cols="2" sm="6"
                                md="5" lg="6" class="pa-0 ma-0" v-show="f != 'Admin'">

                                <v-checkbox v-model="objectForCard_.ruls" :label="f" :value="f" hide-details
                                    :readonly="infoCardOn.data" class="ma-2" color="#E93030" style="
                                    min-height: 37.53% !important; 
                                    max-height: 37.53% !important;
                                ">
                                </v-checkbox>
                            </v-col>
                        </v-row>
                    </v-expansion-panel-content>

                </v-expansion-panel>
            </v-expansion-panels>
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
                                        hide-details :readonly="infoCardOn.data" class="ma-2" color="#E93030" style="
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
                                            hide-details class="ma-2" color="#E93030" on-icon="mdi-checkbox-marked"
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
                        <v-icon style="max-height: 34px; margin: 8px">mdi-file-eye-outline</v-icon>
                        <v-icon style="max-height: 34px;  margin: 8px; margin-left: 15px;">mdi-file-edit-outline
                        </v-icon>
                        <span style="color: #A5A5A6; font-weight: 500; margin-left: 15px;">Группы пользователей</span>
                        <div v-for="el in user.groups" :key="el" style="display: flex;" v-show="el != 'Admin'">
                            <div style="display: flex">
                                <v-checkbox @click="changeGroups(el)" v-model="objectForCard_.permissions"
                                    :readonly="infoCardOn.data" class="ma-2" color="#E93030" hide-details
                                    :value="user.user_permissions.filter(element => element.includes(el))[1]" style="
                                        min-height: 37.53% !important; 
                                        max-height: 37.53% !important;">
                                </v-checkbox>

                                <v-checkbox @click="changeGroups(el)" v-model="objectForCard_.permissions"
                                    :readonly="infoCardOn.data" class="ma-2" color="#E93030" hide-details
                                    :value="user.user_permissions.filter(element => element.includes(el))[0]" style="
                                        min-height: 37.53% !important; 
                                        max-height: 37.53% !important;">
                                </v-checkbox>
                                <span class="mt-3" style="margin-left: 6px; color: #C2C2C2" :class="{
                                    'selected_group': objectForCard_.permissions.find(element => element.includes(el)),
                                }">{{ el }}</span>
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
                        <v-expansion-panels accordion flat class="pa-0 ma-0">
                            <v-expansion-panel v-for="(group, index) in user.all_users" :key="index">

                                <v-expansion-panel-header class="pa-0 ma-0">
                                    {{ index }}
                                </v-expansion-panel-header>
                                <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                                    <v-row class="pa-2 ma-0">
                                        <v-col v-for="user in user.all_users[`${index}`]" :key="user" cols="2" sm="6" md="5"
                                            lg="6" class="pa-0 ma-0">
                                            <v-checkbox v-model="objectForCard_.users" hide-details
                                                :readonly="infoCardOn.data" class="ma-2" color="#E93030" :value="user"
                                                :label="user" style="
                                        min-height: 37.53% !important; 
                                        max-height: 37.53% !important;">
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
        }
    },
    watch: {
        objectForCard: {
            async handler() {
                this.objectForCard_ = this.objectForCard;
                if ('properties' in this.objectForCard && 'all_group_type' in this.objectForCard.properties) {
                    this.objectForCard_.ruls = [...this.objectForCard_.properties.group_type];
                }
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
.selected_group {
    color: #454545 !important;
}
</style>