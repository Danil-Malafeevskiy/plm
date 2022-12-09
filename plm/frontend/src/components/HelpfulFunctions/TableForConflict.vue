<template>
    <div class="table_conflict">
        <v-card-text style="font-size: 16px; color: #454545; font-weight: 400; padding: 16px 30px;">
            Конфликтующие объекты
        </v-card-text>
        <v-data-table :headers="headers" item-key="id" :items="itemsForTable" hide-default-footer
            style="background-color: #FFFFFF; padding: 16px 30px;">
        </v-data-table>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'TableForConflict',
    props: ['objectForCard', 'cardVisable'],
    data() {
        return {
            headers: [
                {
                    text: 'Имя объекта',
                    value: 'id'
                },
                {
                    text: 'Тип объекта',
                    value: 'type'
                },
            ],
            itemsForTable: [],
        }
    },
    watch: {
        cardVisable: {
            handler() {
                this.changeItemFormTable();
            },
            deep: true,
        },
        objectForCard: {
            handler(){
                this.changeItemFormTable();
            }
        }
    },
    computed: {
        ...mapGetters(['conflictArrays']),
    },
    methods: {
        changeItemFormTable() {
            // console.log(this.objectForCard.id_ in this.conflictArrays);
            let conflictArr = this.objectForCard.id in this.conflictArrays ? this.conflictArrays[this.objectForCard.id] : [];
            conflictArr = this.objectForCard.id_ in this.conflictArrays ? this.conflictArrays[this.objectForCard.id_] : []
            this.itemsForTable = conflictArr;
        }
    },
    mounted() {
        this.changeItemFormTable()
    }
}
</script>

<style>
.table_conflict {
    position: absolute;
    bottom: 0;
    top: 30%;
    left: 0;
    right: 0;
    z-index: 3;
}
</style>