<template>
	<div>
		<v-scroll-x-reverse-transition>
			<div id="notification">&nbsp;&nbsp;&nbsp;&nbsp;Развитие версии изменено</div>
		</v-scroll-x-reverse-transition>
	
		<div style="margin: 20px 5px 20px 20px; color: #787878; font-weight: 500;">
			<span v-if="tableArray.length % 10 === 1">{{ tableArray.length }} объект </span>
			<span v-else-if="tableArray.length % 10 > 1 && tableArray.length % 10 < 5">
				{{ tableArray.length }} объекта </span>
			<span v-else>{{ tableArray.length }} объектов </span>
		</div>

		<v-data-table :headers="headers" :items="tableArray" :items-per-page="5" style="
			height: 100% !important;
			width: 95% !important; 
			background-color: #E5E5E5; 
			box-shadow: none !important;
			margin-left: 2% !important;" @click:row="chooseVersion" sort-by="id" :sort-desc="true"
			>
	
			<template v-slot:[`item.select`]="{ item }">
				<v-btn v-model="item.select" class='columnText' text id="no-background-hover" tile
					:style="[(item.flag) ? {'color' : '#EE5E5E'} : {'color' : '#b6b3b3'}]">
					Последняя версия
				</v-btn>
			</template>
	
		</v-data-table>

		<v-btn text id="no-background-hover" class="lastVersion ma-2 pa-2" tile @click="lastVersion">Выбрать текущие данные</v-btn>
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
					align: 'center',
					sortable: false,
				},
				// { text: 'id', value: 'id' },
				{ text: 'Дата', value: 'date_update', align: 'start' },
				{ text: 'Автор', value: 'user', align: 'start' },
				{ text: 'Комментарий', value: 'comment', align: 'start' },
				// { text: 'Flag', value: 'flag' },
			],
			tableArray: [],
			currentVersionId: null,
			currentVersion: null,
			nameGroup: null,
		}
	},
	watch: {
		allVersions: {
			handler() {
				this.tableArray = this.allVersions
				let id = 0
				this.tableArray.forEach(element => {
					if (element === this.tableArray.filter(element => element.flag)[0]) {
						this.currentVersion = element
						this.currentVersionId = element.id
					} 
					else if (!this.tableArray.filter(element => element.flag).length) {
						if ( id < element.id){
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
		...mapGetters(['allVersions', 'allListItem', 'getList', 'getTypeId', 'allGroups', 'allFilteredVersions', 'user','allUserGroups' ])
	},
	methods: {
		...mapActions(['getVersions', 'putVersion', 'getGroup', 'getAllGroups', 'getAllUserGroups', 'putLastVersion']),
		...mapMutations(['updateVersions', 'updateFilteredVersions', 'updateAllGroups', 'updateAllUserGroups']),
		chooseVersion(item) {
			this.putVersion(item.id)
			document.getElementById('notification').style.display = 'block'
			setTimeout(function () {
				document.getElementById('notification').style.display = 'none'
			}, 5000);
			
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
		getGroup(){
			this.allGroups.forEach(element => {
				if ( element.id === this.getTypeId){
					this.nameGroup = element.name
				}
			});
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
				setTimeout(function () {
					document.getElementById('notification').style.display = 'none'
				}, 5000);
				
				this.putLastVersion(id)
			}
		}
		
	},

	async mounted() {
		this.getVersions()
	}, 

}
</script>

<style >
.object {
	margin: 20px 5px 20px 20px;
	color: #787878;
	font-weight: 500;
}

.noCurrent{
	background: #F2F2F2 !important;
}

.current{
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