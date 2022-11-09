<template>
    <div class="text-center">
        <v-dialog class="d" v-model="dialog" width="500" overlay-color="white">
            <v-card class="title">
                <div class="text-h6" style="text-align: center; padding: 44px 0;">
                    Выберите файл для импорта и группу
                </div>
                <div>
                    <v-file-input v-model="file" hide_details prepend-icon="mdi-file-upload">
                    </v-file-input>
                    <v-row no-gutters justify="space-between"
                        style="width: 390px; margin: 0 auto; padding-bottom: 20px">
                        <v-col v-for="el in user.groups" :key="el" style="max-width: 30%; margin-left: 20px !important"
                            cols="2" sm="6" md="5" lg="6" class="pa-0 ma-0">
                            <v-radio-group hide-details v-model="group">
                                <v-radio color="#E93030" :label="el" :value="el" on-icon="mdi-checkbox-marked"
                                    off-icon="mdi-checkbox-blank-outline">
                                </v-radio>
                            </v-radio-group>
                        </v-col>
                    </v-row>
                    <v-select v-model="fileName" @click="test" :items="allTypeForUpload.filter(el => el.group === group).map(el => el.name)"
                        label="Имя типа" style="padding: 0 24px; z-index: 204" filled>
                    </v-select>
                </div>
                <v-card-text>
                    <div class="btn">
                        <v-btn @click="fileUpload"
                            :disabled="!file || !group || !fileName || (user.permissions.filter(el => el.includes(group)).length != 2 && (!user.is_staff || !user.is_superuser))"
                            color="#EE5E5E" block style="height: 45px; color: white !important;">
                            ок
                        </v-btn>
                        <v-btn @click="$emit('offFileInput')" color="#EE5E5E" block
                            style="height: 45px; color: white !important;">
                            отмена
                        </v-btn>
                    </div>
                </v-card-text>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    name: 'ConflictWondow',
    data() {
        return {
            dialog: true,
            file: null,
            componentKey: 0,
            group: '',
            fileName: '',
            types: ['Point', 'LineString', 'Polygon'],
        }
    },
    computed: mapGetters(['user', 'allTypeForUpload']),
    methods: {
        ...mapActions(['uploadFileWithFeature', 'getAllTypeForUpload']),
        fileUpload() {
            this.uploadFileWithFeature({ file: this.file, group: this.group, filename: this.fileName });
            this.componentKey++;
            this.$emit('offFileInput');
        },
        test() {
            setTimeout(() => {
                let element = document.querySelectorAll('.v-menu__content');
                if (element.length == 2) {
                    element = element[1];
                }
                else {
                    element = element[0];
                }
                element.style.setProperty('height', `${[...new Set(this.allTypeForUpload.filter(el => el.group === this.group))].length * 48 + 16}px`, 'important');
            }, 100)
        }
    },
    async mounted() {
        await this.getAllTypeForUpload();
    }
}
</script>

<style scoped>
.title,
.v-card,
.v-sheet {
    min-height: 37% !important;
    max-width: 47.85% !important;
    background-color: #DDDDDD;
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    box-shadow: none !important;
    border-radius: 12px !important;
}

.v-btn {
    min-height: 12.23% !important;
    max-height: 15% !important;
}

.text_centre {
    border-radius: 12px;
}

.btn {
    padding-top: 12px
}
</style>

<style>
.v-icon.v-icon::after {
    background-color: transparent !important;
}

.v-menu__content .v-select-list {
    max-width: 100% !important;
    width: 100% !important;
}
</style>