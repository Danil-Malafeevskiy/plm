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
                                <v-col v-for="(f, index) in groupsForType" :key="index" cols="2" sm="6" md="5" lg="6"
                                    class="pa-0 ma-0">
                                    <v-radio-group hide-details class="ma-0 pa-0" v-model="objectForCard_.properties.group">
                                        <v-radio :label="f" :value="groupsForType[index]" :readonly="infoCardOn.data"
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

                    <v-expansion-panel-content cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                        <v-expansion-panels accordion flat class="pa-0 ma-0">
                            <v-expansion-panel v-for="el in groups" id="permission" :key="el" cols="2" sm="6" md="5"
                                lg="6" class="pa-0 ma-0">

                                <v-expansion-panel-header class="pa-0 ma-0" style="margin-left: 0.5em !important;">
                                    {{  el  }}
                                </v-expansion-panel-header>

                                <v-expansion-panel-content class="ma-0 pa-0">
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
import { mapGetters } from 'vuex';

export default {
    name: 'ExpansionPanel',
    props: ['objectForCard', 'infoCardOn'],
    data() {
        return {
            groups: [],         // Группы прав
            userGroups: [],
            permissionList: [], // список всех прав
            groupsForType: [],
            objectForCard_: this.objectForCard, 
        }
    },
    watch: {
        user: {
            handler() {
                this.groupsForType = [...this.user.groups]
                this.userGroups = [...this.user.groups, ...this.user.avaible_group]
                this.permissionList = [...this.user.permissions, ...this.user.avaible_permission]
                this.groupsPermissions()
            },
        },
        objectForCard: {
            handler(){
                this.objectForCard_ = this.objectForCard;
            }
        }
    },
    computed: mapGetters(['user']),
    methods: {
        groupsPermissions() {
            for (let i = 0; i < this.permissionList.length; ++i) {
                let el = this.permissionList[i].split(" ").pop();
                el = el[0].toUpperCase() + el.slice(1);
                this.groups.push(el);
            }
            this.groups = [...new Set(this.groups)]
        },
    },
}
</script>

<style>
</style>