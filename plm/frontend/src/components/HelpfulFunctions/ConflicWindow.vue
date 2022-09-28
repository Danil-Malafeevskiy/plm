<template>
    <div class="text-center">
        <v-dialog v-model="dialog" width="500" overlay-color="white" overlay-opacity="0.8" persistent no-click-animation
            style="filter: blur(1px) !important; backdrop-filter: blur(4px) !important;">
            <v-card class="title">
                <div class="text-h6" style="text-align: center; padding: 44px 0;">
                    Были изменения в базе данных, которые привели к конфликту
                </div>
                <v-card-text>
                    <div class="btn">
                        <v-btn @click="$emit('offConflictWindow')" color="#EE5E5E" type="submit" style="height: 45px; color: white !important;">
                            ок
                        </v-btn>
                    </div>
                </v-card-text>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>

export default {
    name: 'ConflictWondow',
    data() {
        return {
            dialog: true,
        }
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