<template>
	<div class="counter">
		<span class="object" v-if="tableArray.length % 10 === 1">{{ tableArray.length }} объект </span>
		<span class="object" v-else-if="tableArray.length % 10 > 1 && tableArray.length % 10 < 5">
			{{ tableArray.length }} объекта </span>
		<span class="object" v-else>{{ tableArray.length }} объектов </span>

		<v-data-table :headers="headers" :items="tableArray" hide-default-footer style="
			height: 100% !important;
			width: 95% !important; 
			background-color: #E5E5E5; 
			box-shadow: none !important;
			margin-left: 2% !important;" @click:row="chooseVersion"
			:item-class="currentVersionStyle"
			></v-data-table>
	</div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
export default {
	components: {
	},
	data() {
		return {
			headers: [
				{
					text: '',
					align: 'start',
					sortable: false,
					value: 'name',
				},
				{ text: 'id', value: 'id' },
				{ text: 'Дата', value: 'date_update' },
				{ text: 'Автор', value: 'user' },
				{ text: 'Комментарий', value: 'comment' },
				{ text: 'Flag', value: 'flag' },
			],
			tableArray: this.allVersions,
			timeLastVersion: null,
			currentVersion: null,
		}
	},
	watch: {
		allVersions: {
			handler() {
				this.tableArray = this.allVersions
				this.timeLastVersion = 0
				this.tableArray.forEach(element => {
					if (element === this.tableArray.filter(element => element.flag)[0]) {
						// this.timeLastVersion = time
						this.currentVersion = element
					}
				})
				console.log(this.tableArray)
			}
		},
	},
	computed: {
		...mapGetters(['allVersions'])
	},
	methods: {
		...mapActions(['getVersions', 'putVersion']),
		...mapMutations(['updateVersions']),
		chooseVersion(item){
			this.putVersion(item.id)
		},
		getTimeVersion(time) {
			let data = new Date(time)
			return data
		},
		currentVersionStyle(item){
			if(item === this.currentVersion) {
				return 'current'
			} 
		},
	},
	
	async mounted() {
		this.getVersions()
	}
}
</script>

<style>
.object {
	margin: 20px 5px 20px 20px;
	color: #787878;
	font-weight: 500;
}
.current{
	background-color: rgb(251, 218, 218);
}

.afterCurrent{
	background-color: grey;
}

</style>