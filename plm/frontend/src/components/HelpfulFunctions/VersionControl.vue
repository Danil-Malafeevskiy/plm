<template>
	<div>
		<v-scroll-x-reverse-transition>
			<div id="notification">&nbsp;&nbsp;&nbsp;&nbsp;Развитие версии изменено</div>
		</v-scroll-x-reverse-transition>

		<div style="margin: 20px 5px 20px 20px; color: #787878; font-weight: 500;">
			<span >{{ tableArray.length }} версий </span>
		</div>

		<v-data-table :headers="headers" :items="tableArray" :items-per-page="5" style="
			height: 100% !important;
			width: 95% !important; 
			background-color: #FFFFFF; 
			box-shadow: none !important;
			margin-left: 2% !important;" @click:row="chooseVersion" sort-by="id" :sort-desc="true">
			
			<template v-slot:[`item.select`]="{ item }">

				<v-btn v-model="item.select" plain small class='columnText' fab 
					style="
						border-radius: 100% !important; 
						padding: 4px 10px !important; 
						max-height: 20px !important; 
						max-width: 20px !important;
					"
					id="no-background-hover"
					:style="[(item.flag) ? { 'background-color': '#E93030' } : (item.id <= currentVersionId) ? {'background-color': '#F8BFBF'} : { 'background-color': '#DDDDDD' }]">
				</v-btn>
			</template>

		</v-data-table>

		<v-btn text id="no-background-hover" class="lastVersion ma-2 pa-2" tile @click="lastVersion">Выбрать текущие
			данные</v-btn>
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
					value: 'select',
					align: 'start',
					sortable: false,
					width: '0%'
				},
				{ text: 'Дата', value: 'date_update', align: 'start', width: '7%' },
				{ text: 'Время', value: 'time', align: 'start', width: '7%' },
				{ text: 'Автор', value: 'user', align: 'start', width: '15%' },
				{ text: 'Комментарий', value: 'comment', align: 'start' },
			],
			tableArray: [],
			currentVersionId: null,
			currentVersion: null,
			nameGroup: null,
			timeoutId: null,
		}
	},
	watch: {
		allVersions: {
			handler() {
				this.tableArray = this.allVersions
				let id = 0
				this.tableArray.forEach(element => {
					element.time = element.date_update.split(' ')[1].slice(0, -3);
					element.date_update = element.date_update.split(' ')[0];
					if (element === this.tableArray.filter(element => element.flag)[0]) {
						this.currentVersion = element
						this.currentVersionId = element.id
					}
					else if (!this.tableArray.filter(element => element.flag).length) {
						if (id < element.id) {
							this.currentVersion = element
							this.currentVersionId = element.id
							id = element.id
						}
					}
				})
			}
		},
	},
	computed: {
		...mapGetters(['allVersions', 'allListItem', 'getList', 'getTypeId', 'allGroups', 'allFilteredVersions', 'user', 'allUserGroups', 'allType'])
	},
	methods: {
		...mapActions(['getVersions', 'putVersion', 'getGroup', 'getAllGroups', 'getAllUserGroups', 'putLastVersion', 'getFilteredVersions']),
		...mapMutations(['updateVersions', 'updateFilteredVersions', 'updateAllGroups', 'updateAllUserGroups']),
		chooseVersion(item) {
			this.putVersion(item.id)
			document.getElementById('notification').style.display = 'block'
			this.showNotification()

		},
		getTimeVersion(time) {
			let data = new Date(time)
			return data
		},
		currentVersionStyle(item) {
			if (item.id > this.currentVersionId) {
				return 'noCurrent'
			}
		},
		getGroup() {
			this.allGroups.forEach(element => {
				if (element.id === this.getTypeId) {
					this.nameGroup = element.name
				}
			});
		},

		showNotification() {
			clearTimeout(this.timeoutId)
			this.timeoutId = setTimeout(function () {
				document.getElementById('notification').style.display = 'none'
			}, 2000);
		},

		lastVersion() {
			if (this.tableArray.filter(el => el.flag).length) {
				let id = 0
				this.tableArray.forEach(element => {
					if (element.id > id) {
						id = element.id
					}
				});
				document.getElementById('notification').style.display = 'block'
				this.showNotification()

				this.putLastVersion(id)
			}
		}

	},

	async mounted() {
		if (this.allType.length) {
			this.getFilteredVersions(this.allType[0]);
		}
	},

}
</script>

<style scoped>

* >>> td:first-child {
	border: hidden !important;
}

* >>> th:first-child {
	border: hidden !important;
}

* >>> .v-data-footer {
	margin-left: 6.4em;
}
</style>


<style>

.object {
	margin: 20px 5px 20px 20px;
	color: #787878;
	font-weight: 500;
}

.noCurrent {
	background: #F2F2F2 !important;
}

.current {
	background: #F2F2F2;
	color: #EE5E5E !important;
}

.columnText {
	font-weight: 500;
	font-size: 14px;
	line-height: 16px;
	display: flex;
	align-items: center;
	text-align: right;
	letter-spacing: 1.25px;
	text-transform: uppercase;
	border-bottom: thin solid white !important;
}

#no-background-hover::before {
	background-color: transparent !important;
	display: none !important;
}


.lastVersion {
	left: 77.8%;
	display: flex;
	flex-direction: row;
	justify-content: flex-end;
}

#notification {
	background-color: #FBDADA;
	width: 100%;
	color: #D7153A;
	display: none;
}



</style>